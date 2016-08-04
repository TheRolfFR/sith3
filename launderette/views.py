from datetime import datetime, timedelta
from collections import OrderedDict
import pytz

from django.shortcuts import render
from django.views.generic import ListView, DetailView, RedirectView, TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView, BaseFormView
from django.forms.models import modelform_factory
from django.forms import CheckboxSelectMultiple
from django.utils.translation import ugettext as _
from django.utils import dateparse
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.db import transaction
from django import forms
from django.template import defaultfilters
from django.utils import formats

from core.models import Page
from club.models import Club
from core.views import CanViewMixin, CanEditMixin, CanEditPropMixin, CanCreateMixin
from launderette.models import Launderette, Token, Machine, Slot
from subscription.views import get_subscriber
from subscription.models import Subscriber
from counter.models import Counter, Customer, Selling
from counter.views import GetUserForm

# For users

class LaunderetteMainView(TemplateView):
    """Main presentation view"""
    template_name = 'launderette/launderette_main.jinja'

    def get_context_data(self, **kwargs):
        """ Add page to the context """
        kwargs = super(LaunderetteMainView, self).get_context_data(**kwargs)
        kwargs['page'] = Page.objects.filter(name='launderette').first()
        return kwargs

class LaunderetteBookMainView(CanViewMixin, ListView):
    """Choose which launderette to book"""
    model = Launderette
    template_name = 'launderette/launderette_book_choose.jinja'

class LaunderetteBookView(CanViewMixin, DetailView):
    """Display the launderette schedule"""
    model = Launderette
    pk_url_kwarg = "launderette_id"
    template_name = 'launderette/launderette_book.jinja'

    def get(self, request, *args, **kwargs):
        self.slot_type = "BOTH"
        self.machines = {}
        return super(LaunderetteBookView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.slot_type = "BOTH"
        self.machines = {}
        with transaction.atomic():
            self.object = self.get_object()
            if 'slot_type' in request.POST.keys():
                self.slot_type = request.POST['slot_type']
            if 'slot' in request.POST.keys() and request.user.is_authenticated():
                self.subscriber = get_subscriber(request.user)
                if self.subscriber.is_subscribed():
                    self.date = dateparse.parse_datetime(request.POST['slot']).replace(tzinfo=pytz.UTC)
                    if self.slot_type == "WASHING":
                        if self.check_slot(self.slot_type):
                            Slot(user=self.subscriber, start_date=self.date, machine=self.machines[self.slot_type], type=self.slot_type).save()
                    elif self.slot_type == "DRYING":
                        if self.check_slot(self.slot_type):
                            Slot(user=self.subscriber, start_date=self.date, machine=self.machines[self.slot_type], type=self.slot_type).save()
                    else:
                        if self.check_slot("WASHING") and self.check_slot("DRYING", self.date + timedelta(hours=1)):
                            Slot(user=self.subscriber, start_date=self.date, machine=self.machines["WASHING"], type="WASHING").save()
                            Slot(user=self.subscriber, start_date=self.date + timedelta(hours=1),
                                    machine=self.machines["DRYING"], type="DRYING").save()
        return super(LaunderetteBookView, self).get(request, *args, **kwargs)

    def check_slot(self, type, date=None):
        if date is None: date = self.date
        for m in self.object.machines.filter(is_working=True, type=type).all():
            slot = Slot.objects.filter(start_date=date, machine=m).first()
            if slot is None:
                self.machines[type] = m
                return True
        return False

    @staticmethod
    def date_iterator(startDate, endDate, delta=timedelta(days=1)):
        currentDate = startDate
        while currentDate < endDate:
            yield currentDate
            currentDate += delta

    def get_context_data(self, **kwargs):
        """ Add page to the context """
        kwargs = super(LaunderetteBookView, self).get_context_data(**kwargs)
        kwargs['planning'] = OrderedDict()
        kwargs['slot_type'] = self.slot_type
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=pytz.UTC)
        for date in LaunderetteBookView.date_iterator(start_date, start_date+timedelta(days=6), timedelta(days=1)):
            kwargs['planning'][date] = []
            for h in LaunderetteBookView.date_iterator(date, date+timedelta(days=1), timedelta(hours=1)):
                free = False
                if self.slot_type == "BOTH" and self.check_slot("WASHING", h) and self.check_slot("DRYING", h + timedelta(hours=1)):
                    free = True
                elif self.slot_type == "WASHING" and self.check_slot("WASHING", h):
                    free = True
                elif self.slot_type == "DRYING" and self.check_slot("DRYING", h):
                    free = True
                if free and datetime.now().replace(tzinfo=pytz.UTC) < h:
                    kwargs['planning'][date].append(h)
                else:
                    kwargs['planning'][date].append(None)
        return kwargs

