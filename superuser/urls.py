# from django import views
from django.urls import path
from . import views


app_name = 'superuser'

urlpatterns = [
    path('', views.index, name="index"),


    path('ajax/load-districts/', views.load_districts, name='ajax_load_districts'),
    path('ajax/load-constituencies/', views.load_constituencies, name='ajax_load_constituencies'),
    path('ajax/load-sizes/', views.load_sizes, name='ajax_load_sizes'),

    path('create-agent/', views.createAgent, name="createAgent"),
    path('view-agents/', views.viewAgents, name="viewAgents"),
    path('edit-agent/<str:id>', views.editAgent, name='editAgent'),
    path('view-agent/<str:id>', views.viewAgent, name='viewAgent'),
    path('delete-agent/<str:id>', views.deleteAgent, name='deleteAgent'),
    

    path('create-module/', views.createModule, name="createModule"),
    path('view-modules/', views.viewModules, name="viewModules"),
    path('edit-module/<int:id>', views.editModule, name='editModule'),
    path('view-module/<int:id>', views.viewModule, name='viewModule'),
    path('delete-module/<int:id>', views.deleteModule, name='deleteModule'),


    path('create-payment-details/', views.createPaymentDetails, name="createPaymentDetails"),
    path('view-payment-details/', views.viewPaymentDetails, name="viewPaymentDetails"),
    path('edit-payment-details/<int:id>', views.editPaymentDetails, name='editPaymentDetails'),
    path('delete-payment-details/<int:id>', views.deletePaymentDetails, name='deletePaymentDetails'),



    path('create-client-size/', views.createClientsize, name="createClientsize"),
    path('view-client-sizes/', views.viewClientsizes, name="viewClientsizes"),
    path('edit-client-size/<int:id>/', views.editClientsize, name='editClientsize'),
    path('delete-client-size/<int:id>/', views.deleteClientsize, name='deleteClientsize'),



    path('create-email-details/', views.createEmailDetails, name="createEmailDetails"),
    path('view-email-details/', views.viewEmailDetails, name="viewEmailDetails"),
    path('edit-email-details/<int:id>', views.editEmailDetails, name='editEmailDetails'),
    path('delete-email-details/<int:id>', views.deleteEmailDetails, name='deleteEmailDetails'),


    path('create-united-organization/', views.createUnitedOrganization, name="createUnitedOrganization"),
    path('view-united-organizations/', views.viewUnitedOrganizations, name="viewUnitedOrganizations"),
    path('delete-united-organization/<int:id>', views.deleteUnitedOrganization, name='deleteUnitedOrganization'),


    path('create-service-fees/', views.createServiceFees, name="createServiceFees"),
    path('view-service-fees/', views.viewServiceFees, name="viewServiceFees"),
    path('edit-service-fees/<int:id>', views.editServiceFees, name='editServiceFees'),
    path('delete-service-fees/<int:id>', views.deleteServiceFees, name='deleteServiceFees'),


    path('activate-client/', views.activateClient, name="activateClient"),


    path('set-activation-fee/', views.setActivation, name="setActivation"),
    path('view-activation/', views.viewActivation, name="viewActivation"),
    path('edit-activation-fee/<int:id>', views.editActivation, name='editActivation'),
    path('delete-activation-fee/<int:id>', views.deleteActivation, name='deleteActivation'),

    
    

    path('create-membership-size/', views.createMembershipSize, name="createMembershipSize"),
    path('view-membership-sizes/', views.viewMembershipSizes, name="viewMembershipSizes"),
    path('edit-membership-size/<int:id>', views.editMembershipSize, name='editMembershipSize'),
    path('delete-membership-size/<int:id>', views.deleteMembershipSize, name='deleteMembershipSize'),



    path('ajax/load-items/', views.load_items, name='ajax_load_items'),
    path('ajax/load-onetime/', views.load_onetime, name='ajax_load_onetime'),
    path('ajax/load-commission/', views.load_commission, name='ajax_load_commission'),
    path('ajax/load-archive/', views.load_archive, name='ajax_load_archive'),
    
    path('ajax/load-exchange/', views.load_exchange, name='ajax_load_exchange'),
    path('ajax/load-sizes/', views.load_sizes, name='ajax_load_sizes'),
    path('ajax/load-size/', views.load_size, name='ajax_load_size'),

    path('ajax/load-modulo/', views.load_modulo, name='ajax_load_modulo'),
    path('ajax/load-modula/', views.load_modula, name='ajax_load_modula'),

    path('ajax/load-time/', views.load_time, name='ajax_load_time'),
    path('ajax/load-expired/', views.load_expired, name='ajax_load_expired'),
    path('ajax/load-modules/', views.load_modules, name='ajax_load_modules'),

    path('ajax/load-amount/', views.load_amount, name='ajax_load_amount'),
    path('ajax/load-cost/', views.load_cost, name='ajax_load_cost'),


    path('subscription-history/', views.subscriptionHistory, name="subscriptionHistory"),
    path('account-subscription/', views.accountSubscription, name="accountSubscription"),
    path('subscription-extension/<int:id>/', views.subscriptionExtension, name="subscriptionExtension"),
    path('subscription-renewal/<int:id>/', views.subscriptionRenewal, name="subscriptionRenewal"),
    path('delete-subscription/<int:id>/', views.deleteSubscription, name='deleteSubscription'),




    path('view-commissions/', views.viewCommissions, name="viewCommissions"),
    path('view-profile/', views.viewProfile, name="viewProfile"),

    path('set-module-fees/', views.setModuleFees, name="setModuleFees"),
    path('view-module-fees/', views.viewModuleFees, name="viewModuleFees"),
    path('edit-module-fee/<int:id>', views.editModuleFees, name='editModuleFees'),
    path('delete-module-fee/<int:id>', views.deleteModuleFee, name='deleteModuleFee'),




    path('special-history/', views.specialSubscriptionHistory, name="specialSubscriptionHistory"),
    path('special-subscription/', views.specialSubscription, name="specialSubscription"),
    
    path('delete-special-module-fee/<int:id>', views.deleteSpecialModuleFee, name='deleteSpecialModuleFee'),


    path('register-client/', views.registerClient, name="registerClient"),


    path('clients-data/', views.allClients, name="allClients"),
    path('archived-clients/', views.archivedClients, name="archivedClients"),

    path('view-client/<str:client_id>/', views.viewClient, name='viewClient'),

    path('fee-plan-csv/', views.fee_plan_csv, name="fee_plan_csv"),

    path('logout/<str:id>', views.logout, name='logout'),

]



