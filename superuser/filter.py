import django_filters
from django_filters import DateFilter, CharFilter
from .models import *


# class AssignPaymentDurationFilter(django_filters.FilterSet):
#     member = CharFilter(field_name='member', lookup_expr='icontains')
#     branch = CharFilter(field_name='branch', lookup_expr='icontains')
#     member_category = CharFilter(field_name='member_category', lookup_expr='icontains')
#     group = CharFilter(field_name='group', lookup_expr='icontains')
#     subgroup = CharFilter(field_name='subgroup', lookup_expr='icontains')
#     start_date = DateFilter(field_name='start_date', lookup_expr='gte')
#     end_date = DateFilter(field_name='end_date', lookup_expr='lte')

#     class Meta:
#         model = AssignPaymentDuration
#         fields = ['fee_type']

   

class SubscriptionFilter(django_filters.FilterSet):
    client = CharFilter(field_name='client', lookup_expr='icontains')

    start_date = DateFilter(field_name='start_date', lookup_expr='gte')
    end_date = DateFilter(field_name='end_date', lookup_expr='lte')

    # date_created = DateFilter(field_name='date_created', lookup_expr='lte')


    class Meta:
        model = AccountSubscription
        fields = [ 'submodules' , 'date_created']



class SpecialSubscriptionFilter(django_filters.FilterSet):
    client = CharFilter(field_name='client', lookup_expr='icontains')

    start_date = DateFilter(field_name='start_date', lookup_expr='gte')
    end_date = DateFilter(field_name='end_date', lookup_expr='lte')

    # date_created = DateFilter(field_name='date_created', lookup_expr='lte')


    class Meta:
        model = SpecialModuleFee
        fields = [ 'submodules' , 'date_created', 'client']


class SetFeeFilter(django_filters.FilterSet):
    subscription_type = CharFilter(field_name='subscription_type', lookup_expr='icontains')

    class Meta:
        model = ModuleFee
        fields = ['module'] 


   
