import random
import string
import copy
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render, get_object_or_404
# from login.models import MemberDetails, ClientDetails
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from dateutil.relativedelta import relativedelta
from django.template.loader import get_template
# from reportlab.lib.pagesizes import letter

from django.contrib.auth.hashers import make_password
from django.http import FileResponse
# from reportlab.lib.units import inch
# from reportlab.pdfgen import canvas
from django.core import serializers
from django.contrib import messages
from django.conf import settings
from django.urls import reverse

from client.models import *
from login.models import AdminDetails
# from fee_sys.requests import *
# from xhtml2pdf import pisa
# from fee_sys.auth import *
from .models import *
from .filter import *
# from .forms import *
import requests
import datetime
# import pyshorteners
import json
import io
import os
import csv

import environ

env = environ.Env()
environ.Env.read_env()
import secrets






# PART I                    
# info = {}

# for x in Subscriptions.objects.all():
#     for y in AccountSubscription.objects.all():
#         if x.client_id == y.client_id:

#             try:
#                 for m, n in x.subscribed_modules.items():
#                     info[n['module_name']] = {
#                                             "module_id": n['module_id'],
#                                             "module_name": n['module_name'],
#                                             "expires_on": n['expires_on'],
#                                             "amount_paid": n['amount_paid']
#                                             }
                                            
#                 y.modules = info
#                 y.confirmed = True
#                 y.invoice_no = x.subscription_id
#                 y.save()
#             except:
#                 pass   
#         else:
#             pass  




# # PART II
# for x in ClientSizes.objects.all():

#     try:
#         sizex = MembershipSizes.objects.get(size__contains=x.size)
#         x.client_size = sizex
#         x.pid = x.client_id
#         x.save()  

#     except:
#         sizex = MembershipSizes.objects.all().first()
#         x.client_size = sizex
#         x.pid = x.client_id
#         x.save() 

  




# # PART III
# for x in AccountSubscription.objects.all():

#     try:
#         sizex = MembershipSizes.objects.get(size__contains=x.membership_size)

#     except:
#         sizex = MembershipSizes.objects.all().first()

#     try:
#         clix = ClientSizes.objects.get(pid=x.client_id)
#         clix.client_name = x.client
#         clix.client_size = sizex
#         clix.size = sizex.size
#         clix.save() 
#     except:
#         clix = ClientSizes.objects.create(
#             client_id=x.client_id,
#             pid=x.client_id,
#             client_name = x.client,
#             client_size = sizex,
#             size = sizex.size
#             )

#         clix.save() 



# for x in AccountSubscription.objects.all():
#     try:
#         data = Subscriptions.objects.get(client_id=x.client_id)
#         data.subscribed_modules = x.modules
#         data.save()
#     except:
#         pass    





base_url = "https://db-api-v2.akwaabasoftware.com"


def days_between_today_and_future(future_date):
    # Get today's date
    today_date = datetime.datetime.today().date()

    # Parse the future date string into a datetime object
    future_datetime = datetime.datetime.fromisoformat(future_date.replace("Z", "+00:00"))

    # Get the future date
    future_date_only = future_datetime.date()

    # Calculate the difference in days
    days_difference = (future_date_only - today_date).days

    return days_difference


def send_notice(firstname, email, expiry_date):

    subject = f'ACCOUNT EXPIRY NOTICE'

    body = f"""
                Hi {firstname}, 

                Your account with Akwaaba Solutions will expire on {expiry_date}. You must renew your account soon.  
                Login into your account to renew or contact the provider for assistance.
                Thanks.
            """
    senders_mail = settings.EMAIL_HOST_USER
    to_address = [f'{email}']


    mail = EmailMessage(subject, body, senders_mail, to_address)

    try:
        mail.send()
        # pass
    except: 
        print("Server error")
        pass



def send_expiry_mail():

    histories = AccountSubscription.objects.filter(confirmed=True)

    for x in histories:
        deadline = days_between_today_and_future(str(x.expires_on))

        url = "https://db-api-v2.akwaabasoftware.com/clients/hash-hash"

        payload = json.dumps({
        "accountId": x.client_id
        })

        headers = {
                'Content-Type': 'application/json',
                'Cookie': 'csrftoken=2IKAQnf28CPgts8iFrgCrlRI17Mh96Is; sessionid=vsnlu09sie7ze9lu38p694c4ubf5ndil'
                }

        try:
            firstname = requests.request("POST", url, headers=headers, data=payload).json()['user']['firstname']
            email = requests.request("POST", url, headers=headers, data=payload).json()['user']['email']


            if deadline == 30 or deadline == 15 or deadline == 3:
                send_notice(firstname, email, x.expires_on)
                print("Sent")
            else:
                print("Nothing sent") 
                  
        except:
            pass         






def random_char(y):
    return ''.join(random.choice(string.ascii_uppercase) for x in range(y))



def fee_plan_csv(request, *args, **kwargs):
    
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['Subscription Type','Module', 'Membership Size', 'Unit Cost(USD)', 'Unit Cost(GHS)', 'Promo Months', 'Discount amount(USD)', 'Discount amount(GHS)', 'Updated By'])

    for donor in ModuleFee.objects.all().values_list('subscription_type', 'module_name', 'membership_size', 'unit_fee_usd', 'unit_fee_ghs', 'promo_duration', 'discount_amount_usd', 'discount_amount_ghs', 'created_by'):
        writer.writerow(donor)

    response['Content-Disposition'] =  'filename="fee-plan.csv"'

    return response



# Create your views here.
def index(request):

    template_name = 'superuser/index.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    token = details.token
    account_name = details.account_name
    fullname = details.fullname
    branch = details.branch

    payload = {}
    headers = {
    'Authorization': f'Token {token}',
    'Cookie': 'csrftoken=h4pQDelj3cdEjt4z8HjjUc4U1yL84jbA; sessionid=v20h0pd32jnnsoca6qzjcirfjrta41yu'
    }




    database = 0
    fees = 0
    school = 0
    attendance = 0
    app = 0
    messenger = 0
    finance = 0
    file = 0
    postmaster = 0
    givers = 0
    
    forms = 0

    # for item in response:
    #         if item['module'] in modules:
    #             item['expires_on'] = modules[item['module']]['expires_on']

    for i in AccountSubscription.objects.filter(confirmed=True):

        for x in i.modules.keys():

            if "Database" in x:
                database += 1

            elif "Fee" in x or "Fees" in x or "Cash" in x:
                fees += 1

            elif "School" in x:
                school += 1

            elif "Attendance" in x:
                attendance += 1  

            elif "App" in x:
                app += 1  

            elif "Postmaster" in x:
                postmaster += 1  

            else:
                pass                  

    try:
        total_commission = sum([x.amount for x in TotalCommission.objects.all()])
    except:
        total_commission = 0.00 

    total_agents = Agents.objects.all().count()
    total_agents_male = Agents.objects.filter(gender=1).count()
    total_agents_female = Agents.objects.filter(gender=2).count()

    total_clients = requests.request("GET", "https://db-api-v2.akwaabasoftware.com/clients/account?datatable_plugin&length=1000", headers=headers, data=payload).json()['recordsTotal']
    total_clients_male = requests.request("GET", "https://db-api-v2.akwaabasoftware.com/clients/account?datatable_plugin&length=1000&applicantGender=1", headers=headers, data=payload).json()['recordsTotal']
    total_clients_female = requests.request("GET", "https://db-api-v2.akwaabasoftware.com/clients/account?datatable_plugin&length=1000&applicantGender=2", headers=headers, data=payload).json()['recordsTotal']


    expired_clients = AccountSubscription.objects.filter(confirmed=True, expired=True).count()
    active_clients = AccountSubscription.objects.filter(confirmed=True, expired=False).count()

    modulexx = Modules.objects.all()
    modules = [database, fees, school, attendance, app, postmaster, messenger, givers, finance, file]
    statistics = [total_clients, total_clients_male, total_clients_female, total_agents, total_agents_male, total_agents_female, total_commission, active_clients, expired_clients]

    # for x in modulexx:
    #     sizex.append(len(Modules.objects.filter(client_id=client_id, class_assigned=x.id)))


    return render(request, template_name, {
        'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
        'total_clients': total_clients,
        'total_clients_male': total_clients_male,
        'total_clients_female': total_clients_female,
        'total_agents': total_agents,
        'total_agents_male': total_agents_male,
        'total_agents_female': total_agents_female,
        'total_commission': total_commission,
        'expired_clients': expired_clients,
        'active_clients': active_clients,
        'database': database,
        'fees': fees,
        'school': school,
        'attendance': attendance,
        'app': app,
        'messenger': messenger,
        'postmaster': postmaster,
        'finance': finance,
        'forms': forms,
        'file': file,
        'modules':modules,
        'givers':givers,
        'statistics':statistics,
        'fullname':fullname
    })



# Create Fee types
def createMembershipSize(request):
    # if ClientDetails.objects.count() > 0:
    #     admin = user['firstname'] +' '+ user['surname']

    template_name = 'superuser/create-sizes.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch


    if request.method == 'POST':
        sizes = request.POST.get('sizes')
        # unit_amount_usd = request.POST.get('unit_amount_usd')

        # unit = request.POST.get('unit_amount_ghs') 
        # unit_amount_ghs = round(float(unit), 2)

        if ',' in sizes:
            sizes = sizes.split(',')

            for size in sizes:
                size = MembershipSizes(size=size)
                size.save()

            # activity = ActivityLog(user=admin, action=f'created fee type(s) {",".join(fee_types)}')    
            # activity.save()
        else:
            size = MembershipSizes(size=sizes)
            size.save()

            # activity = ActivityLog(user=admin, action=f'created fee type {fee_types}')    
            # activity.save()

        messages.success(request, 'Membership Size(s) created successfully!')
        return HttpResponseRedirect(reverse('superuser:viewMembershipSizes')) 
    else:
        return render(request, template_name, {
                    'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
        })
    # else:
    #     messages.error(request, 'Please Login to continue') 
    #     return HttpResponseRedirect(reverse('login:login')) 



# View fee type

def viewMembershipSizes(request):
    # if ClientDetails.objects.count() > 0:

    template_name = 'superuser/view-sizes.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch


    return render(request, template_name, {
        'sizes': MembershipSizes.objects.all(),
                'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
    })

    # else:
    #     messages.error(request, 'Please Login to continue') 
    #     return HttpResponseRedirect(reverse('login:login'))


# Edit fee type
def editMembershipSize(request, id):
 

    template_name = 'superuser/edit-size.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch



    size = MembershipSizes.objects.get(id=id)
    
    if request.method == 'POST':
        size.size = request.POST.get('size')

        size.save()


        messages.success(request, 'Membership size edited successfully!')

        return HttpResponseRedirect(reverse('superuser:viewMembershipSizes')) 


    return render(request, template_name, {
        'size': size,
        'sizes': MembershipSizes.objects.all().order_by('size'),
                'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
    }) 




# Delete fee type
def deleteMembershipSize(request, id, *args, **kwargs):
    # admin = user['firstname'] +' '+ user['surname']

    if request.method == "POST":
        fee_type = MembershipSizes.objects.get(id=id)
        fee_type.delete()

        # activity = ActivityLog(user=admin, action=f'deleted fee type {fee_type}')    
        # activity.save()

    messages.success(request, 'Membership size deleted successfully!')
    return HttpResponseRedirect(reverse('superuser:viewMembershipSizes')) 


    

