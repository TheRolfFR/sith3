from ajax_select import register, LookupChannel

from core.views.site import search_user
from core.models import User, Group
from club.models import Club
from counter.models import Product, Counter
from accounting.models import ClubAccount, Company

@register('users')
class UsersLookup(LookupChannel):
    model = User

    def get_query(self, q, request):
        return search_user(q)

    def format_match(self, obj):
        return obj.get_mini_item()

    def format_item_display(self, item):
        return item.get_display_name()

@register('groups')
class GroupsLookup(LookupChannel):
    model = Group

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q)[:50]

    def format_match(self, obj):
        return obj.name

    def format_item_display(self, item):
        return item.name

@register('clubs')
class ClubLookup(LookupChannel):
    model = Club

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q)[:50]

    def format_match(self, obj):
        return obj.name

    def format_item_display(self, item):
        return item.name

@register('counters')
class CountersLookup(LookupChannel):
    model = Counter

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q)[:50]

    def format_item_display(self, item):
        return item.name

@register('products')
class ProductsLookup(LookupChannel):
    model = Product

    def get_query(self, q, request):
        return (self.model.objects.filter(name__icontains=q) | self.model.objects.filter(code__icontains=q))[:50]

    def format_item_display(self, item):
        return item.name

@register('club_accounts')
class ClubAccountLookup(LookupChannel):
    model = ClubAccount

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q)[:50]

    def format_item_display(self, item):
        return item.name

@register('companies')
class CompaniesLookup(LookupChannel):
    model = Company

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q)[:50]

    def format_item_display(self, item):
        return item.name
