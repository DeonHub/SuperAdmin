import copy
import random
import string
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

from django.http import FileResponse
from django.core import serializers
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from api.models import Dasho
from superuser.filter import SetFeeFilter

from superuser.models import *
from login.models import *

from .models import *
import requests
import datetime
import json
import io
import os
import csv
import time
import base64

import environ

env = environ.Env()
environ.Env.read_env()



def index(request, **kwargs):
    template_name = 'client/index.html'

    session_id = request.COOKIES.get('session_id')
    details = ClientDetails.objects.get(session_id=session_id)
 
    account_name = details.account_name
    branch = details.branch
    client_id = details.pid
    usercode = details.usercode


    total_commission_earned = sum([x.amount for x in AgentsCommission.objects.filter(usercode=usercode)])
    total_commission_paid = sum([x.amount for x in AgentsCommission.objects.filter(usercode=usercode, paid=True)])
    total_clients = AgentClients.objects.filter(usercode=usercode).count()

    return render(request, template_name, {
        'pid': client_id,
        'account_name': account_name,
        'branch': branch,
        'session_id':session_id,
        'total_commission_earned':total_commission_earned,
        'total_commission_paid':total_commission_paid,
        'total_clients':total_clients,

    })



def random_char(y):
    return ''.join(random.choice(string.ascii_uppercase) for x in range(y))
    

def remove_non_numeric(string):
    return ''.join(filter(str.isdigit, string))
    