# Fee Type Views
# Create Fee types
def createModule(request):

    template_name = 'superuser/create-module.html'

    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch


    if request.method == 'POST':
        module = request.POST.get('module')
        description = request.POST.get('description')
        logo = request.FILES.get('logo')

        mode = Modules.objects.create(module=module, description=description, logo=logo)
        mode.save()

        if "database" in module or "Database" in module:
            mode.default = True
            mode.save()

        activity = ActivityLog(user="admin", action=f'created module {module}')    
        activity.save()

        messages.success(request, 'Module created successfully!')
        return HttpResponseRedirect(reverse('superuser:viewModules')) 
    else:
        return render(request, template_name, {
                    'session_id':session_id,
        'account_name':account_name,
        'branch':branch,

        })



# View fee type
def viewModules(request):
    # if ClientDetails.objects.count() > 0:

    template_name = 'superuser/view-modules.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch


    modules=Modules.objects.all().order_by('-id')


    return render(request, template_name, {
        'modules': modules,
                'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
    })
    # else:
    #     messages.error(request, 'Please Login to continue') 
    #     return HttpResponseRedirect(reverse('login:login'))


def viewModule(request, id):
    # if ClientDetails.objects.count() > 0:

    template_name = 'superuser/view-module.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch


    mode = Modules.objects.get(id=id)
    modules=Modules.objects.all()

    return render(request, template_name, {
        'mode': mode,
                'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
    })
    # else:
    #     messages.error(request, 'Please Login to continue') 
    #     return HttpResponseRedirect(reverse('login:login'))


# Edit fee type
def editModule(request, id):
    # if ClientDetails.objects.count() > 0:
    #     admin = user['firstname'] +' '+ user['surname']

    template_name = 'superuser/edit-module.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch


    mode = Modules.objects.get(id=id)
    modules = Modules.objects.all()
    
    if request.method == 'POST':
        mode.module = request.POST.get('module')
        mode.description = request.POST.get('description')
        new_logo = request.FILES.get('logo', None)
        if new_logo is not None:
            mode.logo = request.FILES.get('logo', None)

        mode.save()

        activity = ActivityLog(user='admin', action=f'edited module {mode.module}')    
        activity.save()

        messages.success(request, 'Module edited successfully!')

        return HttpResponseRedirect(reverse('superuser:viewModules')) 


    return render(request, template_name, {
        'mode': mode,
        'modules': modules,
                'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
    }) 


    # else:
    #     messages.error(request, 'Please Login to continue') 
    #     return HttpResponseRedirect(reverse('login:login'))



# Delete fee type
def deleteModule(request, id, *args, **kwargs):
    # admin = user['firstname'] +' '+ user['surname']

    if request.method == "POST":
        mode = Modules.objects.get(id=id)
        mode.delete()

        activity = ActivityLog(user='admin', action=f'deleted module {mode}')    
        activity.save()

    messages.success(request, 'Module deleted successfully!')
    return HttpResponseRedirect(reverse('superuser:viewModules')) 






def setActivation(request):
    # if ClientDetails.objects.count() > 0:
    #     admin = user['firstname'] +' '+ user['surname']
    template_name = 'superuser/set-activation.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch


    sizes = MembershipSizes.objects.all()

    if request.method == 'POST':
        membership_size_id = request.POST.get('membership_size')
        membership_size = MembershipSizes.objects.get(id=membership_size_id)

        activation_fee = request.POST.get('activation_fee')
        duration = request.POST.get('duration')

        try:
            act = ActivationFee.objects.get(membership_size=membership_size)
            act.activation_fee = activation_fee
            act.duration = duration
            act.save()
        except:
            act = ActivationFee.objects.create(membership_size=membership_size, activation_fee=activation_fee, duration=duration)
            act.save()    
            

        activity = ActivityLog(user="admin", action=f'set activation fee')    
        activity.save()

        messages.success(request, 'Activation fee set successfully!')
        return HttpResponseRedirect(reverse('superuser:viewActivation')) 

    else:
        return render(request, template_name, {
            'sizes':sizes,
                    'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
        })



# View fee type
def viewActivation(request):
    # if ClientDetails.objects.count() > 0:

    template_name = 'superuser/view-activation.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch


    details=ActivationFee.objects.all()

    return render(request, template_name, {
        'details': details,
                'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
    })



# Edit fee type
def editActivation(request, id):

    template_name = 'superuser/edit-activation.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch


    detail = ActivationFee.objects.get(id=id)
    
    if request.method == 'POST':
        detail.activation_fee = request.POST.get('activation_fee')
        detail.duration = request.POST.get('duration')
        detail.save()

        activity = ActivityLog(user='admin', action=f'edited activation fee')    
        activity.save()

        messages.success(request, 'Activation fee edited successfully!')

        return HttpResponseRedirect(reverse('superuser:viewActivation')) 


    return render(request, template_name, {
        'detail': detail,
                'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
    }) 





def deleteActivation(request, id, *args, **kwargs):
    # admin = user['firstname'] +' '+ user['surname']

    if request.method == "POST":
        mode = ActivationFee.objects.get(id=id)
        mode.delete()

        activity = ActivityLog(user='admin', action=f'deleted activation fee {mode}')    
        activity.save()

    messages.success(request, 'Activation Fee deleted successfully!')
    return HttpResponseRedirect(reverse('superuser:viewActivation')) 








def createPaymentDetails(request):
    # if ClientDetails.objects.count() > 0:
    #     admin = user['firstname'] +' '+ user['surname']
    template_name = 'superuser/create-payment-detail.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch


    base_url = "https://db-api-v2.akwaabasoftware.com/clients"

    today = datetime.date.today()
    # last_paid = datetime.datetime.today().strftime("%Y-%m-%d")
    year = datetime.datetime.now().year
    # today = datetime.datetime.now()
    year = str(year) + "0000"


    url = base_url + "/account?datatable_plugin&length=1000"

    payload = json.dumps({})

    headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=xuw6ruEorE0efPI1r7eypD46F5gkVdJjDCnpUCBqpeDPR799G7V4h5GRIoOfer5R; sessionid=ij0kr81ryje5mijdenssrwt3coffqw4z'
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()['data']

    arr = []
    clieds = []

    for x in response:
        arr.append(x['name'])
        clieds.append(x['id'])

    allids = zip(arr, clieds)



    if request.method == 'POST':
        client_id = request.POST.get('client')

        client_url = f'{base_url}/account?id={client_id}'

        payload = json.dumps({})

        headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=i0QCkPPQCUAYcsvB4MvYAfzl4HrLL0GJ'
        }

        response = requests.request("GET", client_url, headers=headers, data=payload).json()['results'][0]

        client_name = response['name']

        merchant_account_number = request.POST.get('merchant_account_number')



        detail = PaymentDetails.objects.get_or_create(client_id=client_id, client_name=client_name, merchant_account_number=merchant_account_number)
        

        activity = ActivityLog(user="admin", action=f'created payment detail for {client_name}')    
        activity.save()

        messages.success(request, 'Payment Details created successfully!')
        return HttpResponseRedirect(reverse('superuser:viewPaymentDetails')) 

    else:
        return render(request, template_name, {
            'arr':allids,
                    'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
        })


    # else:
    #     messages.error(request, 'Please Login to continue') 
    #     return HttpResponseRedirect(reverse('login:login')) 





# View fee type
def viewPaymentDetails(request):
    # if ClientDetails.objects.count() > 0:

    template_name = 'superuser/view-payment-details.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch


    details=PaymentDetails.objects.all()


    return render(request, template_name, {
        'details': details,
                'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
    })




# Edit fee type
def editPaymentDetails(request, id):
    # if ClientDetails.objects.count() > 0:
    #     admin = user['firstname'] +' '+ user['surname']

    template_name = 'superuser/edit-payment-detail.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch


    detail = PaymentDetails.objects.get(id=id)
    details=PaymentDetails.objects.all()
    
    if request.method == 'POST':
        detail.merchant_account_number = request.POST.get('merchant_account_number')
        detail.save()

        activity = ActivityLog(user='admin', action=f'edited payment details')    
        activity.save()

        messages.success(request, 'Payment details edited successfully!')

        return HttpResponseRedirect(reverse('superuser:viewPaymentDetails')) 


    return render(request, template_name, {
        'detail': detail,
        'details': details,
                'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
    }) 


    # else:
    #     messages.error(request, 'Please Login to continue') 
    #     return HttpResponseRedirect(reverse('login:login'))



# Delete fee type
def deletePaymentDetails(request, id, *args, **kwargs):
    # admin = user['firstname'] +' '+ user['surname']

    if request.method == "POST":
        mode = PaymentDetails.objects.get(id=id)
        mode.delete()

        activity = ActivityLog(user='admin', action=f'deleted payment detail {mode}')    
        activity.save()

    messages.success(request, 'Payment details deleted successfully!')
    return HttpResponseRedirect(reverse('superuser:viewPaymentDetails')) 




















def createClientsize(request):

    template_name = 'superuser/create-client-size.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    account_name = details.account_name
    branch = details.branch


    base_url = "https://db-api-v2.akwaabasoftware.com/clients"
    url = base_url + "/account?datatable_plugin&length=1000"

    payload = json.dumps({})

    headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=xuw6ruEorE0efPI1r7eypD46F5gkVdJjDCnpUCBqpeDPR799G7V4h5GRIoOfer5R; sessionid=ij0kr81ryje5mijdenssrwt3coffqw4z'
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()['data']

    arr = []
    clieds = []

    for x in response:
        arr.append(x['name'])
        clieds.append(x['id'])

    allids = zip(arr, clieds)

    sizes = MembershipSizes.objects.all()

    if request.method == 'POST':
        client_id = request.POST.get('client_id')

        client_url = f'{base_url}/account?id={client_id}'

        payload = json.dumps({})

        headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=i0QCkPPQCUAYcsvB4MvYAfzl4HrLL0GJ'
        }

        response = requests.request("GET", client_url, headers=headers, data=payload).json()['results'][0]

        client_name = response['name']

        size_id = request.POST.get('membership_size')


        size = MembershipSizes.objects.get(id=size_id)

        try:
            client_size = ClientSizes.objects.get(client_id=client_id)
            client_size.client_name=client_name
            client_size.size=size.size
            client_size.client_size=size
            client_size.pid=client_id
            client_size.save()

        except:
            client_size = ClientSizes.objects.create(
                client_id=client_id,
                client_name=client_name,
                size=size.size,
                client_size=size,
                pid=client_id,
            )
            client_size.save()


        activity = ActivityLog(user="admin", action=f'created payment detail for {client_name}')    
        activity.save()

        messages.success(request, 'Client membership size added successfully!')
        return HttpResponseRedirect(reverse('superuser:viewClientsizes')) 

    else:
        return render(request, template_name, {
            'sizes':sizes,
            'arr':allids,
            'session_id':session_id,
            'account_name':account_name,
            'branch':branch,
        })




# View fee type
def viewClientsizes(request):

    template_name = 'superuser/view-client-sizes.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    account_name = details.account_name
    branch = details.branch


    details=ClientSizes.objects.all()


    return render(request, template_name, {
        'details': details,
        'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
    })




