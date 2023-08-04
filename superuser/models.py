from django.db import models
from jsonfield import JSONField
from django.utils import timezone


# Create your models here.
class Modules(models.Model):
    module = models.CharField(max_length= 100)
    description = models.CharField(max_length= 500)
    default = models.BooleanField(default=False, null=True)
    logo = models.ImageField(blank=True, null=True, upload_to='logo-uploads/', default='')
    assigned_fee = models.IntegerField(null=True, default=0)
    link = models.CharField(max_length= 500, default="https://google.com")
    icon = models.CharField(max_length= 500, default="description")
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f'{self.module}'


class MembershipSizes(models.Model):
    size = models.CharField(max_length= 100)
    unit_cost_usd = models.IntegerField(null=True, default=0)
    unit_cost_ghs = models.IntegerField(null=True, default=0)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.size



class ClientSizes(models.Model):
    client_id = models.CharField(max_length= 100)
    pid = models.CharField(max_length= 100)
    client_name = models.CharField(max_length= 100)    
    size = models.CharField(max_length= 100)
    client_size = models.ForeignKey(MembershipSizes, on_delete= models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f'{self.client_name} - {self.client_size}'



class ModuleFee(models.Model):
    subscription_type = models.CharField(max_length= 100)
    duration = models.IntegerField(null=True, default=0)

    module = models.ForeignKey(Modules, on_delete= models.SET_NULL, null=True)
    client_size = models.ForeignKey(MembershipSizes, on_delete= models.SET_NULL, null=True)

    module_name = models.CharField(max_length= 20, default="None")
    membership_size = models.CharField(max_length= 20, default="None")

    unit_fee_usd = models.FloatField(null=True, default=0.00)
    unit_fee_ghs = models.FloatField(null=True, default=0.00)


    respective_increase = models.IntegerField(null=True, default=0)

    promo = models.BooleanField(default=False, null=True)
    promo_discount = models.IntegerField(null=True, default=0)
    discount_amount_usd = models.FloatField(null=True, default=0.00)
    discount_amount_ghs = models.FloatField(null=True, default=0.00)
    promo_duration = models.IntegerField(null=True, default=0)
    promo_membership_size = models.CharField(max_length= 20, default="None")
    created_by = models.CharField(max_length= 20, default="Admin")
    amount_to_be_paid_usd = models.FloatField(null=True, default=0.00)
    amount_to_be_paid_ghs = models.FloatField(null=True, default=0.00)

    agent_cost = JSONField(null=True, default=dict)

    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f'{self.module} at an amount of {self.unit_fee_usd}'



class PaymentDetails(models.Model):
    client_id = models.CharField(max_length= 100)
    client_name = models.CharField(max_length= 100)
    merchant_account_number = models.CharField(max_length=100, default="2017254")
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f'{self.client_name} payment details'


class ActivationFee(models.Model):
    membership_size = models.ForeignKey(MembershipSizes, on_delete= models.SET_NULL, null=True)
    activation_fee = models.FloatField(null= True, default=0.00)
    agent_cost = JSONField(null=True, default=dict)
    duration = models.IntegerField(null=True, default=0)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f'{self.membership_size} - {self.activation_fee}'



class SpecialModuleFee(models.Model):
    subscription_type = models.CharField(max_length= 100)
    duration = models.IntegerField(null=True, default=0)
    sub_duration = models.IntegerField(null=True, default=0)
    client = models.CharField(max_length= 100)

    submodules = models.ManyToManyField(Modules)
    module_name = models.CharField(max_length= 20, default="None")
    membership_size = models.CharField(max_length= 20, default="None")
    renewing_days = models.IntegerField(null=True, default=0)
    remaining_days = models.IntegerField(null=True, default=0)
    expired_days = models.IntegerField(null=True, default=0)
    promo = models.BooleanField(default=False, null=True)
    description = models.CharField(max_length= 100, default="None")

    promo_discount = models.IntegerField(null=True, default=0)
    created_by = models.CharField(max_length= 20, default="Admin")
    amount_to_be_paid_usd = models.FloatField(null=True, default=0.00)
    amount_to_be_paid_ghs = models.FloatField(null=True, default=0.00)
    invoice_no = models.CharField(max_length= 100, default="ASP20220003", null=True)
    expires_on = models.DateField( default=timezone.now )
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f'{self.client} at an amount of {self.amount_to_be_paid_usd}'



class AccountSubscription(models.Model):
    client_id = models.CharField(max_length= 100, default="1")
    client = models.CharField(max_length= 100, null=True, default="None")
    submodules = models.ManyToManyField(Modules)

    modules = JSONField(null=True, default=dict)
    membership_size = models.CharField(max_length= 20)
    description = models.CharField(max_length= 100, default="None")
    duration = models.IntegerField(null=True, default=0)
    amount_paid = models.IntegerField(null=True, default=0)
    renewing_days = models.IntegerField(null=True, default=0)
    remaining_days = models.IntegerField(null=True, default=0)
    expired_days = models.IntegerField(null=True, default=0)
    annual_maintenance_fee = models.FloatField(null=True, default=0.00)
    subscription_fee_usd = models.FloatField(null=True, default=0.00)
    subscription_fee_ghs = models.FloatField(null=True, default=0.00)
    paid_by = models.CharField(max_length= 100, default="Admin")
    invoice_no = models.CharField(max_length= 100, default="ASL0003", null=True)
    invoice_copy = models.CharField(max_length= 100, default="ASL0003", null=True)
    usercode = models.CharField(max_length= 100, default="ABC12345", null=True)
    expires_on = models.DateTimeField( default=timezone.now, null=True )
    confirmed = models.BooleanField(default=False, null=True)
    expired = models.BooleanField(default=False, null=True)
    special = models.BooleanField(default=False, null=True)
    non_expiry = models.BooleanField(default=False, null=True)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f'{self.client} subscribed on {self.date_created}, {self.expires_on}'



class AccountSubscriptionCopy(models.Model):
    client_id = models.CharField(max_length= 100, default="1")
    client = models.CharField(max_length= 100, null=True, default="None")
    # module = models.ForeignKey(Modules, on_delete= models.SET_NULL, null=True)
    submodules = models.ManyToManyField(Modules)

    modules = JSONField(null=True, default=dict)
    membership_size = models.CharField(max_length= 20)
    description = models.CharField(max_length= 100, default="None")
    duration = models.IntegerField(null=True, default=0)
    amount_paid = models.IntegerField(null=True, default=0)
    renewing_days = models.IntegerField(null=True, default=0)
    remaining_days = models.IntegerField(null=True, default=0)
    expired_days = models.IntegerField(null=True, default=0)
    subscription_fee_usd = models.FloatField(null=True, default=0.00)
    subscription_fee_ghs = models.FloatField(null=True, default=0.00)
    annual_maintenance_fee = models.FloatField(null=True, default=0.00)
    paid_by = models.CharField(max_length= 100, default="Admin")
    invoice_no = models.CharField(max_length= 100, default="ASL0003", null=True)
    invoice_copy = models.CharField(max_length= 100, default="ASL0003", null=True)
    usercode = models.CharField(max_length= 100, default="ABC12345", null=True)
    expires_on = models.DateTimeField( default=timezone.now, null=True )
    confirmed = models.BooleanField(default=False, null=True)
    expired = models.BooleanField(default=False, null=True)
    special = models.BooleanField(default=False, null=False)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f'{self.client} subscribed on {self.date_created}'



class Subscriptions(models.Model):
    client = models.CharField(max_length= 100)
    client_id = models.CharField(max_length= 100)
    subscription_id = models.CharField(max_length= 100)
    subscribed_modules = models.JSONField(null=True, default=dict)
    confirmed = models.BooleanField(default=False, null=True)
    date_created = models.DateField( auto_now_add= True)

    def __str__(self):
        return f'{self.client} subscribed with an id of {self.subscription_id}'



class ServiceFee(models.Model):
    client = models.CharField(max_length= 100)
    client_id = models.CharField(max_length= 100)
    service_fee = models.FloatField(null=True, default=0.00)
    limit = models.FloatField(null=True, default=0.00)
    outstanding_fee = models.FloatField(null=True, default=0.00)
    date_created = models.DateField(auto_now_add= True)

    def __str__(self):
        return f'{self.client} has an outstanding service fee({self.service_fee}) of {self.outstanding_fee}'



class EmailDetails(models.Model):
    client_name = models.CharField(max_length= 100)
    client_id = models.CharField(max_length= 100)
    email = models.CharField(max_length= 100)
    password = models.CharField(max_length= 100)
    date_created = models.DateField(auto_now_add= True)

    def __str__(self):
        return f'{self.client_name}'




class UnitedOrganizations(models.Model):
    client_name = models.CharField(max_length= 100)
    client_id = models.CharField(max_length= 100)
    date_created = models.DateField(auto_now_add= True)

    def __str__(self):
        return f'{self.client_name}'


class TuakaUsers(models.Model):
    firstname = models.CharField(max_length= 100, null=True)
    middlename = models.CharField(max_length= 100, null=True)
    surname = models.CharField(max_length= 100, null=True)
    email = models.CharField(max_length= 100, null=True)
    contact = models.CharField(max_length= 100, null=True)
    country = models.CharField(max_length= 100, null=True)
    usercode = models.CharField(max_length= 100, null=True)
    verified = models.BooleanField(default=False, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='profile-uploads/', default='profile.png')
    date_created = models.DateField(auto_now_add= True)

    def __str__(self):
        return f'{self.firstname} {self.surname}'


class Verifications(models.Model):
    firstname = models.CharField(max_length= 100, null=True)
    email = models.CharField(max_length= 100, null=True)
    contact = models.CharField(max_length= 100, null=True)
    code = models.CharField(max_length= 100, null=True)
    date_created = models.DateField(auto_now_add= True)

    def __str__(self):
        return f'{self.firstname} {self.code}'



class Agents(models.Model):
    pid = models.CharField(max_length=200, null=True, default=0)
    gender = models.IntegerField(null=True, default=1) 
    account_name = models.CharField(max_length=200, null=True, default="Demo Account")
    branch = models.CharField(max_length=200, null=True, default="Main")
    token = models.CharField(max_length=100, null=True)
    firstname = models.CharField(max_length= 100, null=True)
    surname = models.CharField(max_length= 100, null=True)
    fullname = models.CharField(max_length=100, null=True, default="None")
    email = models.CharField(max_length= 100, null=True)
    password = models.CharField(max_length= 100, null=True)
    contact = models.CharField(max_length= 100, null=True)
    account = models.CharField(max_length= 100, null=True)
    country = models.CharField(max_length= 100, null=True)
    usercode = models.CharField(max_length= 100, null=True)
    profile = models.ImageField(blank=True, null=True, upload_to='agents-profile-uploads/', default='profile.png')
    card = models.ImageField(blank=True, null=True, upload_to='agents-card-uploads/', default='profile.png')
    activation_commission = models.FloatField(null=True, default=0.00)
    renewal_commission = models.FloatField(null=True, default=0.00)
    link = models.CharField(max_length= 100, null=True)
    date_created = models.DateField(auto_now_add= True)

    def __str__(self):
        return f'{self.firstname} {self.surname}'



class AgentsCommission(models.Model):
    client_name = models.CharField(max_length= 100, null=True)
    client_id = models.CharField(max_length= 100, null=True)
    agent_name = models.CharField(max_length= 100, null=True)
    usercode = models.CharField(max_length= 100, null=True)
    commission = models.CharField(max_length= 100, null=True)
    amount = models.FloatField(null=True, default=0.00)
    paid = models.BooleanField(default=False, null=False)
    status = models.CharField(max_length= 100, null=True, default="Not paid")
    date_created = models.DateField(auto_now_add= True)

    def __str__(self):
        return f'{self.agent_name} earned {self.amount}'



class TotalCommission(models.Model):
    usercode = models.CharField(max_length= 100, null=True)
    amount = models.FloatField(null=True, default=0.00)
    paid = models.BooleanField(default=False, null=False)
    status = models.CharField(max_length= 100, null=True, default="Not paid")
    date_created = models.DateField(auto_now_add= True)

    def __str__(self):
        return f'{self.usercode} earned {self.amount}'



class AgentClients(models.Model):
    usercode = models.CharField(max_length= 100, null=True)
    agent_name = models.CharField(max_length= 100, null=True)

    client_id = models.CharField(max_length= 100, null=True)
    pid = models.CharField(max_length= 100, null=True)
    client_name = models.CharField(max_length= 100, null=True)
    account_name = models.CharField(max_length= 200, null=True)
    gender = models.IntegerField(null=True, default=1) 
    
    email = models.CharField(max_length= 100, null=True)
    contact = models.CharField(max_length= 100, null=True)
    size = models.CharField(max_length= 100)
    date_created = models.DateField(auto_now_add= True)
    
    # pid = models.CharField(max_length=200, null=True, default=0)
    # account_name = models.CharField(max_length=200, null=True, default="Demo Account")
    # branch = models.CharField(max_length=200, null=True, default="Main")
    # token = models.CharField(max_length=100, null=True)
    # firstname = models.CharField(max_length= 100, null=True)
    # surname = models.CharField(max_length= 100, null=True)
    # fullname = models.CharField(max_length=100, null=True, default="None")

    # account = models.CharField(max_length= 100, null=True)
    # country = models.CharField(max_length= 100, null=True)
    # profile = models.ImageField(blank=True, null=True, upload_to='agents-profile-uploads/', default='profile.png')
    # card = models.ImageField(blank=True, null=True, upload_to='agents-card-uploads/', default='profile.png')
    # activation_commission = models.FloatField(null=True, default=0.00)
    # renewal_commission = models.FloatField(null=True, default=0.00)
    # link = models.CharField(max_length= 100, null=True)

    def __str__(self):
        return f'{self.client_name} belongs to agent {self.usercode}'


class ActivityLog(models.Model):
    user = models.CharField(max_length= 100, null=True)
    action = models.CharField(max_length= 100, null=True)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"{self.user} {self.action}"