def load_bill(request):
    template_name = 'client/bill.html'

    session_id = request.COOKIES.get('session_id')
    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid

    usercode = details.usercode

    modules = []
    today = datetime.date.today()
    now = datetime.datetime.now()
    year = datetime.datetime.now().year
    year = str(year) + "0000"

    if request.method == "GET":

        client_id = request.GET.get('client_id')

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
        

        module_ids = request.GET.getlist('module_ids[]') 

        for id in module_ids:
            modules.append(Modules.objects.get(id=id))


        membership_size=request.GET.get('membership_size')

        subscription_id=request.GET.get('subscription_id')
 
        duration=request.POST.get('duration') if request.POST.get('duration') != "" else 0
        renewing_days=request.GET.get('renewing_days')
        remaining_days=request.GET.get('remaining_days')
        expiring_days=request.GET.get('expiring_days')

        subscription_fee_usd=request.GET.get('subscription_fee_usd')
        subscription_fee_usd = round(float(subscription_fee_usd), 2)

        subscription_fee_ghs=request.GET.get('subscription_fee_ghs')
        subscription_fee_ghs = round(float(subscription_fee_ghs), 2)






        if subscription_id:

            account = AccountSubscription.objects.get(id=id)
            detail_copy = copy.deepcopy(account)

            # Making a copy of the original one

            account_copy = AccountSubscriptionCopy.objects.create(
                    client_id=detail_copy.client_id,
                    client=detail_copy.client_name,
                    membership_size=detail_copy.membership_size,
                    duration=detail_copy.duration,
                    renewing_days=detail_copy.renewing_days,
                    remaining_days=detail_copy.remaining_days,
                    expired_days=detail_copy.expiring_days,
                    subscription_fee_usd=detail_copy.subscription_fee_usd,
                    subscription_fee_ghs=detail_copy.subscription_fee_ghs,
                    description="Subscription",
                    usercode=detail_copy.usercode,
                )
            
            account_copy.save()








            subscription = AccountSubscriptionCopy.objects.get(client_id=detail_copy.client_id)
            quiz = dict()

            invoice_no = remove_non_numeric(str(now))


            subscription.duration=duration
            subscription.renewing_days+= int(renewing_days)
            subscription.remaining_days=remaining_days
            subscription.expired_days=expiring_days

            subscription.subscription_fee_usd=subscription_fee_usd
            subscription.subscription_fee_ghs=subscription_fee_ghs
            subscription.description="Subscription"
            subscription.usercode=usercode
            subscription.invoice_no=invoice_no
            subscription.invoice_copy = invoice_no
            subscription.confirmed = False
            subscription.date_created = timezone.now()


            # try:
            #     subss = Subscriptions.objects.get(client_id=subscription.client_id)
            #     subss.subscribed_modules = {}
            #     subss.save()
                
            # except:
            #     subss = Subscriptions.objects.create(client_id=subscription.client_id)



            for module in modules:
                # new_date_obj = datetime.datetime.strptime(subscription.modules[module.module]['expires_on'], "%d-%m-%Y") + datetime.timedelta(days=int(renewing_days))   

                try:
                    new_date_obj = datetime.datetime.strptime(subscription.modules[module.module]['expires_on'], '%d-%m-%Y') + datetime.timedelta(days=int(renewing_days)) 
                except:
                    new_date_obj = datetime.datetime.strptime(subscription.modules[module.module]['expires_on'], '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(days=int(renewing_days))                    


                if "Database" not in module.module:

                    try:
                        # database_obj = datetime.datetime.strptime(subscription.modules['Database Manager']['expires_on'], "%d-%m-%Y")
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

            # subss.client = subscription.client
            # subss.subscription_id = subscription.invoice_no
            # subss.subscribed_modules = subscription.modules
            # subss.date_created = timezone.now()
            # subss.save()



        else: 

            account = AccountSubscription.objects.get(client_id=client_id)
            detail_copy = copy.deepcopy(account)

            # Making a copy of the original one

            account_copy = AccountSubscriptionCopy.objects.create(
                    client_id=detail_copy.client_id,
                    client=detail_copy.client_name,
                    membership_size=detail_copy.membership_size,
                    duration=detail_copy.duration,
                    renewing_days=detail_copy.renewing_days,
                    remaining_days=detail_copy.remaining_days,
                    expired_days=detail_copy.expiring_days,
                    subscription_fee_usd=detail_copy.subscription_fee_usd,
                    subscription_fee_ghs=detail_copy.subscription_fee_ghs,
                    description="Subscription",
                    usercode=detail_copy.usercode,
                )
            
            account_copy.save()



            solution = {}
            quiz = dict()

            invoice_no = remove_non_numeric(str(now))
    

            expires_on =  today + datetime.timedelta(days=(int(renewing_days)))

            try:
                sub_fee = AccountSubscriptionCopy.objects.get(client_id=client_id)

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
                sub_fee.confirmed = False
                sub_fee.date_created = timezone.now()
                
                expires_on = sub_fee.expires_on + datetime.timedelta(days=(int(renewing_days)))
                

                sub_fee.save()

                for i in module_ids:
                    sub_fee.submodules.add(Modules.objects.get(id=i))
                    
                sub_fee.save()

                solution = sub_fee.modules 

                for module in modules:

                    # database_obj = datetime.datetime.strptime(sub_fee.modules['Database Manager']['expires_on'], "%d-%m-%Y")
                    try:
                        database_obj = datetime.datetime.strptime(sub_fee.modules['Database Manager']['expires_on'], '%d-%m-%Y')
                    except:
                        database_obj = datetime.datetime.strptime(sub_fee.modules['Database Manager']['expires_on'], '%Y-%m-%dT%H:%M:%SZ')    


                    try:
                        # new_date_obj = datetime.datetime.strptime(sub_fee.modules[module.module]['expires_on'], "%d-%m-%Y") + datetime.timedelta(days=int(renewing_days))                

                        try:
                            new_date_obj = datetime.datetime.strptime(sub_fee.modules[module.module]['expires_on'], '%d-%m-%Y') + datetime.timedelta(days=int(renewing_days)) 
                        except:
                            new_date_obj = datetime.datetime.strptime(sub_fee.modules[module.module]['expires_on'], '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(days=int(renewing_days))


                        if "Database" not in module.module:
                            try:
                                # database_obj = datetime.datetime.strptime(sub_fee.modules['Database Manager']['expires_on'], "%d-%m-%Y")

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
                sub_fee.invoice_copy = invoice_no
                sub_fee.save()


            except:

                sub_fee = AccountSubscriptionCopy(
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
                    )
                sub_fee.save()
                sub_fee.expires_on = today + datetime.timedelta(days=(int(renewing_days)))
                sub_fee.save() 


                for i in module_ids:
                    sub_fee.submodules.add(Modules.objects.get(id=i))
                    
                sub_fee.save()    

                for module in modules:

                    quiz = {
                            "module_id": module.id,
                            "module_name": module.module,
                            "expires_on": expires_on.strftime("%d-%m-%Y"),
                            "amount_paid": subscription_fee_ghs,
                    }
                        
                        
                    solution[module.module] = quiz


                sub_fee.invoice_no = invoice_no
                sub_fee.invoice_copy = invoice_no
                sub_fee.modules = solution
                sub_fee.expires_on = expires_on
                sub_fee.save()



        try:
            account = AccountSubscription.objects.get(client_id=client_id)
            account.invoice_copy = invoice_no
            account.date_created = timezone.now()
            account.save()

        except:
            account = AccountSubscription.objects.create(client_id=client_id, invoice_copy=invoice_no)
            account.save()


        url = "https://payproxyapi.hubtel.com/items/initiate"

        # returnUrl = f"https://super.akwaabasoftware.com/client/subscription-history/"
        returnUrl = f"https://super.akwaabasoftware.com/client/subscription-history/"



        payload = json.dumps({
                "totalAmount": subscription_fee_ghs,
                # "totalAmount": 0.1,
                "description": "Module Subscription",
                "callbackUrl": "https://transactions.akwaabasoftware.com/add-transaction/",
                "returnUrl": returnUrl,
                "merchantAccountNumber": "2017254",
                "cancellationUrl": "https://hubtel.com/",
                "clientReference": invoice_no
            })


        headers = {
        'Authorization': 'Basic UDc5RVdSVzozNmZmNzk3YTgyMjU0NzJmOTA2ZGU0NGM3NGVkZWE0Zg==',
        'Content-Type': 'application/json'
        }


        response = requests.request("POST", url, headers=headers, data=payload).json()['data']['checkoutUrl']

        
        return render(request, template_name, {'response': response})



def load_items(request):
    template_name = 'client/test.html'

    if request.method == 'GET': 
        mode_id = request.GET.get('mode')
        module = Modules.objects.get(id=mode_id)


        try:
            module_detail = ModuleFee.objects.get(module=module)
            
        except:
            module_detail = ModuleFee.objects.filter(module=module).first()
            


        return render(request, template_name, {'mode': module_detail,})


def days_since_date(date_str):
    today = datetime.date.today()

    try:
        data = datetime.datetime.strptime(date_str, '%d-%m-%Y').date()
    except:
        data = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

    delta = today - data
    return delta.days


def load_expired(request):
    template_name = 'client/expired.html'

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



def load_time(request):
    template_name = 'client/time.html'
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


def load_amount(request):
    template_name = 'client/amount.html'
    api_key ='e660c7f73ca24b041ceee820'
    amount = 0

    if request.method == 'POST': 
        ids = request.POST.getlist('id[]')
        size = request.POST.get('size')
        dur_type = request.POST.get('dur_type')
        
        duration = request.POST.get('duration')
        duration = int(duration) 

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





def accountSubscription(request, **kwargs):
    template_name = 'user/account-subscription.html'
    session_id = request.COOKIES.get('session_id')

    token = kwargs.get('token')
    decoded_token = base64.b64decode(token).decode("utf-8")

    items = []
    base_url = "https://db-api-v2.akwaabasoftware.com/clients"
    url = "https://db-api-v2.akwaabasoftware.com/clients/verify-token"
    payload = json.dumps({ "token": decoded_token })

    headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}

    key = requests.request("POST", url, headers=headers, data=payload).json()
    user = requests.request("POST", url, headers=headers, data=payload).json()

    for item in key.keys():
        items.append(item)

    if "detail" in items: 
        messages.error(request, 'Invalid token') 
        return redirect("https://akwaabasoftware.com/") 

    else:
        taken = key['token']
        userId = user['user']['id']
        account_id = user['user']['accountId']
        branch_id = user['user']['branchId']
        firstname = user['user']['firstname']
        surname = user['user']['surname']
        phone = user['user']['phone']
        fullname = f'{firstname} {surname}'
        
        payload = json.dumps({})

        headers = {
        'Authorization': f'Token {taken}',
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=L7T0btpjJQY6ui0vF4Q7xZJHRVa4w4ZGwTIDnhrpxekccH2TugoVOGMmvNrc7YsI; sessionid=vtslfhyk77anv2ha7loicgehrj5rafq3'
        }


        account_url = f"{base_url}/account/{account_id}"
        pid = requests.request("GET", account_url, headers=headers, data=payload).json()['data']['id']
        account_name = requests.request("GET", account_url, headers=headers, data=payload).json()['data']['name']


        branch_url =  f"{base_url}/branch/{branch_id}"

        try:
            branch = requests.request("GET", branch_url, headers=headers, data=payload).json()['data']['name']
        except:
            branch = "Main Branch"    


        try:
            size_id = ClientSizes.objects.get(pid=pid).client_size 
            modula = MembershipSizes.objects.get(id=size_id).size
        except:
            size_id = "0"
            modula = "0-50"    


    default = Modules.objects.get(default=True).id
    database = False

    try:
        datadetail = AccountSubscription.objects.get(client_id=pid)

        for x in datadetail.modules:
            if "Database" in datadetail.modules[x]['module_name']:
                database = True
                break
            else:
                database = False

    except:
        database = False    

    modxx = Modules.objects.all() 


    return render(request, template_name, {
        'session_id':session_id,
        'account_name':account_name,
        'branch':branch,
        'default':default, 
        'modxx': modxx, 
        'database':database,
        'modula': modula,
        'pid':pid,
        'token':token,
    })



def subscriptionExtension(request, **kwargs):
    template_name = 'user/subscription-extension.html'
    session_id = request.COOKIES.get('session_id')

    token = kwargs.get('token')
    decoded_token = base64.b64decode(token).decode("utf-8")

    subscription_id = kwargs.get('id')

    subscription = AccountSubscription.objects.get(id=subscription_id)


    items = []
    base_url = "https://db-api-v2.akwaabasoftware.com/clients"
    url = "https://db-api-v2.akwaabasoftware.com/clients/verify-token"
    payload = json.dumps({ "token": decoded_token })

    headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}

    key = requests.request("POST", url, headers=headers, data=payload).json()
    user = requests.request("POST", url, headers=headers, data=payload).json()

    for item in key.keys():
        items.append(item)

    if "detail" in items: 
        messages.error(request, 'Invalid token') 
        return redirect("https://akwaabasoftware.com/") 

    else:
        taken = key['token']
        userId = user['user']['id']
        account_id = user['user']['accountId']
        branch_id = user['user']['branchId']
        firstname = user['user']['firstname']
        surname = user['user']['surname']
        phone = user['user']['phone']
        fullname = f'{firstname} {surname}'
        
        payload = json.dumps({})

        headers = {
        'Authorization': f'Token {taken}',
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=L7T0btpjJQY6ui0vF4Q7xZJHRVa4w4ZGwTIDnhrpxekccH2TugoVOGMmvNrc7YsI; sessionid=vtslfhyk77anv2ha7loicgehrj5rafq3'
        }


        account_url = f"{base_url}/account/{account_id}"
        pid = requests.request("GET", account_url, headers=headers, data=payload).json()['data']['id']
        account_name = requests.request("GET", account_url, headers=headers, data=payload).json()['data']['name']


        branch_url =  f"{base_url}/branch/{branch_id}"

        try:
            branch = requests.request("GET", branch_url, headers=headers, data=payload).json()['data']['name']
        except:
            branch = "Main Branch"    


        try:
            size_id = ClientSizes.objects.get(pid=pid).client_size 
            modula = MembershipSizes.objects.get(id=size_id).size
        except:
            size_id = "0"
            modula = "0-50"    


    default = Modules.objects.get(default=True).id
    database = False

    try:
        datadetail = AccountSubscription.objects.get(client_id=pid)

        for x in datadetail.modules:
            if "Database" in datadetail.modules[x]['module_name']:
                database = True
                break
            else:
                database = False

    except:
        database = False    


    modxx = subscription.modules 


    return render(request, template_name, {
        'session_id':session_id,
        'subscription':subscription,
        'account_name':account_name,
        'branch':branch,
        'default':default, 
        'modxx': modxx, 
        'database':database,
        'modula': modula,
        'pid':pid,
        'token':token,
    })