# Edit fee type
def editClientsize(request, id):

    template_name = 'superuser/edit-client-size.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)
  
    account_name = details.account_name
    branch = details.branch


    detail = ClientSizes.objects.get(id=id)
    
    sizes = MembershipSizes.objects.all()

    if request.method == 'POST':

        size_id = request.POST.get('membership_size')
        size = MembershipSizes.objects.get(id=size_id)

        detail.size=size.size
        detail.client_size=size
        detail.save()

        activity = ActivityLog(user='admin', action=f'changed client membership size')    
        activity.save()

        messages.success(request, 'Client membership size changed successfully!')

        return HttpResponseRedirect(reverse('superuser:viewClientsizes')) 


    return render(request, template_name, {
        'sizes':sizes,
        'detail': detail,
        'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
    }) 




# # Delete fee type
def deleteClientsize(request, id, *args, **kwargs):

    if request.method == "POST":
        mode = ClientSizes.objects.get(id=id)
        mode.delete()

        activity = ActivityLog(user='admin', action=f'deleted client size {mode}')    
        activity.save()

    messages.success(request, 'Client membership size deleted successfully!')
    return HttpResponseRedirect(reverse('superuser:viewClientsizes')) 



















def createEmailDetails(request):
    # if ClientDetails.objects.count() > 0:
    #     admin = user['firstname'] +' '+ user['surname']
    template_name = 'superuser/create-email-detail.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch


    base_url = "https://db-api-v2.akwaabasoftware.com/clients"

    today = datetime.date.today()
    # last_paid = datetime.datetime.today().strftime("%Y-%m-%d")
    year = datetime.datetime.now().year
    # today = datetime.datetime.now()
    year = str(year) + "0000"


    url = base_url + "/account?datatable_plugin&length=1000"

    payload = json.dumps({})

    headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=xuw6ruEorE0efPI1r7eypD46F5gkVdJjDCnpUCBqpeDPR799G7V4h5GRIoOfer5R; sessionid=ij0kr81ryje5mijdenssrwt3coffqw4z'
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()['data']

    arr = []
    clieds = []

    for x in response:
        arr.append(x['name'])
        clieds.append(x['id'])

    allids = zip(arr, clieds)



    if request.method == 'POST':
        client_id = request.POST.get('client')

        client_url = f'{base_url}/account?id={client_id}'

        payload = json.dumps({})

        headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=i0QCkPPQCUAYcsvB4MvYAfzl4HrLL0GJ'
        }

        response = requests.request("GET", client_url, headers=headers, data=payload).json()['results'][0]

        client_name = response['name']

        email = request.POST.get('email')
        password = request.POST.get('password')



        detail = EmailDetails.objects.get_or_create(client_id=client_id, client_name=client_name, email=email, password=password)
        

        activity = ActivityLog(user="admin", action=f'created email detail for {client_name}')    
        activity.save()

        messages.success(request, 'Email Details created successfully!')
        return HttpResponseRedirect(reverse('superuser:viewEmailDetails')) 

    else:
        return render(request, template_name, {
            'arr':allids,
                    'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
        })


    # else:
    #     messages.error(request, 'Please Login to continue') 
    #     return HttpResponseRedirect(reverse('login:login')) 





# View fee type
def viewEmailDetails(request):
    # if ClientDetails.objects.count() > 0:

    template_name = 'superuser/view-email-details.html'
    details=EmailDetails.objects.all()
    session_id = request.COOKIES.get('session_id')
    detail = AdminDetails.objects.get(session_id=session_id)

    client_id = detail.pid
    token = detail.token
    email = detail.email  
    password = detail.password  
    account_name = detail.account_name
    branch = detail.branch

    return render(request, template_name, {
        'details': details,
        'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
    })




def editEmailDetails(request, id):
    template_name = 'superuser/edit-email-detail.html'
    detail = EmailDetails.objects.get(id=id)
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch
    # Make a copy of the instance

    detail_copy = copy.deepcopy(detail)
    details=EmailDetails.objects.all()

    if request.method == 'POST':
        detail_copy.email = request.POST.get('email')
        detail_copy.password = request.POST.get('password')
        detail_copy.save()

        messages.success(request, 'Email details edited successfully!')
        return HttpResponseRedirect(reverse('superuser:viewEmailDetails'))

    return render(request, template_name, {
        'detail': detail,
        'details': details,
        'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
    })



# Delete fee type
def deleteEmailDetails(request, id, *args, **kwargs):

    if request.method == "POST":
        mode = EmailDetails.objects.get(id=id)
        mode.delete()

        activity = ActivityLog(user='admin', action=f'deleted email detail {mode}')    
        activity.save()

    messages.success(request, 'Email details deleted successfully!')
    return HttpResponseRedirect(reverse('superuser:viewEmailDetails')) 














def createUnitedOrganization(request):
    # if ClientDetails.objects.count() > 0:
    #     admin = user['firstname'] +' '+ user['surname']
    template_name = 'superuser/create-united-organization.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch


    base_url = "https://db-api-v2.akwaabasoftware.com/clients"

    today = datetime.date.today()
    # last_paid = datetime.datetime.today().strftime("%Y-%m-%d")
    year = datetime.datetime.now().year
    # today = datetime.datetime.now()
    year = str(year) + "0000"


    url = base_url + "/account?datatable_plugin&length=1000"

    payload = json.dumps({})

    headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=xuw6ruEorE0efPI1r7eypD46F5gkVdJjDCnpUCBqpeDPR799G7V4h5GRIoOfer5R; sessionid=ij0kr81ryje5mijdenssrwt3coffqw4z'
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()['data']

    arr = []
    clieds = []

    for x in response:
        arr.append(x['name'])
        clieds.append(x['id'])

    allids = zip(arr, clieds)



    if request.method == 'POST':
        client_id = request.POST.get('client')

        client_url = f'{base_url}/account?id={client_id}'

        payload = json.dumps({})

        headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=i0QCkPPQCUAYcsvB4MvYAfzl4HrLL0GJ'
        }

        response = requests.request("GET", client_url, headers=headers, data=payload).json()['results'][0]

        client_name = response['name']


        detail = UnitedOrganizations.objects.get_or_create(client_id=client_id, client_name=client_name)
        

        activity = ActivityLog(user="admin", action=f'added united organization')    
        activity.save()

        messages.success(request, 'UN Organization added successfully!')
        return HttpResponseRedirect(reverse('superuser:viewUnitedOrganizations')) 

    else:
        return render(request, template_name, {
            'arr':allids,
                    'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
        })







# View fee type
def viewUnitedOrganizations(request):
    # if ClientDetails.objects.count() > 0:

    template_name = 'superuser/view-united-organizations.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch


    details=UnitedOrganizations.objects.all()


    return render(request, template_name, {
        'details': details,
                'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
    })



# Delete fee type
def deleteUnitedOrganization(request, id, *args, **kwargs):

    if request.method == "POST":
        mode = UnitedOrganizations.objects.get(id=id)
        mode.delete()

        activity = ActivityLog(user='admin', action=f'removed united organization {mode}')    
        activity.save()

    messages.success(request, 'UN Organization removed successfully!')
    return HttpResponseRedirect(reverse('superuser:viewUnitedOrganizations')) 










def setModuleFees(request):
    template_name = 'superuser/set-module-fees.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    account_name = details.account_name
    branch = details.branch


    modes = Modules.objects.all()
    sizes = MembershipSizes.objects.all()
    modules = []



    if request.method == 'POST':
        subscription_type = request.POST.get('subscription_type') 
        duration = request.POST.get('duration') if request.POST.get('duration') else 0


        membership_size = request.POST.get('membership_size') 
        client_size = MembershipSizes.objects.get(id=membership_size)


        module_ids = request.POST.getlist('foo[]') 

        unit_amounts_usd = request.POST.getlist('unit_amounts_usd[]') 
        unit_amounts_usd = [round(float(x), 2) for x in unit_amounts_usd if x != '']

        unit_amounts_ghs = request.POST.getlist('unit_amounts_ghs[]')
        unit_amounts_ghs = [round(float(x), 2) for x in unit_amounts_ghs if x != '']
            

        for cid in module_ids:
            modules.append(Modules.objects.get(id=cid))


        promo = request.POST.get('promo')

        if promo:
            promo = True
            promo_discount = request.POST.get('promo_discount') if request.POST.get('promo_discount') else 0
            promo_duration = request.POST.get('promo_duration') if request.POST.get('promo_duration') else int(promo_duration)

        else:
            promo = False 
            promo_discount = None
            promo_duration = None   



        for i in range(len(module_ids)):

            try:

                set_fee = ModuleFee.objects.get(
                    subscription_type=subscription_type,
                    module=modules[i],
                    module_name=Modules.objects.get(id=module_ids[i]).module,
                    membership_size=client_size.size,
                    client_size=client_size
                )

                set_fee.duration=duration
                set_fee.unit_fee_usd=unit_amounts_usd[i]
                set_fee.unit_fee_ghs=unit_amounts_ghs[i]
                set_fee.promo=promo
                set_fee.promo_discount=promo_discount
                set_fee.respective_increase=0
                set_fee.promo_duration=promo_duration
                set_fee.save()

                messages.success(request, 'Module fee(s) set successfully!')
                return HttpResponseRedirect(reverse('superuser:viewModuleFees')) 

            except: 
                   
                    set_fee = ModuleFee.objects.create(
                        subscription_type=subscription_type,
                        duration=duration,
                        module=modules[i],
                        module_name=Modules.objects.get(id=module_ids[i]).module,
                        membership_size=client_size.size,
                        unit_fee_usd=unit_amounts_usd[i],
                        unit_fee_ghs=unit_amounts_ghs[i],
                        respective_increase=0,
                        promo=promo,
                        promo_discount=promo_discount,
                        promo_duration=promo_duration,
                        created_by="Lord Asante Fordjour",
                        client_size=client_size
                    )  

                    set_fee.save()

        messages.success(request, 'Module fee(s) set successfully!')
        return HttpResponseRedirect(reverse('superuser:viewModuleFees')) 

    else:
        return render(request, template_name, {
            'modes':modes,
            'sizes': sizes,
                    'session_id':session_id,
        'account_name':account_name,
        'branch':branch,

        })




def editModuleFees(request, id, *args, **kwargs):
    template_name = 'superuser/edit-module-fees.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    account_name = details.account_name
    branch = details.branch


    detail = ModuleFee.objects.get(id=id)


    if request.method == 'POST':
        duration = request.POST.get('duration') if request.POST.get('duration') else 0

        unit_amounts_usd = request.POST.getlist('unit_amounts_usd[]') 
        unit_amounts_usd = [round(float(x), 2) for x in unit_amounts_usd if x != '']

        unit_amounts_ghs = request.POST.getlist('unit_amounts_ghs[]')
        unit_amounts_ghs = [round(float(x), 2) for x in unit_amounts_ghs if x != '']
    

        promo = request.POST.get('promo')

        if promo:
            promo = True
            promo_discount = request.POST.get('promo_discount') if request.POST.get('promo_discount') else 0
            promo_duration = request.POST.get('promo_duration') if request.POST.get('promo_duration') else int(promo_duration)

        else:
            promo = False 
            promo_discount = None
            promo_duration = None

  

        detail.duration=duration
        detail.unit_fee_usd=unit_amounts_usd[0]
        detail.unit_fee_ghs=unit_amounts_ghs[0]
        detail.promo=promo
        detail.promo_discount=promo_discount
        detail.promo_duration=promo_duration
        detail.save()

       
        messages.success(request, 'Module fee(s) set successfully!')
        return HttpResponseRedirect(reverse('superuser:viewModuleFees')) 

    else:
        return render(request, template_name, {

            'detail':detail,
            'session_id':session_id,
            'account_name':account_name,
            'branch':branch,

        })





