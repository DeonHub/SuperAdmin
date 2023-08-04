from django.contrib import admin
from .models import *


# Register your models here.
@admin.register( 
    Modules,
    ModuleFee,
    AccountSubscription,
    ActivityLog,
    MembershipSizes,
    Subscriptions,
    PaymentDetails,
    ServiceFee,
    TuakaUsers,
    Verifications,
    UnitedOrganizations,
    ClientSizes,
    Agents,
    AgentClients,
    ActivationFee,
    AccountSubscriptionCopy,
    EmailDetails,
    AgentsCommission,
    TotalCommission,
    )

class AppAdmin(admin.ModelAdmin):
    pass