def subscriptionRenewal(request, **kwargs):
    template_name = 'user/subscription-renewal.html'
    session_id = request.COOKIES.get('session_id')

    token = kwargs.get('token')
    decoded_token = base64.b64decode(token).decode("utf-8")

    subscription_id = kwargs.get('id')

    subscription = AccountSubscription.objects.get(id=subscription_id)


    items = []
    base_url = "https://db-api-v2.akwaabasoftware.com/clients"
    url = "https://db-api-v2.akwaabasoftware.com/clients/verify-token"
    payload = json.dumps({ "token": decoded_token })

    headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}

    key = requests.request("POST", url, headers=headers, data=payload).json()
    user = requests.request("POST", url, headers=headers, data=payload).json()

    for item in key.keys():
        items.append(item)

    if "detail" in items: 
        messages.error(request, 'Invalid token') 
        return redirect("https://akwaabasoftware.com/") 

    else:
        taken = key['token']
        userId = user['user']['id']
        account_id = user['user']['accountId']
        branch_id = user['user']['branchId']
        firstname = user['user']['firstname']
        surname = user['user']['surname']
        phone = user['user']['phone']
        fullname = f'{firstname} {surname}'
        
        payload = json.dumps({})

        headers = {
        'Authorization': f'Token {taken}',
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=L7T0btpjJQY6ui0vF4Q7xZJHRVa4w4ZGwTIDnhrpxekccH2TugoVOGMmvNrc7YsI; sessionid=vtslfhyk77anv2ha7loicgehrj5rafq3'
        }


        account_url = f"{base_url}/account/{account_id}"
        pid = requests.request("GET", account_url, headers=headers, data=payload).json()['data']['id']
        account_name = requests.request("GET", account_url, headers=headers, data=payload).json()['data']['name']


        branch_url =  f"{base_url}/branch/{branch_id}"

        try:
            branch = requests.request("GET", branch_url, headers=headers, data=payload).json()['data']['name']
        except:
            branch = "Main Branch"    


        try:
            size_id = ClientSizes.objects.get(pid=pid).client_size 
            modula = MembershipSizes.objects.get(id=size_id).size
        except:
            size_id = "0"
            modula = "0-50"    


    default = Modules.objects.get(default=True).id
    database = False

    try:
        datadetail = AccountSubscription.objects.get(client_id=pid)

        for x in datadetail.modules:
            if "Database" in datadetail.modules[x]['module_name']:
                database = True
                break
            else:
                database = False

    except:
        database = False    

    modxx = subscription.modules   

    return render(request, template_name, {
        'session_id':session_id,
        'subscription':subscription,
        'account_name':account_name,
        'branch':branch,
        'default':default, 
        'modxx': modxx, 
        'database':database,
        'modula': modula,
        'pid':pid,
        'token':token,
    })