# Delete fee type
def deleteModuleFee(request, id, *args, **kwargs):
    # admin = user['firstname'] +' '+ user['surname']

    if request.method == "POST":
        mode = ModuleFee.objects.get(id=id)
        mode.delete()

        activity = ActivityLog(user='admin', action=f'deleted module fee {mode}')    
        activity.save()

    messages.success(request, 'Module deleted successfully!')
    return HttpResponseRedirect(reverse('superuser:viewModules')) 






def viewModuleFees(request):
    template_name = 'superuser/view-module-fees.html'

    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch


    payments=ModuleFee.objects.all().order_by('-id')
    today = datetime.date.today()

    if request.method == 'GET':
        activations = ModuleFee.objects.filter(subscription_type='Account Activation').order_by('-id')
        payments = ModuleFee.objects.filter(subscription_type='Module Subscription').order_by('-id')
        payment_filter = SetFeeFilter(request.GET, queryset=payments)
        payments = payment_filter.qs
        today = datetime.date.today()



    return render(request, template_name, {
        'payment_filter': payment_filter, 
        'payments': payments, 
        'today': today,
        'activations':activations, 
        'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
        }) 




def load_size(request):
    template_name = 'superuser/size.html'

    if request.method == 'GET': 
        client_id = request.GET.get('client_id')

        try:
            try:
                size = ClientSizes.objects.get(pid=client_id).client_size
            except:
                size = ClientSizes.objects.filter(pid=client_id).first().client_size    
        except:
            size = '0-50'    


        return render(request, template_name, {'size': size})


def load_exchange(request):
    template_name = 'superuser/exchange.html'

    if request.method == 'GET': 
        mode = request.GET.get('mode')

        module = MembershipSizes.objects.filter(size=mode).first()
        usd = module.unit_cost_usd
        ghs = module.unit_cost_ghs


    return render(request, template_name, {'usd': usd, 'ghs':ghs})




def load_items(request):
    template_name = 'superuser/test.html'

    if request.method == 'GET': 
        mode_id = request.GET.get('mode')
        module = Modules.objects.get(id=mode_id)


        try:
            module_detail = ModuleFee.objects.get(module=module)
            
        except:
            module_detail = ModuleFee.objects.filter(module=module).first()
            


        return render(request, template_name, {'mode': module_detail,})






def load_archive(request):
    template_name = 'superuser/archive.html'


    if request.method == 'GET': 
        client_id = request.GET.get('client_id')
        archive = request.GET.get('archive')

        hash_url = "https://db-api-v2.akwaabasoftware.com/clients/hash-hash"

        payload = json.dumps({ "accountId": client_id })
        headers = {
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=h4pQDelj3cdEjt4z8HjjUc4U1yL84jbA; sessionid=v20h0pd32jnnsoca6qzjcirfjrta41yu'
        }

        try:
            token = requests.request("POST", hash_url, headers=headers, data=payload).json()['token']

            url = f"https://db-api-v2.akwaabasoftware.com/clients/account/{client_id}"

            payload = {'archive': f'{archive}'}
            files=[]

            headers = {
            'Authorization': f'Token {token}',
            'Cookie': 'csrftoken=Okmg2qu7wHQd1RjdYflS0kZhITg1ncgV; sessionid=lzujday1dfpf70saxb57t7uwllqwqm0b'
            }

            response = requests.request("PATCH", url, headers=headers, data=payload, files=files).json()

                       
        except:
            pass



        info = "" 


        return render(request, template_name, {'info': info})





def load_modulo(request):
    template_name = 'superuser/modulo.html'
    base_url = "https://account.akwaabasoftware.com/api"


    if request.method == 'GET': 
        client_id = request.GET.get('client_id')

        url = base_url + "/client-size/"

        payload = json.dumps({
        "client_id": client_id
        })

        headers = {
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=i0QCkPPQCUAYcsvB4MvYAfzl4HrLL0GJ'
        }

        response = requests.request("POST", url, headers=headers, data=payload).json()['info']
        size = response['membership_size']

        return render(request, template_name, {'size': size,})




def load_modula(request):
    template_name = 'superuser/modula.html'

    if request.method == 'GET': 
        size = request.GET.get('size')
        duration = request.GET.get('duration')

        if duration == "":
            duration = 1


        module = MembershipSizes.objects.filter(size=size).first()
        cost_usd = int(module.unit_cost_usd) * int(duration)
        cost_ghs = int(module.unit_cost_ghs) * int(duration)


    return render(request, template_name, {'cost_usd':cost_usd, 'cost_ghs':cost_ghs})



def load_time(request):
    template_name = 'superuser/time.html'
    base_url = "https://db-api-v2.akwaabasoftware.com/clients"
    today = datetime.date.today()
    year = datetime.datetime.now().year

    default = Modules.objects.get(default=True).id
 

    if request.method == 'GET': 
        client_id = request.GET.get('client_id')
        database = True

        try:
            datadetail = AccountSubscription.objects.get(client_id=client_id)

            for x in datadetail.modules:
                if "Database" in datadetail.modules[x]['module_name']:
                    database = True
                    break
                else:
                    database = False

        except:
            database = False    


        modxx = Modules.objects.all()   


    return render(request, template_name, {'default':default, 'modxx': modxx, 'database':database })


def days_since_date(date_str):
    today = datetime.date.today()

    try:
        data = datetime.datetime.strptime(date_str, '%d-%m-%Y').date()
    except:
        data = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

    delta = today - data
    return delta.days




def load_expired(request):
    template_name = 'superuser/expired.html'

    if request.method == 'GET': 
        client_id = request.GET.get('client_id')
  
        try:
            sub = Subscriptions.objects.filter(client_id=client_id).last().subscribed_modules

            for x, y in sub.items():

                if y['module_name'] == 'Database Manager' or 'database' in y['module_name']:
                    info = y['expires_on'][0:10]

                    expired = days_since_date(info) if days_since_date(info) > 0 else 0
                
        except:

            expired = 0

    return render(request, template_name, { 'expired':expired })