# For admins

class LaunderetteListView(CanEditPropMixin, ListView):
    """Choose which launderette to administer"""
    model = Launderette
    template_name = 'launderette/launderette_list.jinja'

class LaunderetteEditView(CanEditPropMixin, UpdateView):
    """Edit a launderette"""
    model = Launderette
    pk_url_kwarg = "launderette_id"
    fields = ['name']
    template_name = 'core/edit.jinja'

class LaunderetteCreateView(CanCreateMixin, CreateView):
    """Create a new launderette"""
    model = Launderette
    fields = ['name']
    template_name = 'core/create.jinja'

    def form_valid(self, form):
        club = Club.objects.filter(unix_name=settings.SITH_LAUNDERETTE_MANAGER['unix_name']).first()
        c = Counter(name=form.instance.name, club=club, type='OFFICE')
        c.save()
        form.instance.counter = c
        return super(LaunderetteCreateView, self).form_valid(form)

class LaunderetteDetailView(CanEditPropMixin, DetailView):
    """The admin page of the launderette"""
    model = Launderette
    pk_url_kwarg = "launderette_id"
    template_name = 'launderette/launderette_detail.jinja'

class GetLaunderetteUserForm(GetUserForm):
    def clean(self):
        cleaned_data = super(GetLaunderetteUserForm, self).clean()
        sub = get_subscriber(cleaned_data['user'])
        if sub.slots.all().count() <= 0:
            raise forms.ValidationError(_("User has booked no slot"))
        return cleaned_data

