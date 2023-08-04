# from django import views
from django.urls import path, re_path
from . import views


app_name = 'user'

urlpatterns = [
    path('', views.index, name="index"),


    path('ajax/load-items/', views.load_items, name='ajax_load_items'),
    path('ajax/load-time/', views.load_time, name='ajax_load_time'),
    path('ajax/load-modules/', views.load_modules, name='ajax_load_modules'),

    path('ajax/load-expired/', views.load_expired, name='ajax_load_expired'),
    
    path('ajax/load-amount/', views.load_amount, name='ajax_load_amount'),

    path('ajax/load-sizes/', views.load_sizes, name='ajax_load_sizes'),
    path('ajax/load-size/', views.load_size, name='ajax_load_size'),

    path('ajax/load-bill/', views.load_bill, name='ajax_load_bill'),

    # re_path(r'^user/subscription-history/(?P<id>[\w-]+)/?$')

    path('subscription-history/<str:token>/', views.subscriptionHistory, name='subscriptionHistory'),
    path('account-subscription/<str:token>/', views.accountSubscription, name="accountSubscription"),
    path('subscription-extension/<str:token>/<str:id>/', views.subscriptionExtension, name="subscriptionExtension"),
    path('subscription-renewal/<str:token>/<int:id>/', views.subscriptionRenewal, name="subscriptionRenewal"),
    path('delete-subscription/<str:token>/<int:id>/', views.deleteSubscription, name='deleteSubscription'),
    path('cancel-subscription/<str:module_id>/<int:subscription_id>/', views.cancelSubscription, name='cancelSubscription'),

    # path('redirect-home/', views.redirectView, name="redirectView"),
    path('logout/', views.logout, name='logout'),


    path('view-profile/<str:token>/', views.viewProfile, name="viewProfile"),


]