def subscriptionExtension(request, id):
    template_name = 'superuser/subscription-extension.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    account_name = details.account_name
    branch = details.branch

    subscription = AccountSubscription.objects.get(id=id)
    default = Modules.objects.get(default=True).id

    modxx = subscription.modules 

    now = datetime.datetime.now()
    year = datetime.datetime.now().year
    year = str(year) + "0000"

    modules = []
    quiz = dict()
    invoice_no = remove_non_numeric(str(now))



    if request.method == "POST":

        module_ids = request.POST.getlist('foo[]') 

        for id in module_ids:
            modules.append(Modules.objects.get(id=id))

        duration=request.POST.get('duration') if request.POST.get('duration') != "" else 0

        renewing_days=request.POST.get('renewing_days')
        remaining_days=request.POST.get('remaining_days')
        expiring_days=request.POST.get('expiring_days')

        subscription_fee_usd=request.POST.get('subscription_fee_usd')
        subscription_fee_usd = round(float(subscription_fee_usd), 2)

        subscription_fee_ghs=request.POST.get('subscription_fee_ghs')
        subscription_fee_ghs = round(float(subscription_fee_ghs), 2)


        subscription.duration=duration
        subscription.renewing_days+= int(renewing_days)
        subscription.remaining_days=remaining_days
        subscription.expired_days=expiring_days

        subscription.subscription_fee_usd=subscription_fee_usd
        subscription.subscription_fee_ghs=subscription_fee_ghs
        subscription.description="Subscription"
        subscription.invoice_no=invoice_no
        subscription.date_created = timezone.now()
        

        try:
            subss = Subscriptions.objects.get(client_id=subscription.client_id)
            subss.subscribed_modules = {}
            subss.save()
            
        except:
            subss = Subscriptions.objects.create(client_id=subscription.client_id)



        for module in modules:
            try:

                new_date_obj = datetime.datetime.strptime(subscription.modules[module.module]['expires_on'], '%d-%m-%Y') + datetime.timedelta(days=int(renewing_days))                
            except:
                new_date_obj = datetime.datetime.strptime(subscription.modules[module.module]['expires_on'], '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(days=int(renewing_days)) 


            if "Database" not in module.module:

                try:
                    try:
                        database_obj = datetime.datetime.strptime(subscription.modules['Database Manager']['expires_on'], '%d-%m-%Y')
                    except:
                        database_obj = datetime.datetime.strptime(subscription.modules['Database Manager']['expires_on'], '%Y-%m-%dT%H:%M:%SZ')

                except:
                    database_obj = ""

                if new_date_obj > database_obj:
                    new_date_obj = database_obj 


            else:

                subscription.expires_on = new_date_obj
                subscription.save()

            quiz = {
                    "module_id": module.id,
                    "module_name": module.module,
                    "expires_on": new_date_obj.strftime("%d-%m-%Y"),
                    "amount_paid": subscription_fee_ghs,
                }
                
            subscription.modules[module.module] = quiz


        subscription.save()

        subss.client = subscription.client
        subss.subscription_id = invoice_no
        subss.subscribed_modules = subscription.modules
        subss.save()


        messages.success(request, 'Subscription extension successful!')
        return HttpResponseRedirect(reverse('superuser:subscriptionHistory' )) 
    else:    
        return render(request, template_name, {
            
            'subscription':subscription,
            'session_id':session_id,
            'account_name':account_name,
            'branch':branch,
            'modxx': modxx,
            'default':default,
        })




def subscriptionRenewal(request, id):
    template_name = 'superuser/subscription-renewal.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    account_name = details.account_name
    branch = details.branch

    subscription = AccountSubscription.objects.get(id=id)
    default = Modules.objects.get(default=True).id

    modxx = subscription.modules 


    modules = []
    quiz = dict()

    now = datetime.datetime.now()
    invoice_no = remove_non_numeric(str(now))


    if request.method == "POST":

        module_ids = request.POST.getlist('foo[]') 

        for id in module_ids:
            modules.append(Modules.objects.get(id=id))

        duration=request.POST.get('duration') if request.POST.get('duration') != "" else 0

        renewing_days=request.POST.get('renewing_days')
        remaining_days=request.POST.get('remaining_days')
        expiring_days=request.POST.get('expiring_days')

        subscription_fee_usd=request.POST.get('subscription_fee_usd')
        subscription_fee_usd = round(float(subscription_fee_usd), 2)

        subscription_fee_ghs=request.POST.get('subscription_fee_ghs')
        subscription_fee_ghs = round(float(subscription_fee_ghs), 2)

        subscription.duration=duration
        subscription.renewing_days+= int(renewing_days)
        subscription.remaining_days=remaining_days
        subscription.expired_days=expiring_days

        subscription.subscription_fee_usd=subscription_fee_usd
        subscription.subscription_fee_ghs=subscription_fee_ghs
        subscription.description="Subscription"
        subscription.invoice_no=invoice_no
        subscription.date_created = timezone.now()

        try:
            subss = Subscriptions.objects.get(client_id=subscription.client_id)
            subss.subscribed_modules = {}
            subss.save()
            
        except:
            subss = Subscriptions.objects.create(client_id=subscription.client_id)



        for module in modules:
            try:
                new_date_obj = datetime.datetime.strptime(subscription.modules[module.module]['expires_on'], '%d-%m-%Y') + datetime.timedelta(days=int(renewing_days))                
            except:
                new_date_obj = datetime.datetime.strptime(subscription.modules[module.module]['expires_on'], '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(days=int(renewing_days)) 


            if "Database" not in module.module:

                try:
                    try:
                        database_obj = datetime.datetime.strptime(subscription.modules['Database Manager']['expires_on'], '%d-%m-%Y')
                    except:
                        database_obj = datetime.datetime.strptime(subscription.modules['Database Manager']['expires_on'], '%Y-%m-%dT%H:%M:%SZ')

                except:
                    database_obj = ""

                if new_date_obj > database_obj:
                    new_date_obj = database_obj 


            else:

                subscription.expires_on = new_date_obj
                subscription.save()


            quiz = {
                    "module_id": module.id,
                    "module_name": module.module,
                    "expires_on": new_date_obj.strftime("%d-%m-%Y"),
                    "amount_paid": subscription_fee_ghs,
                }
                
            subscription.modules[module.module] = quiz


        
        subscription.save()

        subss.client = subscription.client
        subss.subscription_id = invoice_no
        subss.subscribed_modules = subscription.modules
        subss.save()


        messages.success(request, 'Subscription extension successful!')
        return HttpResponseRedirect(reverse('superuser:subscriptionHistory' )) 
    else:    
        return render(request, template_name, {
            
            'subscription':subscription,
            'session_id':session_id,
            'account_name':account_name,
            'branch':branch,
            'modxx': modxx,
            'default':default,
        })



#  Delete fee type
def deleteSubscription(request, id, *args, **kwargs):

    if request.method == "POST":
        account = AccountSubscription.objects.get(id=id)
        subscription = Subscriptions.objects.get(client_id=account.client_id) 

        subscription.delete()
        account.delete()


    messages.success(request, 'Subscription deleted successfully!')
    return HttpResponseRedirect(reverse('superuser:subscriptionHistory')) 




def load_modules(request):
    template_name = 'superuser/modules.html'

    if request.method == 'GET': 
        subscription_id = request.GET.get('subscription_id')

        subscription = AccountSubscription.objects.get(id=subscription_id)

        return render(request, template_name, {'subscription': subscription})


def subscriptionHistory(request, **kwargs):
    template_name = 'superuser/subscription-history.html'

    today = timezone.now()

    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)
    account_name = details.account_name
    branch = details.branch
    client_id = details.pid
    token = details.token
    

    if request.method == 'POST':
        modules = request.POST.getlist('modules[]')
        subscription_id = request.POST.get('subscription_id')

        account = AccountSubscription.objects.get(id=subscription_id)
        subscription = Subscriptions.objects.get(client_id=account.client_id) 
        
        database = False

        for x in modules:
            if "Database" in Modules.objects.get(id=x).module:
                database = True


        if database:
            account.delete()
            subscription.delete()

        else:
            for y in modules:
                del account.modules[Modules.objects.get(id=y).module]
                del subscription.subscribed_modules[Modules.objects.get(id=y).module]
                account.save()
                subscription.save()


        messages.success(request, 'Module(s) unsubscribed successfully')
        return HttpResponseRedirect(reverse('superuser:subscriptionHistory')) 


    else:

        send_expiry_mail()

        histories = AccountSubscription.objects.filter(confirmed=True, special=False)

        for x in histories:
            # print(x.expires_on)

            if today > x.expires_on:
                x.expired = True
            else:
                x.expired = False

            x.save()    
        

        return render(request, template_name, {
            # 'history_filter': history_filter, 
            'histories': histories, 
            'today': today, 
            'pid': client_id,
            'session_id':session_id,
            'account_name':account_name,
            'branch':branch,
        }) 


def random_char(y):
    return ''.join(random.choice(string.ascii_uppercase) for x in range(y))
    

def remove_non_numeric(string):
    return ''.join(filter(str.isdigit, string))


# try:
#     try:
#         account_expiry = datetime.datetime.strptime(account_expiry, '%d-%m-%Y').strftime('%d %B, %Y') 
#     except:
#         account_expiry = datetime.datetime.strptime(account_expiry, '%Y-%m-%d').strftime('%d %B, %Y')  
# except: 
#     account_expiry = datetime.datetime.strptime(account_expiry, '%Y-%m-%dT%H:%M:%SZ').strftime('%d %B, %Y')  

def accountSubscription(request):
    template_name = 'superuser/account-subscription.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch
    now = datetime.datetime.now()

    invoice_no = remove_non_numeric(str(now))

    modes = Modules.objects.filter(default=False)
    sizes = MembershipSizes.objects.all()
    base_url = "https://db-api-v2.akwaabasoftware.com/clients"

    today = datetime.date.today()
    # last_paid = datetime.datetime.today().strftime("%Y-%m-%d")
    year = datetime.datetime.now().year
    # today = datetime.datetime.now()
    year = str(year) + "0000"


    url = base_url + "/account?datatable_plugin&length=1000"

    payload = json.dumps({})

    headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=xuw6ruEorE0efPI1r7eypD46F5gkVdJjDCnpUCBqpeDPR799G7V4h5GRIoOfer5R; sessionid=ij0kr81ryje5mijdenssrwt3coffqw4z'
    }


    response = requests.request("GET", url, headers=headers, data=payload).json()['data']

    arr = [x['name'] for x in response]
    clieds = [x['id'] for x in response]
    modules = []


    # print(len(arr))

    allids = zip(arr, clieds)



    if request.method == "POST":

        client_id = request.POST.get('client')


        verify_url = "https://db-api-v2.akwaabasoftware.com/clients/hash-hash"

        payload = json.dumps({"accountId": f"{client_id}"})

        headers = {
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=8YuU53R4y1D2lrQUjxTrgGYymWbu7epD; sessionid=9mphxmdyzsna3si16qtwiidc3g3j9mfu'
        }

        token = requests.request("POST", verify_url, headers=headers, data=payload).json()['token']        

        url = f"https://db-api-v2.akwaabasoftware.com/clients/account/{client_id}"

        payload = json.dumps({})

        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {token}',
        'Cookie': 'csrftoken=xZi0YWasylnr7fm2DxgCEXnk6uhZr30m; sessionid=uhx3mg7b0lxg42w1kz8fq6r4ghu9al79'
        }

        response = requests.request("GET", url, headers=headers, data=payload).json()['data']

        client_name = response['name']
        
        try:
            usercode = AgentClients.objects.get(pid=client_id).usercode
        except:
            usercode = None

        module_ids = request.POST.getlist('foo[]') 

        for id in module_ids:
            modules.append(Modules.objects.get(id=id))

        membership_size=request.POST.get('membership_size')
 

        duration=request.POST.get('duration') if request.POST.get('duration') != "" else 0
        renewing_days=request.POST.get('renewing_days')
        remaining_days=request.POST.get('remaining_days')
        expiring_days=request.POST.get('expiring_days')

        subscription_fee_usd=request.POST.get('subscription_fee_usd')
        subscription_fee_usd = round(float(subscription_fee_usd), 2)

        subscription_fee_ghs=request.POST.get('subscription_fee_ghs')
        subscription_fee_ghs = round(float(subscription_fee_ghs), 2)


        solution = {}
        quiz = dict()
  
        expires_on =  today + datetime.timedelta(days=(int(renewing_days)))

        try:
            sub_fee = AccountSubscription.objects.get(client_id=client_id)

            sub_fee.client=client_name
            sub_fee.membership_size=membership_size
            sub_fee.duration=duration
            sub_fee.renewing_days += int(renewing_days)
            sub_fee.remaining_days=remaining_days
            sub_fee.expired_days=expiring_days
            sub_fee.subscription_fee_usd=subscription_fee_usd
            sub_fee.subscription_fee_ghs=subscription_fee_ghs
            sub_fee.description="Subscription"
            sub_fee.usercode=usercode
            sub_fee.date_created = timezone.now()
            sub_fee.confirmed=True
               
            expires_on = sub_fee.expires_on + datetime.timedelta(days=(int(renewing_days)))
            
            sub_fee.save()

            for i in module_ids:
                sub_fee.submodules.add(Modules.objects.get(id=i))
                
            sub_fee.save()


            subss = Subscriptions.objects.get(client_id=client_id)
            subss.subscribed_modules = {}
            subss.save()

            solution = sub_fee.modules 

            for module in modules:
                try:
                    database_obj = datetime.datetime.strptime(sub_fee.modules['Database Manager']['expires_on'], '%d-%m-%Y')
                except:
                    database_obj = datetime.datetime.strptime(sub_fee.modules['Database Manager']['expires_on'], '%Y-%m-%dT%H:%M:%SZ')    

                try:
                    try:
                        new_date_obj = datetime.datetime.strptime(sub_fee.modules[module.module]['expires_on'], '%d-%m-%Y') + datetime.timedelta(days=int(renewing_days)) 
                    except:
                        new_date_obj = datetime.datetime.strptime(sub_fee.modules[module.module]['expires_on'], '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(days=int(renewing_days))                    

                    if "Database" not in module.module:
                        try:
                            try:
                                database_obj = datetime.datetime.strptime(sub_fee.modules['Database Manager']['expires_on'], '%d-%m-%Y')
                            except:
                                database_obj = datetime.datetime.strptime(sub_fee.modules['Database Manager']['expires_on'], '%Y-%m-%dT%H:%M:%SZ')    
                        except:
                            database_obj = expires_on


                        if new_date_obj > database_obj:
                            new_date_obj = database_obj 
                    else:
                        sub_fee.expires_on = new_date_obj
                        sub_fee.save()  


                    quiz = {
                            "module_id": module.id,
                            "module_name": module.module,
                            "expires_on": new_date_obj.strftime("%d-%m-%Y"),
                            "amount_paid": subscription_fee_ghs,
                        }


                except:

                    date_str = f"{expires_on}"
                    date_obj = datetime.datetime.fromisoformat(date_str.replace("+00:00", ""))
                    expires_on = date_obj.replace(tzinfo=None)

                    if expires_on > database_obj:
                        expires_on = database_obj 

                    quiz = {
                            "module_id": module.id,
                            "module_name": module.module,
                            "expires_on": expires_on.strftime("%d-%m-%Y"),
                            "amount_paid": subscription_fee_ghs,
                        }

                    
                solution[module.module] = quiz
            
            
            sub_fee.modules =  solution
            sub_fee.invoice_no =  invoice_no
            sub_fee.save()


            subss.subscribed_modules = solution
            subss.client=client_name
            subss.subscription_id=invoice_no
            subss.confirmed=True
            subss.save()


        except:

            sub_fee = AccountSubscription(
                client_id=client_id,
                client=client_name,
                membership_size=membership_size,
                duration=duration,
                renewing_days=renewing_days,
                remaining_days=remaining_days,
                expired_days=expiring_days,
                subscription_fee_usd=subscription_fee_usd,
                subscription_fee_ghs=subscription_fee_ghs,
                description="Subscription",
                usercode=usercode,
                confirmed=True
                )
            sub_fee.save()
            sub_fee.expires_on = today + datetime.timedelta(days=(int(renewing_days)))
            sub_fee.save() 


            for i in module_ids:
                sub_fee.submodules.add(Modules.objects.get(id=i))
                
            sub_fee.save()    


            subss = Subscriptions.objects.create(client_id=client_id)
            subss.subscribed_modules = {}
            subss.save()


            for module in modules:

                quiz = {
                        "module_id": module.id,
                        "module_name": module.module,
                        "expires_on": expires_on.strftime("%d-%m-%Y"),
                        "amount_paid": subscription_fee_ghs,
                }
                    
                    
                solution[module.module] = quiz


            sub_fee.invoice_no =  invoice_no
            sub_fee.modules = solution
            sub_fee.expires_on = expires_on
            sub_fee.save()


            subss.client=client_name
            subss.subscription_id=invoice_no
            subss.subscribed_modules=solution
            subss.confirmed=True
            subss.save()


        messages.success(request, 'Subscription done successfully!')
        return HttpResponseRedirect(reverse('superuser:subscriptionHistory'))  
    else:    
        return render(request, template_name, {
            'modes':modes,
            'arr':allids,
            
            'session_id':session_id,
            'account_name':account_name,
            'branch':branch,
        })




def load_amount(request):
    template_name = 'superuser/amount.html'
    api_key ='e660c7f73ca24b041ceee820'
    amount = 0

    if request.method == 'POST': 
        ids = request.POST.getlist('id[]')
        size = request.POST.get('size')
        dur_type = request.POST.get('dur_type')
        
        duration = request.POST.get('duration')
        duration = int(duration) 

        # print(size)
        # print(type(size))

        for x in ids:

            try:
                module = ModuleFee.objects.filter(module=x, membership_size__icontains=size).first()
                # print(module)
                
                per_day = round((int(module.unit_fee_usd) / 30), 2)
               

                if dur_type == "months":
                    if module.promo == True and int(module.promo_duration) == duration:
                        # print("Promo")
                        summer = (int(module.unit_fee_usd) * duration) - ((int(module.promo_discount) / 100) * (int(module.unit_fee_usd) * duration))
                        amount += summer

                    else:
                        # print("No promotion")
                        amount += int(module.unit_fee_usd) * duration


                elif dur_type == "days":

                    if module.promo == True and int(module.promo_duration) == duration:
                        # print("Promo")
                        summer = (per_day * duration) - ((int(module.promo_discount) / 100) * (per_day * duration))
                        amount += summer

                    else:
                        # print("No promotion")
                        amount += per_day * duration   
            except:
                amount = 0
                # print("An error occured")    

     
        # print(duration)
        # print(dur_type)

        payload = json.dumps({})
        url = f'https://v6.exchangerate-api.com/v6/{api_key}/pair/USD/GHS/{amount}'

        headers = {}
            # result.conversion_result

        response = requests.request("GET", url, headers=headers, data=payload).json()['conversion_result']
        # response = 10
        # print(response)
        # print(amount)

        return render(request, template_name, {'amount': amount, 'response':response})




def load_cost(request):
    template_name = 'superuser/cost.html'
    api_key ='66d4824684db8ea0ab67fa76'
    amount = 0

    if request.method == 'POST': 
        ids = request.POST.getlist('id[]')
        size = request.POST.get('size')
        
        # duration = request.POST.get('duration')
        # duration = int(duration) 


        for x in ids:
            try:
                module = ModuleFee.objects.filter(module=x, membership_size=size).first()

                summer = (int(module.unit_fee_usd))
                amount += summer
 
            except:
                amount = 0
                


        payload = json.dumps({})
        url = f'https://v6.exchangerate-api.com/v6/{api_key}/pair/USD/GHS/{amount}'

        headers = {}
            # result.conversion_result

        response = requests.request("GET", url, headers=headers, data=payload).json()['conversion_result']
        # print(response)

        return render(request, template_name, {'amount': amount, 'response':response})




# Delete fee type
def deleteSpecialModuleFee(request, id, *args, **kwargs):
    # admin = user['firstname'] +' '+ user['surname']

    if request.method == "POST":
        invoice_no = request.POST.get('invoice_no')

        mode = SpecialModuleFee.objects.get(id=id)
        mode.delete()

        try:
            invoice = Subscriptions.objects.get(subscription_id=invoice_no)
            invoice.delete()
        except:
            pass 


        activity = ActivityLog(user='admin', action=f'deleted module fee {mode}')    
        activity.save()

    messages.success(request, 'Module deleted successfully!')
    return HttpResponseRedirect(reverse('superuser:viewModules')) 



def specialSubscription(request):
    template_name = 'superuser/special-subscription.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch
    now = datetime.datetime.now()

    invoice_no = remove_non_numeric(str(now))

    modes = Modules.objects.filter(default=False)
    sizes = MembershipSizes.objects.all()
    base_url = "https://db-api-v2.akwaabasoftware.com/clients"

    today = datetime.date.today()
    # last_paid = datetime.datetime.today().strftime("%Y-%m-%d")
    year = datetime.datetime.now().year
    # today = datetime.datetime.now()
    year = str(year) + "0000"


    url = base_url + "/account?datatable_plugin&length=1000"

    payload = json.dumps({})

    headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=xuw6ruEorE0efPI1r7eypD46F5gkVdJjDCnpUCBqpeDPR799G7V4h5GRIoOfer5R; sessionid=ij0kr81ryje5mijdenssrwt3coffqw4z'
    }

    # response = requests.request("GET", url, headers=headers, data=payload).json()['data']
    response = requests.request("GET", url, headers=headers, data=payload).json()['data']

    arr = []
    clieds = []
    modules = []

    for x in response:
        arr.append(x['name'])
        clieds.append(x['id'])

    # print(len(arr))

    allids = zip(arr, clieds)




    if request.method == "POST":

        client_id = request.POST.get('client')

        verify_url = "https://db-api-v2.akwaabasoftware.com/clients/hash-hash"

        payload = json.dumps({"accountId": f"{client_id}"})

        headers = {
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=8YuU53R4y1D2lrQUjxTrgGYymWbu7epD; sessionid=9mphxmdyzsna3si16qtwiidc3g3j9mfu'
        }

        token = requests.request("POST", verify_url, headers=headers, data=payload).json()['token']        

        url = f"https://db-api-v2.akwaabasoftware.com/clients/account/{client_id}"

        payload = json.dumps({})

        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {token}',
        'Cookie': 'csrftoken=xZi0YWasylnr7fm2DxgCEXnk6uhZr30m; sessionid=uhx3mg7b0lxg42w1kz8fq6r4ghu9al79'
        }

        response = requests.request("GET", url, headers=headers, data=payload).json()['data']

        client_name = response['name']
        
        try:
            usercode = AgentClients.objects.get(pid=client_id).usercode
        except:
            usercode = None



        module_ids = request.POST.getlist('foo[]') 

        for id in module_ids:
            modules.append(Modules.objects.get(id=id))

        membership_size=request.POST.get('membership_size')

        non_expiry = True if request.POST.get('non_expiry') else False

        duration=request.POST.get('duration') if request.POST.get('duration') != "" else 0

        renewing_days = 100000 if non_expiry else request.POST.get('renewing_days')
        remaining_days=request.POST.get('remaining_days')
        expiring_days=request.POST.get('expiring_days')


        subscription_fee_usd = request.POST.get('subscription_fee_usd')
        subscription_fee_usd = round(float(subscription_fee_usd), 2)

        subscription_fee_ghs=request.POST.get('subscription_fee_ghs')
        subscription_fee_ghs = round(float(subscription_fee_ghs), 2)

        annual_maintenance_fee=request.POST.get('maintenance_fee_ghs') if request.POST.get('maintenance_fee_ghs') else 0

        # promo = request.POST.get('promo')

        # if promo == "promo":
        #     promo = True
        #     promo_discount = request.POST.get('promo_discount')

        #     if promo_discount == "":
        #         promo_discount = 0


        #     amount_to_be_paid_usd = request.POST.get('amount_to_be_paid_usd')
        #     amount_to_be_paid_usd = round(float(amount_to_be_paid_usd), 2)

        #     amount_to_be_paid_ghs = request.POST.get('amount_to_be_paid_ghs')
        #     amount_to_be_paid_ghs = round(float(amount_to_be_paid_ghs), 2)
  
        # else:
        #     promo = False 
        #     promo_discount = 0

        #     amount_to_be_paid_usd = subscription_fee_usd
        #     amount_to_be_paid_ghs = subscription_fee_ghs 






        solution = {}
        quiz = dict()
  
        expires_on =  today + datetime.timedelta(days=(int(renewing_days)))

        try:
            sub_fee = AccountSubscription.objects.get(client_id=client_id)

            sub_fee.client=client_name
            sub_fee.membership_size=membership_size
            sub_fee.duration=duration
            sub_fee.renewing_days += int(renewing_days)
            sub_fee.remaining_days=remaining_days
            sub_fee.expired_days=expiring_days
            sub_fee.subscription_fee_usd=subscription_fee_usd
            sub_fee.subscription_fee_ghs=subscription_fee_ghs
            sub_fee.description="Subscription"
            sub_fee.usercode=usercode
            sub_fee.date_created = timezone.now()
            sub_fee.confirmed=True
            sub_fee.special=True
            sub_fee.non_expiry=non_expiry
            sub_fee.annual_maintenance_fee=annual_maintenance_fee
               
            expires_on = sub_fee.expires_on + datetime.timedelta(days=(int(renewing_days)))
            
            sub_fee.save()

            for i in module_ids:
                sub_fee.submodules.add(Modules.objects.get(id=i))
                
            sub_fee.save()


            subss = Subscriptions.objects.get(client_id=client_id)
            subss.subscribed_modules = {}
            subss.save()

            solution = sub_fee.modules 


            for module in modules:

                try:
                    database_obj = datetime.datetime.strptime(sub_fee.modules['Database Manager']['expires_on'], '%d-%m-%Y')
                except:    
                    database_obj = datetime.datetime.strptime(sub_fee.modules['Database Manager']['expires_on'], '%Y-%m-%dT%H:%M:%SZ')

                try:
                    try:
                        new_date_obj = datetime.datetime.strptime(sub_fee.modules[module.module]['expires_on'], '%d-%m-%Y') + datetime.timedelta(days=int(renewing_days))                
                    except:
                        new_date_obj = datetime.datetime.strptime(sub_fee.modules[module.module]['expires_on'], '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(days=int(renewing_days))                


                    if "Database" not in module.module:
                        try:
                            try:
                                database_obj = datetime.datetime.strptime(sub_fee.modules['Database Manager']['expires_on'], '%d-%m-%Y')
                            except:
                                database_obj = datetime.datetime.strptime(sub_fee.modules['Database Manager']['expires_on'], '%Y-%m-%dT%H:%M:%SZ')  
                        except:
                            database_obj = expires_on

                        if new_date_obj > database_obj:
                            new_date_obj = database_obj 
                    else:
                        sub_fee.expires_on = new_date_obj
                        sub_fee.save()  


                    quiz = {
                            "module_id": module.id,
                            "module_name": module.module,
                            "expires_on": new_date_obj.strftime("%d-%m-%Y"),
                            "amount_paid": subscription_fee_ghs,
                        }


                except:

                    date_str = f"{expires_on}"
                    date_obj = datetime.datetime.fromisoformat(date_str.replace("+00:00", ""))
                    expires_on = date_obj.replace(tzinfo=None)

                    if expires_on > database_obj:
                        expires_on = database_obj 

                    quiz = {
                            "module_id": module.id,
                            "module_name": module.module,
                            "expires_on": expires_on.strftime("%d-%m-%Y"),
                            "amount_paid": subscription_fee_ghs,
                        }

                    
                solution[module.module] = quiz
            
            
            sub_fee.modules =  solution
            sub_fee.invoice_no = invoice_no
            sub_fee.save()


            subss.subscribed_modules = solution
            subss.client=client_name
            subss.subscription_id=invoice_no
            subss.confirmed=True
            subss.save()


        except:

            sub_fee = AccountSubscription(
                client_id=client_id,
                client=client_name,
                membership_size=membership_size,
                duration=duration,
                renewing_days=renewing_days,
                remaining_days=remaining_days,
                expired_days=expiring_days,
                subscription_fee_usd=subscription_fee_usd,
                subscription_fee_ghs=subscription_fee_ghs,
                description="Subscription",
                usercode=usercode,
                confirmed=True,
                special=True,
                non_expiry=non_expiry,
                annual_maintenance_fee=annual_maintenance_fee
                )
            sub_fee.save()
            sub_fee.expires_on = today + datetime.timedelta(days=(int(renewing_days)))
            sub_fee.save() 


            for i in module_ids:
                sub_fee.submodules.add(Modules.objects.get(id=i))
                
            sub_fee.save()    


            subss = Subscriptions.objects.create(client_id=client_id)
            subss.subscribed_modules = {}
            subss.save()


            for module in modules:

                quiz = {
                        "module_id": module.id,
                        "module_name": module.module,
                        "expires_on": expires_on.strftime("%d-%m-%Y"),
                        "amount_paid": subscription_fee_ghs,
                }
                    
                    
                solution[module.module] = quiz


            sub_fee.invoice_no =  invoice_no
            sub_fee.modules = solution
            sub_fee.expires_on = expires_on
            sub_fee.save()


            subss.client=client_name
            subss.subscription_id=invoice_no
            subss.subscribed_modules=solution
            subss.confirmed=True
            subss.save()
            
        messages.success(request, 'Special subscription done successfully!')
        return HttpResponseRedirect(reverse('superuser:specialSubscriptionHistory')) 

    else:    
        return render(request, template_name, {
            'modes':modes,
            'arr':allids,
            'sizes':sizes,
            'session_id':session_id,
            'account_name':account_name,
            'branch':branch,
        })






def specialSubscriptionHistory(request, **kwargs):
    template_name = 'superuser/special-history.html'

    today = timezone.now()

    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)
    account_name = details.account_name
    branch = details.branch
    client_id = details.pid
    token = details.token
    

    if request.method == 'POST':
        modules = request.POST.getlist('modules[]')
        subscription_id = request.POST.get('subscription_id')

        account = AccountSubscription.objects.get(id=subscription_id)
        subscription = Subscriptions.objects.get(client_id=account.client_id) 
        
        database = False

        for x in modules:
            if "Database" in Modules.objects.get(id=x).module:
                database = True


        if database:
            account.delete()
            subscription.delete()

        else:
            for y in modules:
                del account.modules[Modules.objects.get(id=y).module]
                del subscription.subscribed_modules[Modules.objects.get(id=y).module]
                account.save()
                subscription.save()


        messages.success(request, 'Module(s) unsubscribed successfully')
        return HttpResponseRedirect(reverse('superuser:specialSubscriptionHistory')) 


    else:
        histories = AccountSubscription.objects.filter(confirmed=True, special=True)

        for x in histories:
            if today > x.expires_on:
                x.expired = True
            else:
                x.expired = False

            x.save()    
        

        return render(request, template_name, {
            # 'history_filter': history_filter, 
            'histories': histories, 
            'today': today, 
            'pid': client_id,
            'session_id':session_id,
            'account_name':account_name,
            'branch':branch,
        }) 






