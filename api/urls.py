from django.urls import include, path, re_path
# from api import context_processors
from rest_framework import routers
from . import views

# router = routers.DefaultRouter()
# # router.register(r'heroes', views.HeroViewSet)
# # router.register(r'villains', views.VillainViewSet)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Superadmin API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('sizes/', views.GetSizes.as_view(), name="login"),
    path('membership-size/', views.AddMembershipSize.as_view(), name="membership_size"),
    
    
    path('size/<str:client_id>/', views.GetSize.as_view(), name="get-size"),
    path('limit/<str:client_id>/', views.GetLimit.as_view(), name="get-limit"),
    
    path('modules/', views.GetModules.as_view(), name="modules"),
    path('united-organizations/', views.GetUnitedOrganizations.as_view(), name="united_organizations"),
    path('modules/<str:module_id>', views.GetModule.as_view(), name="modules"),

    path('get-app/<str:token>/', views.GetApp.as_view(), name="get_app"),

    path('service-fee/<str:client_id>/', views.GetServiceFee.as_view(), name="service_fee"),
    path('outstanding-service-fee/', views.OutstandingServiceFee.as_view(), name="outstanding_service_fee"),



    path('get-client-database/<str:client_id>/', views.GetDatabaseDetails.as_view(), name="database"),
    path('client-email/<str:client_id>/', views.GetClientEmailDetails.as_view(), name="client_email_details"),
    path('client-payment/<str:client_id>/', views.GetClientPaymentDetails.as_view(), name="client_payment_details"),



    path('client-activation/<str:client_id>/', views.ClientActivation.as_view(), name="activation"),
    path('subscribed-modules/<str:client_id>/', views.GetSubscribedModules.as_view(), name="subscribed_modules"),
    path('pay-client-activation/<str:client_id>/', views.PayOneTime.as_view(), name="pay_activation"),



    path('activation-fee/<str:membership_size>/', views.GetActivation.as_view(), name="activation"),



    path('validate-code/<str:usercode>/', views.ValidateCode.as_view(), name="validate_code"),
    path('register-user/', views.RegisterUser.as_view(), name="register_user"),
    path('verify-user/', views.VerifyUser.as_view(), name="verify_user"),
    path('reset-code/', views.ResetCode.as_view(), name="reset_code"),
    path('member-details/<str:usercode>/', views.GetMemberDetails.as_view(), name="member_details"),
    
    # path('clients/', views.GetClients.as_view(), name="clients"),
    # path('validate-token/', views.ValidateToken.as_view(), name="token"),
    # path('signup/', views.SignUp.as_view(), name="signup"),
    # path('add-modules/', views.AddSubscribedModules.as_view(), name="add_modules"),
    # path('client-size/', views.GetClientSize.as_view(), name="client-size"),


                                                               
    # path('total/', views.GetTotal.as_view(), name="total"),
    # path('fee-types/', views.GetFeeTypes.as_view(), name="fee_types"),
    # path('members/', views.GetMembers.as_view(), name="fee_types"),

    
    # path('payment-history/', views.GetPaymentHistory.as_view(), name="payment_history"),
    # path('assigned-fees/', views.GetAssignedFees.as_view(), name="assigned_fees"),
    # path('make-payment/<int:id>', views.MakeFeePayment.as_view(), name="pay_fee"),
    path('renew-subscription/token=<str:token>/', views.ClientSubscription.as_view(), name="pay_subs"),
    # path('subscribers/', views.GetSubscribers.as_view(), name="subs"),



    re_path('swagger', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # path('assigned-fees/token', views.GetAssignedFees.as_view({'post':'post_token'})),
    

    # path('total-paid/', views.TotalPaid.as_view(), name="total_paid"),

    # path('list/<int:pk>', views.HeroDetails.as_view(), name="heros"),
    # path('members/', views.members, name="members"),
]