#  Delete fee type
def deleteSubscription(request, id, *args, **kwargs):

    token = kwargs.get('token')
    decoded_token = base64.b64decode(token).decode("utf-8")

    if request.method == "POST":
        account = AccountSubscription.objects.get(id=id)
        subscription = Subscriptions.objects.get(client_id=account.client_id) 

        subscription.delete()
        account.delete()


    messages.success(request, 'Subscription deleted successfully!')
    return HttpResponseRedirect(reverse('user:subscriptionHistory', token)) 






def cancelSubscription(request, **kwargs):

    session_id = request.COOKIES.get('session_id')
    today = timezone.now()

    module_id = kwargs.get('module_id')
    modules = [module_id]
    subscription_id = kwargs.get('subscription_id')

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


    return redirect(f"https://akwaabasoftware.com/client/")




def subscriptionHistory(request, **kwargs):
    template_name = 'user/subscription-history.html'
    session_id = request.COOKIES.get('session_id')
    today = timezone.now()

    token = kwargs.get('token')
    decoded_token = base64.b64decode(token).decode("utf-8")


    items = []
    base_url = "https://db-api-v2.akwaabasoftware.com/clients"
    url = "https://db-api-v2.akwaabasoftware.com/clients/verify-token"
    payload = json.dumps({ "token": decoded_token })

    headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}

    key = requests.request("POST", url, headers=headers, data=payload).json()
    user = requests.request("POST", url, headers=headers, data=payload).json()

    for item in key.keys():
        items.append(item)

    if "detail" in items: 
        messages.error(request, 'Invalid token') 
        return redirect("https://akwaabasoftware.com/") 

    else:
        taken = key['token']
        userId = user['user']['id']
        account_id = user['user']['accountId']
        branch_id = user['user']['branchId']
        firstname = user['user']['firstname']
        surname = user['user']['surname']
        phone = user['user']['phone']
        fullname = f'{firstname} {surname}'
        
        payload = json.dumps({})

        headers = {
        'Authorization': f'Token {taken}',
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=L7T0btpjJQY6ui0vF4Q7xZJHRVa4w4ZGwTIDnhrpxekccH2TugoVOGMmvNrc7YsI; sessionid=vtslfhyk77anv2ha7loicgehrj5rafq3'
        }

        # redirect_url = f"https://super.akwaabasoftware.com/user/subscription-history/{token}/"

        account_url = f"{base_url}/account/{account_id}"
        pid = requests.request("GET", account_url, headers=headers, data=payload).json()['data']['id']
        account_name = requests.request("GET", account_url, headers=headers, data=payload).json()['data']['name']


        branch_url =  f"{base_url}/branch/{branch_id}"

        try:
            branch = requests.request("GET", branch_url, headers=headers, data=payload).json()['data']['name']
        except:
            branch = "Main Branch"    


    try:
        usercode = AgentClients.objects.get(pid=pid).usercode
    except:
        usercode = ""

    


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


        messages.success(request, 'Modules unsubscribed successfully')
        return redirect(f"https://super.akwaabasoftware.com/user/subscription-history/{token}/")


    else:

        try:
            # subscription = AccountSubscription.objects.filter(usercode=usercode).last()
            subscription = AccountSubscriptionCopy.objects.latest('date_created')
            order_id = subscription.invoice_no
            client_id = subscription.client_id



            # confirming payment
            url = f"https://transactions.akwaabasoftware.com/transactions/{order_id}/"
            payload = {}
            headers = {}

            paid = requests.request("GET", url, headers=headers, data=payload).json()['success']
           
            

            if paid == True:

                status = AccountSubscriptionCopy.objects.get(client_id=client_id, invoice_no=order_id, usercode=usercode)

                if status.confirmed == True:
                    pass
                else:
                    status.confirmed = True
                    status.save()

                              
                
                try:
                    account = AccountSubscription.objects.get(invoice_copy=order_id)
                    account.client_id = subscription.client_id
                    account.client = subscription.client
                    account.duration=subscription.duration
                    account.membership_size=subscription.membership_size
                    account.renewing_days = subscription.renewing_days
                    account.remaining_days=subscription.remaining_days
                    account.expired_days=subscription.expired_days
                    account.subscription_fee_usd=subscription.subscription_fee_usd
                    account.subscription_fee_ghs=subscription.subscription_fee_ghs
                    account.description="Subscription"
                    account.usercode=subscription.usercode
                    account.invoice_no=subscription.invoice_no
                    account.modules=subscription.modules
                    account.expires_on=subscription.expires_on
                    account.confirmed = True
                    account.date_created = timezone.now()   
                    account.save()

                except:
                    account = AccountSubscription.objects.create(
                        client_id = subscription.client_id,
                        client = subscription.client,
                        duration=subscription.duration,
                        membership_size=subscription.membership_size,
                        renewing_days = subscription.renewing_days,
                        remaining_days=subscription.remaining_days,
                        expired_days=subscription.expired_days,
                        subscription_fee_usd=subscription.subscription_fee_usd,
                        subscription_fee_ghs=subscription.subscription_fee_ghs,
                        description="Subscription",
                        usercode=subscription.usercode,
                        invoice_no=subscription.invoice_no,
                        modules=subscription.modules,
                        expires_on=subscription.expires_on,
                        confirmed = True,
                        )
                    account.save()

                

                try:
                    subss = Subscriptions.objects.get(client_id=subscription.client_id)
                    subss.subscribed_modules = subscription.modules
                    subss.client = subscription.client
                    subss.subscription_id = subscription.invoice_no
                    subss.confirmed = True
                    subss.date_created = timezone.now()
                    subss.save()
                except:
                    subss = Subscriptions.objects.create(
                        client_id=subscription.client_id,
                        subscribed_modules = subscription.modules,
                        client = subscription.client,
                        subscription_id = subscription.invoice_no,
                        confirmed = True
                        )
                    subss.save()

                  

                


                if usercode:
                    main = Agents.objects.get(usercode=usercode).renewal_commission
                    percentage = 0.01 * float(main)

                    # The commission will be settled here
                    try:
                        agent = AgentsCommission.objects.get(usercode=usercode)
                        agent.client_name=subscription.client
                        agent.client_id=subscription.client_id
                        agent.agent_name=fullname
                        agent.usercode=usercode
                        agent.commission="Renewal Commission"
                        agent.amount = percentage * int(subscription.subscription_fee_ghs)
                        agent.save()
                    except:
                        agent = AgentsCommission.objects.create(
                        client_name=subscription.client,
                        client_id=subscription.client_id,
                        agent_name=fullname,
                        usercode=usercode,
                        commission="Renewal Commission",
                        amount = percentage * int(subscription.subscription_fee_ghs),
                        ) 

                        agent.save()  

                    try:
                        commission = TotalCommission.objects.get(usercode=usercode)
                        commission.amount += float(percentage * int(subscription.subscription_fee_ghs))
                        commission.save()
                    except:
                        commission = TotalCommission.objects.create(
                        usercode=usercode,
                        amount=float(percentage * int(subscription.subscription_fee_ghs))
                        ) 

                        commission.save() 
                else:
                    subscription.delete()         


                

            else:
                subscription.delete()
        
        except:    
            client_id = pid


        histories = AccountSubscription.objects.filter(client_id=client_id, confirmed=True)

        for x in histories:
            if today > x.expires_on:
                x.expired = True
            else:
                x.expired = False
                
            x.save()   

        return render(request, template_name, {
            'histories': histories, 
            'today': today, 
            'session_id':session_id,
            'account_name':account_name,
            'branch':branch,
            'token':token,
        }) 