def allClients(request):
    
    template_name = 'superuser/clients.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch

    base_url = "https://db-api-v2.akwaabasoftware.com/clients"
    url = base_url + "/account?length=1000&datatable_plugin&archive=0"

    payload = json.dumps({})

    headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=Hf5Wd7yKmiDjeyREEwvlbZUZzfYR1vzVYaUpdIO01NjhxGBEM19MJTn2ioMrJbBI; sessionid=ca7rumjb8xhn9md452xwgsv7zwgvjzq2'
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()['data']


    return render(request, template_name, {
        'response': response,
                'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
    })



def archivedClients(request):
    
    template_name = 'superuser/archived-clients.html'

    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch


    base_url = "https://db-api-v2.akwaabasoftware.com/clients"
    url = base_url + "/account?length=500&datatable_plugin&archive=1"

    payload = json.dumps({})

    headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=Hf5Wd7yKmiDjeyREEwvlbZUZzfYR1vzVYaUpdIO01NjhxGBEM19MJTn2ioMrJbBI; sessionid=ca7rumjb8xhn9md452xwgsv7zwgvjzq2'
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()['data']


    return render(request, template_name, {
        'response': response,
                'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
    })



# def viewClient(request, id):
#     template_name = "superuser/view-client.html"

#     return render(request, template_name, {

