# -*- coding:utf-8 -*
#
# Copyright 2016,2017
# - Skia <skia@libskia.so>
# - Sli <antoine@bartuccio.fr>
#
# Ce fichier fait partie du site de l'Association des Étudiants de l'UTBM,
# http://ae.utbm.fr.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License a published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Sofware Foundation, Inc., 59 Temple
# Place - Suite 330, Boston, MA 02111-1307, USA.
#
#

from django.utils.translation import ugettext as _
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.urls import reverse
from django import forms
from django.core.exceptions import PermissionDenied

from ajax_select.fields import AutoCompleteSelectField

from core.views import CanEditPropMixin
from core.models import User, OperationLog
from counter.models import Customer

from forum.models import ForumMessageMeta


def merge_users(u1, u2):
    u1.nick_name = u1.nick_name or u2.nick_name
    u1.date_of_birth = u1.date_of_birth or u2.date_of_birth
    u1.home = u1.home or u2.home
    u1.sex = u1.sex or u2.sex
    u1.pronouns = u1.pronouns or u2.pronouns
    u1.tshirt_size = u1.tshirt_size or u2.tshirt_size
    u1.role = u1.role or u2.role
    u1.department = u1.department or u2.department
    u1.dpt_option = u1.dpt_option or u2.dpt_option
    u1.semester = u1.semester or u2.semester
    u1.quote = u1.quote or u2.quote
    u1.school = u1.school or u2.school
    u1.promo = u1.promo or u2.promo
    u1.forum_signature = u1.forum_signature or u2.forum_signature
    u1.second_email = u1.second_email or u2.second_email
    u1.phone = u1.phone or u2.phone
    u1.parent_phone = u1.parent_phone or u2.parent_phone
    u1.address = u1.address or u2.address
    u1.parent_address = u1.parent_address or u2.parent_address
    u1.save()
    for u in u2.godfathers.all():
        u1.godfathers.add(u)
    u1.save()
    for i in u2.invoices.all():
        for f in i._meta.local_fields:  # I have sadly not found anything better :/
            if f.name == "date":
                f.auto_now = False
        u1.invoices.add(i)
    u1.save()
    s1 = User.objects.filter(id=u1.id).first()
    s2 = User.objects.filter(id=u2.id).first()
    for s in s2.subscriptions.all():
        s1.subscriptions.add(s)
    s1.save()
    c1 = Customer.objects.filter(user__id=u1.id).first()
    c2 = Customer.objects.filter(user__id=u2.id).first()
    if c1 and c2:
        for r in c2.refillings.all():
            c1.refillings.add(r)
        c1.save()
        for s in c2.buyings.all():
            c1.buyings.add(s)
        c1.save()
    elif c2 and not c1:
        c2.user = u1
        c1 = c2
        c1.save()
    c1.recompute_amount()
    u2.delete()
    return u1


def delete_all_forum_user_messages(user, moderator, verbose=False):
    """
        Create a ForumMessageMeta that says a forum
            message is deleted on every forum message of an user
        user: the user to delete messages from
        moderator: the one marked as the moderator
    """
    for message in user.forum_messages.all():
        if message.is_deleted():
            continue

        if verbose:
            print(message)
        ForumMessageMeta(message=message, user=moderator, action="DELETE").save()


class MergeForm(forms.Form):
    user1 = AutoCompleteSelectField(
        "users", label=_("User that will be kept"), help_text=None, required=True
    )
    user2 = AutoCompleteSelectField(
        "users", label=_("User that will be deleted"), help_text=None, required=True
    )


class SelectUserForm(forms.Form):
    user = AutoCompleteSelectField(
        "users", label=_("User to be selected"), help_text=None, required=True
    )


class MergeUsersView(FormView):
    template_name = "rootplace/merge.jinja"
    form_class = MergeForm

    def dispatch(self, request, *arg, **kwargs):
        res = super(MergeUsersView, self).dispatch(request, *arg, **kwargs)
        if request.user.is_root:
            return res
        raise PermissionDenied

    def form_valid(self, form):
        self.final_user = merge_users(
            form.cleaned_data["user1"], form.cleaned_data["user2"]
        )
        return super(MergeUsersView, self).form_valid(form)

    def get_success_url(self):
        return reverse("core:user_profile", kwargs={"user_id": self.final_user.id})


class DeleteAllForumUserMessagesView(FormView):
    """
        Delete all forum messages from an user
        Messages are soft deleted and are still visible from admins
        GUI frontend to the dedicated command
    """

    template_name = "rootplace/delete_user_messages.jinja"
    form_class = SelectUserForm

    def dispatch(self, request, *args, **kwargs):
        res = super(DeleteAllForumUserMessagesView, self).dispatch(
            request, *args, **kwargs
        )
        if request.user.is_root:
            return res
        raise PermissionDenied

    def form_valid(self, form):
        self.user = form.cleaned_data["user"]
        delete_all_forum_user_messages(self.user, self.request.user)
        return super(DeleteAllForumUserMessagesView, self).form_valid(form)

    def get_success_url(self):
        return reverse("core:user_profile", kwargs={"user_id": self.user.id})


class OperationLogListView(ListView, CanEditPropMixin):
    """
    List all logs
    """

    model = OperationLog
    template_name = "rootplace/logs.jinja"
    ordering = ["-date"]
    paginate_by = 100