def load_size(request):
    template_name = 'client/size.html'

    if request.method == 'GET': 
        client_id = request.GET.get('client_id')

        try:
            size = ClientSizes.objects.get(pid=client_id).client_size
        except:
            size = '0-50'    


        return render(request, template_name, {'size': size})




def load_modules(request):
    template_name = 'client/modules.html'

    if request.method == 'GET': 
        subscription_id = request.GET.get('subscription_id')

        subscription = AccountSubscription.objects.get(id=subscription_id)

        return render(request, template_name, {'subscription': subscription})




def load_sizes(request):
    template_name = 'client/sizes.html'
    base_url = "https://db-api-v2.akwaabasoftware.com/clients"

    session_id = request.COOKIES.get('session_id')
    details = ClientDetails.objects.get(session_id=session_id)

    client_id = details.pid
    token = details.token
    email = details.email  
    password = details.password  
    account_name = details.account_name
    branch = details.branch
    usercode = details.usercode

    if request.method == 'GET': 
        client_id = request.GET.get('client_id')
        pid = request.GET.get('pid')
        
        client_name = request.GET.get('client_name')
        size_id = request.GET.get('size_id')
        usercode = request.GET.get('usercode')
        email = request.GET.get('email')


        client_url = f'{base_url}/account?id={pid}'

        payload = json.dumps({})

        headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=i0QCkPPQCUAYcsvB4MvYAfzl4HrLL0GJ'
        }

        response = requests.request("GET", client_url, headers=headers, data=payload).json()['results'][0]

        account = response['name']

        contact = request.GET.get('contact')
        agent_name = Agents.objects.get(usercode=usercode).fullname

        size = MembershipSizes.objects.get(id=size_id)


        try:
            new_client = AgentClients.objects.get(client_id=client_id)
            new_client.client_name=client_name
            new_client.account_name=account
            new_client.pid=pid
            
            new_client.usercode=usercode
            new_client.email=email
            new_client.contact=contact
            new_client.size=size
            new_client.agent_name = agent_name
            new_client.save()
        except:
            new_client = AgentClients.objects.create(
                client_id=client_id,
                client_name=client_name,
                account_name=account,
                pid=pid,
                usercode=usercode,
                email=email,
                contact=contact,
                size=size,
                agent_name = agent_name,
            )
            new_client.save()
            
        


        try:
            client_size = ClientSizes.objects.get(client_id=client_id)
            client_size.client_name=client_name,
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