#     })


def viewClient(request, **kwargs):
    
    template_name = 'superuser/view-client.html'

    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = kwargs.get('client_id')
 
    account_name = details.account_name
    branch = details.branch

    url = "https://db-api-v2.akwaabasoftware.com/clients/hash-hash"

    payload = json.dumps({
    "accountId": client_id
    })

    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=1OPH0wWok2QOkHyrkq7nRqwdl7GbDkmH; sessionid=3j739a19sx6igxmn5n2fan65u3aa1115'
    }

    token = requests.request("POST", url, headers=headers, data=payload).json()['token']


    url = f"https://db-api-v2.akwaabasoftware.com/clients/account/{client_id}"
    
    headers = {
                'Authorization': f'Token {token}',
                'Content-Type': 'application/json',
                'Cookie': 'csrftoken=4qQVgGyOrmGlgdMwQwsuRh9jmnTOyPSbjOI6Vm4VQLxX9O7gKkWr3DufNXYd7RVH; sessionid=0e2td1b1uzn4cjb5naw9bjw1hs9sjzxw'
                }

    response = requests.request("GET", url, headers=headers).json()['data']



    return render(request, template_name, {
        'response': response,
        'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
    })











def registerClient(request):
    template_name = 'superuser/register-client.html'

    base_url = "https://db-api-v2.akwaabasoftware.com"


    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch


    region_url = base_url + "/locations/region"
    account_url = base_url + "/generic/account-type"
    country_url = base_url + "/locations/country"
    category_url = base_url + "/clients/account-category"


    payload={}
    headers = {
    'Authorization': f'Token {token}',
    'Cookie': 'csrftoken=UN5qKQ1rbg40wB0OWDXyWbO612Lvx41Bb2o0xCYkNfcrhrdvUpxgSYkXDBneGvMT; sessionid=ij0kr81ryje5mijdenssrwt3coffqw4z'
    }


    categories = requests.request("GET", category_url, headers=headers, data=payload).json()['data']
    # print(categories)


    regions = requests.request("GET", region_url, headers=headers, data=payload).json()
    # id and location

    accounts = requests.request("GET", account_url, headers=headers, data=payload).json()['data']
    # id and name

    countries = requests.request("GET", country_url, headers=headers, data=payload).json()
    # id and name


    membership_sizes = MembershipSizes.objects.all()
   

    # id and size

 
    return render(request, template_name,{
        'regions': regions,
        'membership_sizes': membership_sizes,
        'accounts': accounts,
        'countries': countries,
        'categories': categories,
        'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
    })  





def load_sizes(request):
    template_name = 'superuser/sizes.html'

    if request.method == 'GET': 
        client_id = request.GET.get('client_id')
        client_name = request.GET.get('client_name')
        size_id = request.GET.get('size_id')
        pid = request.GET.get('pid')
        

        size = MembershipSizes.objects.get(id=size_id)

        try:
            client_size = ClientSizes.objects.get(client_id=client_id)
            client_size.client_name=client_name
            client_size.size=size.size
            client_size.client_size=size
            client_size.pid=pid
            client_size.save()

        except:
            client_size = ClientSizes.objects.create(
                client_id=client_id,
                client_name=client_name,
                size=size.size,
                client_size=size,
                pid=pid,
            )
            client_size.save()

        response = ""    

        return render(request, template_name, {'response': response})




def load_districts(request):
    template_name = 'superuser/districts.html'
    base_url = "https://db-api-v2.akwaabasoftware.com"


    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch

    if request.method == 'GET': 
        region_id = request.GET.get('region_id')

        url = base_url + f"/locations/district/filter/{region_id}"

        payload={}
        
        headers = {
        'Authorization': f'Token {token}',
        'Cookie': 'csrftoken=UN5qKQ1rbg40wB0OWDXyWbO612Lvx41Bb2o0xCYkNfcrhrdvUpxgSYkXDBneGvMT; sessionid=ij0kr81ryje5mijdenssrwt3coffqw4z'
        }

        districts = requests.request("GET", url, headers=headers, data=payload).json()
        # id and location

        return render(request, template_name, {'districts': districts})




def load_constituencies(request):
    template_name = 'superuser/constituencies.html'


    base_url = "https://db-api-v2.akwaabasoftware.com"

    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch

    if request.method == 'GET': 
        region_id = request.GET.get('region_id')
        district_id = request.GET.get('district_id')

        url = base_url + f"/locations/constituency/filter/{region_id}/{district_id}"

        payload={}
        
        headers = {
        'Authorization': f'Token {token}',
        'Cookie': 'csrftoken=UN5qKQ1rbg40wB0OWDXyWbO612Lvx41Bb2o0xCYkNfcrhrdvUpxgSYkXDBneGvMT; sessionid=ij0kr81ryje5mijdenssrwt3coffqw4z'
        }

        constituencies = requests.request("GET", url, headers=headers, data=payload).json()
        # id and location

        return render(request, template_name, {'constituencies': constituencies})









# def activateClient(request)
def activateClient(request):
    
    template_name = 'superuser/activate-client.html'
    base_url = "https://db-api-v2.akwaabasoftware.com/clients"
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch


    today = datetime.date.today()
    year = datetime.datetime.now().year
    year = str(year) + "0000"

    url = base_url + "/account?datatable_plugin&length=1000"

    payload = json.dumps({})

    headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=xuw6ruEorE0efPI1r7eypD46F5gkVdJjDCnpUCBqpeDPR799G7V4h5GRIoOfer5R; sessionid=ij0kr81ryje5mijdenssrwt3coffqw4z'
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()['data']

    arr = []
    clieds = []
    paid = []


    for x in response:
        arr.append(x['name'])
        clieds.append(x['id'])
        try:
            paid.append(OneTimeDetails.objects.get(client_id=x['id']).paid)
        except:
            paid.append("False")   

    allids = zip(arr, clieds, paid)


    return render(request, template_name, {
        'arr':allids,
                        'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
    })