class LaunderetteMainClickView(CanEditMixin, BaseFormView, DetailView):
    """The click page of the launderette"""
    model = Launderette
    pk_url_kwarg = "launderette_id"
    template_name = 'counter/counter_main.jinja'
    form_class = GetLaunderetteUserForm # Form to enter a client code and get the corresponding user id

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(LaunderetteMainClickView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(LaunderetteMainClickView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        """
        We handle here the redirection, passing the user id of the asked customer
        """
        self.kwargs['user_id'] = form.cleaned_data['user_id']
        return super(LaunderetteMainClickView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """
        We handle here the login form for the barman
        """
        kwargs = super(LaunderetteMainClickView, self).get_context_data(**kwargs)
        kwargs['counter'] = self.object.counter
        kwargs['form'] = self.get_form()
        kwargs['barmen'] = [self.request.user]
        if 'last_basket' in self.request.session.keys():
            kwargs['last_basket'] = self.request.session.pop('last_basket', None)
            kwargs['last_customer'] = self.request.session.pop('last_customer', None)
            kwargs['last_total'] = self.request.session.pop('last_total', None)
            kwargs['new_customer_amount'] = self.request.session.pop('new_customer_amount', None)
        return kwargs

    def get_success_url(self):
        return reverse_lazy('launderette:click', args=self.args, kwargs=self.kwargs)

class ClickTokenForm(forms.BaseForm):
    def clean(self):
        with transaction.atomic():
            operator = Subscriber.objects.filter(id=self.operator_id).first()
            customer = Customer.objects.filter(user__id=self.subscriber_id).first()
            counter = Counter.objects.filter(id=self.counter_id).first()
            subscriber = get_subscriber(customer.user)
            self.last_basket = {
                    'last_basket': [],
                    'last_customer': customer.user.get_display_name(),
                    }
            total = 0
            for k,t in self.cleaned_data.items():
                if t is not None:
                    slot_id = int(k[5:])
                    slot = Slot.objects.filter(id=slot_id).first()
                    slot.token = t
                    slot.save()
                    t.user = subscriber
                    t.borrow_date = datetime.now().replace(tzinfo=pytz.UTC)
                    t.save()
                    price = settings.SITH_LAUNDERETTE_PRICES[t.type]
                    s = Selling(label="Jeton "+t.get_type_display()+" N°"+t.name, product=None, counter=counter, unit_price=price,
                            quantity=1, seller=operator, customer=customer)
                    s.save()
                    total += price
                    self.last_basket['last_basket'].append("Jeton "+t.get_type_display()+" N°"+t.name)
            self.last_basket['new_customer_amount'] = str(customer.amount)
            self.last_basket['last_total'] = str(total)
        return self.cleaned_data

class LaunderetteClickView(CanEditMixin, DetailView, BaseFormView):
    """The click page of the launderette"""
    model = Launderette
    pk_url_kwarg = "launderette_id"
    template_name = 'launderette/launderette_click.jinja'

    def get_form_class(self):
        fields = OrderedDict()
        kwargs = {}
        def clean_field_factory(field_name, slot):
            def clean_field(self2):
                t_name = str(self2.data[field_name])
                if t_name != "":
                    t = Token.objects.filter(name=str(self2.data[field_name]), type=slot.type, launderette=self.object,
                            user=None).first()
                    if t is None:
                        raise forms.ValidationError(_("Token not found"))
                    return t
            return clean_field
        for s in self.subscriber.slots.filter(token=None).all():
            field_name = "slot-%s" % (str(s.id))
            fields[field_name] = forms.CharField(max_length=5, required=False,
                    label="%s - %s" % (s.get_type_display(), defaultfilters.date(s.start_date, "j N Y H:i")))
            # XXX l10n settings.DATETIME_FORMAT didn't work here :/
            kwargs["clean_"+field_name] = clean_field_factory(field_name, s)
        kwargs['subscriber_id'] = self.subscriber.id
        kwargs['counter_id'] = self.object.counter.id
        kwargs['operator_id'] = self.operator.id
        kwargs['base_fields'] = fields
        return type('ClickForm', (ClickTokenForm,), kwargs)

    def get(self, request, *args, **kwargs):
        """Simple get view"""
        self.customer = Customer.objects.filter(user__id=self.kwargs['user_id']).first()
        self.subscriber = get_subscriber(self.customer.user)
        self.operator = request.user
        return super(LaunderetteClickView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """ Handle the many possibilities of the post request """
        self.object = self.get_object()
        self.customer = Customer.objects.filter(user__id=self.kwargs['user_id']).first()
        self.subscriber = get_subscriber(self.customer.user)
        self.operator = request.user
        return super(LaunderetteClickView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        """
        We handle here the redirection, passing the user id of the asked customer
        """
        self.request.session.update(form.last_basket)
        return super(LaunderetteClickView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """
        We handle here the login form for the barman
        """
        kwargs = super(LaunderetteClickView, self).get_context_data(**kwargs)
        if 'form' not in kwargs.keys():
            kwargs['form'] = self.get_form()
        kwargs['counter'] = self.object.counter
        kwargs['customer'] = self.customer
        return kwargs

    def get_success_url(self):
        self.kwargs.pop('user_id', None)
        return reverse_lazy('launderette:main_click', args=self.args, kwargs=self.kwargs)



class MachineEditView(CanEditPropMixin, UpdateView):
    """Edit a machine"""
    model = Machine
    pk_url_kwarg = "machine_id"
    fields = ['name', 'launderette', 'type', 'is_working']
    template_name = 'core/edit.jinja'

class MachineDeleteView(CanEditPropMixin, DeleteView):
    """Edit a machine"""
    model = Machine
    pk_url_kwarg = "machine_id"
    template_name = 'core/delete_confirm.jinja'
    success_url = reverse_lazy('launderette:launderette_list')

class MachineCreateView(CanCreateMixin, CreateView):
    """Create a new machine"""
    model = Machine
    fields = ['name', 'launderette', 'type']
    template_name = 'core/create.jinja'

    def get_initial(self):
        ret = super(MachineCreateView, self).get_initial()
        if 'launderette' in self.request.GET.keys():
            obj = Launderette.objects.filter(id=int(self.request.GET['launderette'])).first()
            if obj is not None:
                ret['launderette'] = obj.id
        return ret