def viewProfile(request, **kwargs):

    template_name = 'user/profile.html'
    session_id = request.COOKIES.get('session_id')

    token = kwargs.get('token')
    decoded_token = base64.b64decode(token).decode("utf-8")

    items = []
    base_url = "https://db-api-v2.akwaabasoftware.com/clients"
    url = "https://db-api-v2.akwaabasoftware.com/clients/verify-token"
    payload = json.dumps({ "token": decoded_token })

    headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}

    key = requests.request("POST", url, headers=headers, data=payload).json()
    user = requests.request("POST", url, headers=headers, data=payload).json()

    for item in key.keys():
        items.append(item)

    if "detail" in items: 
        messages.error(request, 'Invalid token') 
        return redirect("https://akwaabasoftware.com/") 

    else:
        taken = key['token']
        account_id = user['user']['accountId']
        branch_id = user['user']['branchId']
        
        payload = json.dumps({})

        headers = {
        'Authorization': f'Token {taken}',
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=L7T0btpjJQY6ui0vF4Q7xZJHRVa4w4ZGwTIDnhrpxekccH2TugoVOGMmvNrc7YsI; sessionid=vtslfhyk77anv2ha7loicgehrj5rafq3'
        }


        account_url = f"{base_url}/account/{account_id}"
        pid = requests.request("GET", account_url, headers=headers, data=payload).json()['data']['id']
        account_name = requests.request("GET", account_url, headers=headers, data=payload).json()['data']['name']


        branch_url =  f"{base_url}/branch/{branch_id}"

        try:
            branch = requests.request("GET", branch_url, headers=headers, data=payload).json()['data']['name']
        except:
            branch = "Main Branch"   



    url = f"https://db-api-v2.akwaabasoftware.com/clients/account/{account_id}"
    
    headers = {
                'Authorization': f'Token {taken}',
                'Content-Type': 'application/json',
                'Cookie': 'csrftoken=4qQVgGyOrmGlgdMwQwsuRh9jmnTOyPSbjOI6Vm4VQLxX9O7gKkWr3DufNXYd7RVH; sessionid=0e2td1b1uzn4cjb5naw9bjw1hs9sjzxw'
                }

    response = requests.request("GET", url, headers=headers).json()['data']
    # print(response)

    return render(request, template_name, {'response': response, 'pid':pid,
                'branch':branch,
                'token':token,
            'account_name':account_name, 'session_id':session_id})




def logout(request):
    
    response = HttpResponse("You have been logged out.")
    response.delete_cookie('session_id')

    return redirect('https://akwaabasoftware.com')