# Delete fee type
def load_onetime(request):
    template_name = 'superuser/onetime.html'
    today = datetime.date.today()

    if request.method == 'GET': 
        client_id = request.GET.get('client_id')

        period = ActivationFee.objects.all().first().duration
        
        expires_on =  today + datetime.timedelta(days=(int(period)))

        try:
            subscribers = OneTimeDetails.objects.get(client_id=client_id, paid=True)
        except:
            subscribers = OneTimeDetails.objects.create(client_id=client_id, paid=True, expires_on=expires_on)
            subscribers.save()


        return render(request, template_name, {

        })




# Delete fee type
def load_commission(request):
    template_name = 'superuser/commission.html'

    if request.method == 'GET': 
        commission_id = request.GET.get('commission_id')
        info = request.GET.get('info')

        if info == 'single':
            commission = AgentsCommission.objects.get(id=commission_id)
            commission.paid = True
            commission.status = "Paid"
            commission.save()

            total_commission = TotalCommission.objects.get(usercode=commission.usercode)
            total_commission.amount = 0.00
            total_commission.paid = True
            total_commission.status = "Paid"
            total_commission.save()

        else:
            for commission in AgentsCommission.objects.all():
                commission.paid = True
                commission.status = "Paid"
                commission.save()

             
            for total_commission in TotalCommission.objects.all():
                total_commission.amount = 0.00
                total_commission.paid = True
                total_commission.status = "Paid"
                total_commission.save()
                    

        return render(request, template_name, {})







def createServiceFees(request):

    template_name = 'superuser/create-service-fees.html'
    base_url = "https://db-api-v2.akwaabasoftware.com/clients"

    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch

    today = datetime.date.today()
    year = datetime.datetime.now().year
    year = str(year) + "0000"

    url = base_url + "/account?datatable_plugin&length=1000"

    payload = json.dumps({})

    headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=xuw6ruEorE0efPI1r7eypD46F5gkVdJjDCnpUCBqpeDPR799G7V4h5GRIoOfer5R; sessionid=ij0kr81ryje5mijdenssrwt3coffqw4z'
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()['data']

    arr = []
    clieds = []

    for x in response:
        arr.append(x['name'])
        clieds.append(x['id'])

    allids = zip(arr, clieds)



    if request.method == 'POST':
        client_id = request.POST.get('client')

        client_url = f'{base_url}/account?id={client_id}'

        payload = json.dumps({})

        headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=i0QCkPPQCUAYcsvB4MvYAfzl4HrLL0GJ'
        }

        response = requests.request("GET", client_url, headers=headers, data=payload).json()['results'][0]

        client = response['name']

        service_fee = request.POST.get('service_fee')
        limit = request.POST.get('limit')


        try:
            service = ServiceFee.objects.get(client_id=client_id)
            service.client = client
            service.service_fee = service_fee
            service.limit = limit
            service.save()
        except:
            service = ServiceFee.objects.create(client_id=client_id, client=client, service_fee=service_fee, limit=limit)
            service.save()
        

        activity = ActivityLog(user="admin", action=f'created service fee for {client}')    
        activity.save()

        messages.success(request, 'Service Fee created successfully!')
        return HttpResponseRedirect(reverse('superuser:viewServiceFees')) 

    else:
        return render(request, template_name, {
            'arr':allids,
                            'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
        })




# View fee type
def viewServiceFees(request):

    template_name = 'superuser/view-service-fees.html'

    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch


    service_fees=ServiceFee.objects.all()
    total_outstanding = 0
    try:
        outstanding = [float(x.outstanding_fee) for x in ServiceFee.objects.all()]

        for x in outstanding:
            total_outstanding += x
    except:
        total_outstanding = 0.00  


    return render(request, template_name, {
        'service_fees': service_fees,
        'total_outstanding': total_outstanding,
                        'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
    })




# Edit fee type
def editServiceFees(request, id):
    # if ClientDetails.objects.count() > 0:
    #     admin = user['firstname'] +' '+ user['surname']

    template_name = 'superuser/edit-service-fees.html'

    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch

    detail = ServiceFee.objects.get(id=id)

    details=ServiceFee.objects.all()
    
    if request.method == 'POST':
        detail.service_fee = request.POST.get('service_fee')
        detail.limit = request.POST.get('limit')
        detail.save()

        activity = ActivityLog(user='admin', action=f'edited service fee')    
        activity.save()

        messages.success(request, 'Service Fee edited successfully!')

        return HttpResponseRedirect(reverse('superuser:viewServiceFees')) 


    return render(request, template_name, {
        'detail': detail,
        'details': details,
                        'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
    }) 





# Delete fee type
def deleteServiceFees(request, id, *args, **kwargs):

    if request.method == "POST":
        mode = ServiceFee.objects.get(id=id)
        mode.delete()

        activity = ActivityLog(user='admin', action=f'deleted service fees for {mode.client}')    
        activity.save()

    messages.success(request, 'Service Fees deleted successfully!')
    return HttpResponseRedirect(reverse('superuser:viewServiceFees')) 









# Fee Type Views
# Create Fee types
def createAgent(request):

    template_name = 'superuser/create-agent.html'
    base_url = "https://db-api-v2.akwaabasoftware.com"
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)
 
    account_name = details.account_name
    branch = details.branch
    pid = details.pid
    token = details.token

    payload = json.dumps({})


    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=UN5qKQ1rbg40wB0OWDXyWbO612Lvx41Bb2o0xCYkNfcrhrdvUpxgSYkXDBneGvMT; sessionid=ij0kr81ryje5mijdenssrwt3coffqw4z'
    }


    country_url = base_url + "/locations/country"
    countries = requests.request("GET", country_url, headers=headers, data=payload).json()
    # id and name


    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        account = request.POST.get('account')
        country = request.POST.get('country')
        gender = request.POST.get('gender')
        activation_commission = request.POST.get('activation_commission')
        renewal_commission = request.POST.get('renewal_commission')

        profile = request.FILES.get('profile')
        card = request.FILES.get('card')

        usercode = secrets.token_hex(16)
        link = f"https://signup.akwaabasoftware.com/{usercode}/"


        try:
            emailx = Agents.objects.get(email=email)

            messages.error(request, 'Agent already exists!')
            return HttpResponseRedirect(reverse('superuser:viewAgents'))

        except: 

            agent = Agents.objects.create(
                firstname=firstname, 
                surname=surname, 
                email=email,
                password=make_password(contact), 
                contact=contact, 
                account=account, 
                country=country,
                activation_commission=activation_commission, 
                renewal_commission=renewal_commission, 
                profile=profile,
                card=card, 
                usercode=usercode,
                pid=pid,
                account_name=account_name,
                branch=branch,
                token=token,
                gender=gender,
                link=link
                )
            
            agent.save()

            messages.success(request, 'Agent created successfully!')
            return HttpResponseRedirect(reverse('superuser:viewAgents')) 
    else:
        return render(request, template_name, {
                'session_id':session_id,
                'account_name':account_name,
                'branch':branch,
                'countries':countries,

        })



def viewAgents(request):

    template_name = 'superuser/view-agents.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id) 
    account_name = details.account_name
    branch = details.branch


    return render(request, template_name, {
        'agents': Agents.objects.all(),
        'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
    })



def viewAgent(request, id):
    # if ClientDetails.objects.count() > 0:

    template_name = 'superuser/view-agent.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)
    account_name = details.account_name
    branch = details.branch


    # agent = Agents.objects.get(id=id)
 

    return render(request, template_name, {
        'agent': Agents.objects.get(id=id),
        'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
    })



# Edit fee type
def editAgent(request, id):

    template_name = 'superuser/edit-agent.html'
    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    base_url = "https://db-api-v2.akwaabasoftware.com"
    payload = json.dumps({})


    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=UN5qKQ1rbg40wB0OWDXyWbO612Lvx41Bb2o0xCYkNfcrhrdvUpxgSYkXDBneGvMT; sessionid=ij0kr81ryje5mijdenssrwt3coffqw4z'
    }


    country_url = base_url + "/locations/country"
    countries = requests.request("GET", country_url, headers=headers, data=payload).json()
 
    account_name = details.account_name
    branch = details.branch

    agent = Agents.objects.get(id=id)
    
    if request.method == 'POST':
        agent.firstname = request.POST.get('firstname')
        agent.surname = request.POST.get('surname')
        agent.email = request.POST.get('email')
        agent.contact = request.POST.get('contact')
        agent.gender = request.POST.get('gender')
        agent.account = request.POST.get('account')
        agent.country = request.POST.get('country') if request.POST.get('country') != "" else agent.country
        agent.activation_commission = request.POST.get('activation_commission')
        agent.renewal_commission = request.POST.get('renewal_commission')

        new_profile = request.FILES.get('profile', None)
        if new_profile is not None:
            agent.profile = request.FILES.get('profile', None)

        new_card = request.FILES.get('card', None)
        if new_card is not None:
            agent.card = request.FILES.get('card', None)


        agent.save()

        # activity = ActivityLog(user=admin, action=f'edited fee type {fee_type}')    
        # activity.save()

        messages.success(request, 'Agent details edited successfully!')

        return HttpResponseRedirect(reverse('superuser:viewAgents')) 


    return render(request, template_name, {
        'agent': agent,
        'agents': Agents.objects.all(),
        'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
        'countries':countries,
    }) 

    # else:
    #     messages.error(request, 'Please Login to continue') 
    #     return HttpResponseRedirect(reverse('login:login'))



# Delete fee type
def deleteAgent(request, id, *args, **kwargs):
    # admin = user['firstname'] +' '+ user['surname']

    if request.method == "POST":
        fee_type = Agents.objects.get(id=id)
        fee_type.delete()

        # activity = ActivityLog(user=admin, action=f'deleted fee type {fee_type}')    
        # activity.save()

    messages.success(request, 'Agent deleted successfully!')
    return HttpResponseRedirect(reverse('superuser:viewAgents')) 


    

def viewCommissions(request):
    template_name = 'superuser/commissions.html'
    today = datetime.date.today()

    session_id = request.COOKIES.get('session_id')
    details = AdminDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch


    payments=AgentsCommission.objects.all()
    
    try:
        total_commission = sum([x.amount for x in TotalCommission.objects.all()])
    except:
        total_commission = 0.00 


    return render(request, template_name, {
        'payments': payments, 
        'today': today,
        'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
        'total_commission': total_commission,
        }) 




def viewProfile(request, **kwargs):

    template_name = 'superuser/profile.html'
    session_id = request.COOKIES.get('session_id')

    details = AdminDetails.objects.get(session_id=session_id)
    client_id = details.pid
    token = details.token
    account_name = details.account_name
    branch = details.branch

    url = f"https://db-api-v2.akwaabasoftware.com/clients/account/{client_id}"
    
    headers = {
                'Authorization': f'Token {token}',
                'Content-Type': 'application/json',
                'Cookie': 'csrftoken=4qQVgGyOrmGlgdMwQwsuRh9jmnTOyPSbjOI6Vm4VQLxX9O7gKkWr3DufNXYd7RVH; sessionid=0e2td1b1uzn4cjb5naw9bjw1hs9sjzxw'
                }

    response = requests.request("GET", url, headers=headers).json()['data']
    # print(response)

    return render(request, template_name, {'response': response, 'pid':client_id,
                'branch':branch,
            'account_name':account_name, 'session_id':session_id})




def logout(request, id):
    
    response = HttpResponse("You have been logged out.")
    response.delete_cookie('session_id')

    subject = AdminDetails.objects.get(session_id=id)
    subject.delete()
    
    return redirect('login:login')


    