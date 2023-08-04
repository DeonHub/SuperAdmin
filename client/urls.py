# from django import views
from django.urls import path
from . import views


app_name = 'client'

urlpatterns = [
    path('', views.index, name="index"),
    path('reset-password/', views.resetPassword, name="resetPassword"),
    path('register/<str:usercode>/', views.clientRegistration, name="clientRegistration"),

    path('register-client/', views.registerClient, name="registerClient"),
    path('view-clients/', views.viewClients, name="viewClients"),
    path('view-client/<str:client_id>/', views.viewClient, name='viewClient'),


    # path('delete-module/<int:id>', views.deleteModule, name='deleteModule'),


    # path('create-membership-size/', views.createMembershipSize, name="createMembershipSize"),
    # path('view-membership-sizes/', views.viewMembershipSizes, name="viewMembershipSizes"),
    # path('edit-membership-size/<int:id>', views.editMembershipSize, name='editMembershipSize'),
    # path('delete-membership-size/<int:id>', views.deleteMembershipSize, name='deleteMembershipSize'),

    path('ajax/load-items/', views.load_items, name='ajax_load_items'),
    path('ajax/load-time/', views.load_time, name='ajax_load_time'),
    path('ajax/load-modules/', views.load_modules, name='ajax_load_modules'),

    path('ajax/load-expired/', views.load_expired, name='ajax_load_expired'),
    
    path('ajax/load-amount/', views.load_amount, name='ajax_load_amount'),

    path('ajax/load-districts/', views.load_districts, name='ajax_load_districts'),
    path('ajax/load-constituencies/', views.load_constituencies, name='ajax_load_constituencies'),
    path('ajax/load-sizes/', views.load_sizes, name='ajax_load_sizes'),
    path('ajax/load-size/', views.load_size, name='ajax_load_size'),

    path('ajax/load-bill/', views.load_bill, name='ajax_load_bill'),


    # path('subscription-history/', views.subscriptionHistory, name="subscriptionHistory"),
    path('subscription-history/', views.subscriptionHistory, name="subscriptionHistory"),
    path('account-subscription/', views.accountSubscription, name="accountSubscription"),
    path('subscription-extension/<int:id>/', views.subscriptionExtension, name="subscriptionExtension"),
    path('subscription-renewal/<int:id>/', views.subscriptionRenewal, name="subscriptionRenewal"),
    path('delete-subscription/<int:id>/', views.deleteSubscription, name='deleteSubscription'),


    # path('redirect-home/', views.redirectView, name="redirectView"),
    path('logout/<str:id>', views.logout, name='logout'),
    
    # path('special-subscription/', views.specialSubscription, name="specialSubscription"),

    path('view-module-fees/', views.viewModuleFees, name="viewModuleFees"),
    path('edit-module-fee/<int:id>/', views.editModuleFees, name='editModuleFees'),


    path('view-profile/', views.viewProfile, name="viewProfile"),


    path('view-activation/', views.viewActivation, name="viewActivation"),
    path('view-commission/', views.viewCommissions, name="viewCommissions"),
    path('edit-activation-fee/<int:id>/', views.editActivation, name='editActivation'),


    # path('special-history/', views.specialSubscriptionHistory, name="specialSubscriptionHistory"),
    # path('special-subscription/', views.specialSubscription, name="specialSubscription"),
    # path('delete-special-module-fee/<int:id>', views.deleteSpecialModuleFee, name='deleteSpecialModuleFee'),



    # path('fee-plan-csv/', views.fee_plan_csv, name="fee_plan_csv"),



]



