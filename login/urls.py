# from django import views
from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.login, name="login"),
    path('verify-email/', views.verifyEmail, name="verifyEmail"),
    path('verify-code/', views.verifyCode, name="verifyCode"),
    path('change-password/<str:code>/', views.changePassword, name="changePassword"),


    # path('tester/', views.tester, name="tester"),

    # path('create-module/', views.createModule, name="createModule"),
    # path('view-modules/', views.viewModules, name="viewModules"),
    # path('edit-module/<int:id>', views.editModule, name='editModule'),
    # path('view-module/<int:id>', views.viewModule, name='viewModule'),
    # path('delete-module/<int:id>', views.deleteModule, name='deleteModule'),
    

    # path('create-payment-details/', views.createPaymentDetails, name="createPaymentDetails"),
    # path('view-payment-details/', views.viewPaymentDetails, name="viewPaymentDetails"),
    # path('edit-payment-details/<int:id>', views.editPaymentDetails, name='editPaymentDetails'),
    # path('delete-payment-details/<int:id>', views.deletePaymentDetails, name='deletePaymentDetails'),


    # path('create-membership-size/', views.createMembershipSize, name="createMembershipSize"),
    # path('view-membership-sizes/', views.viewMembershipSizes, name="viewMembershipSizes"),
    # path('edit-membership-size/<int:id>', views.editMembershipSize, name='editMembershipSize'),
    # path('delete-membership-size/<int:id>', views.deleteMembershipSize, name='deleteMembershipSize'),



    # path('ajax/load-items/', views.load_items, name='ajax_load_items'),
    # path('ajax/load-size/', views.load_size, name='ajax_load_size'),
    
    # path('ajax/load-modulo/', views.load_modulo, name='ajax_load_modulo'),
    # path('ajax/load-modula/', views.load_modula, name='ajax_load_modula'),

    # path('ajax/load-time/', views.load_time, name='ajax_load_time'),
    # path('ajax/load-amount/', views.load_amount, name='ajax_load_amount'),
    # path('ajax/load-cost/', views.load_cost, name='ajax_load_cost'),


    # path('subscription-history/', views.subscriptionHistory, name="subscriptionHistory"),
    # path('module-subscription/', views.accountSubscription, name="accountSubscription"),
    # path('cancel-subscription/<int:id>', views.deleteSubscription, name='deleteSubscription'),

    # # path('special-subscription/', views.specialSubscription, name="specialSubscription"),

    # path('set-module-fees/', views.setModuleFees, name="setModuleFees"),
    # path('view-module-fees/', views.viewModuleFees, name="viewModuleFees"),
    # path('delete-module-fee/<int:id>', views.deleteModuleFee, name='deleteModuleFee'),




    # path('special-history/', views.specialSubscriptionHistory, name="specialSubscriptionHistory"),
    # path('special-subscription/', views.specialSubscription, name="specialSubscription"),
    
    # path('delete-special-module-fee/<int:id>', views.deleteSpecialModuleFee, name='deleteSpecialModuleFee'),



    # path('fee-plan-csv/', views.fee_plan_csv, name="fee_plan_csv"),



]



