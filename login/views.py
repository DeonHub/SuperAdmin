from email.message import EmailMessage
import random
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
import requests
import json
import io
import os
import environ
import base64
from django.core.mail import send_mail

from superuser.models import *
from .models import *
import datetime
from itertools import chain
# from django.conf import settings

env = environ.Env()
environ.Env.read_env()


# # Create your views here.
def login(request):

        template_name = 'login/login.html'
        today = datetime.date.today()
        base_url = "https://db-api-v2.akwaabasoftware.com/clients"
        

        if request.method == "POST":
            # role = request.POST.get('role')
            email = request.POST.get('email')
            password = request.POST.get('password')
            session_id = request.COOKIES.get('session_id')


            if email == env('EMAIL'):

                items = []
                url = base_url+"/login"
                payload = json.dumps({"phone_email": email, "password": password})
                headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}
                key = requests.request("POST", url, headers=headers, data=payload).json()
                user = requests.request("POST", url, headers=headers, data=payload).json()

                for item in key.keys():
                    items.append(item)
                if "non_field_errors" in items: 
                    response = HttpResponse("You have been logged out.") 
                    response.delete_cookie('session_id')

                    messages.error(request, 'Incorrect email or password') 
                    return HttpResponseRedirect(reverse('login:login'))   
                  
                else:
                    
                    token = key['token']
                    userId = user['user']['id']
                    account_id = user['user']['accountId']
                    branch_id = user['user']['branchId']
                    firstname = user['user']['firstname']
                    surname = user['user']['surname']
                    phone = user['user']['phone']
                    fullname = f'{firstname} {surname}'
                    
                    payload = json.dumps({})


                    headers = {
                    'Authorization': f'Token {token}',
                    'Content-Type': 'application/json',
                    'Cookie': 'csrftoken=L7T0btpjJQY6ui0vF4Q7xZJHRVa4w4ZGwTIDnhrpxekccH2TugoVOGMmvNrc7YsI; sessionid=vtslfhyk77anv2ha7loicgehrj5rafq3'
                    }

                

                    account_url = f"https://db-api-v2.akwaabasoftware.com/clients/account/{account_id}"
                    
                    pid = requests.request("GET", account_url, headers=headers, data=payload).json()['data']['id']
                    # pid = requests.request("GET", account_url, headers=headers, data=payload)
                    account_name = requests.request("GET", account_url, headers=headers, data=payload).json()['data']['name']


                    branch_url =  f"{base_url}/branch/{branch_id}"

                    try:
                        branch = requests.request("GET", branch_url, headers=headers, data=payload).json()['data']['name']
                    except:
                        branch = "Main Branch"    


                    # access_url = f"{base_url}/user-access?userId={userId}"


                    # access = requests.request("GET", access_url, headers=headers, data=payload).json()['data']
                    unlimited = False
                
                    # for x in access:
                        
                        # if x['pageId']['moduleInfo']['module'] == "Cash Manager":
                            
                        #     if x['isUnlimited']['name'] == "Unlimited":
                                
                        #         unlimited = True


                    try:
                        details = AdminDetails.objects.get(session_id=session_id)
                        details.pid=pid
                        details.account_name = account_name
                        details.branch = branch
                        details.email = email
                        details.password = make_password(password)
                        details.phone = phone
                        details.token = token
                        details.firstname=firstname
                        details.surname=surname
                        details.fullname=fullname
                        details.userId=userId
                        details.unlimited=unlimited
                        
                        details.expiry_date =  today + datetime.timedelta(days=(int(30)))
                        details.save()
                        
                    except:
                        details = AdminDetails.objects.create(
                            session_id=session_id,
                            account_name=account_name, 
                            branch=branch, 
                            pid=pid, 
                            token=token, 
                            email=email,
                            password=make_password(password), 
                            firstname=firstname, 
                            fullname=fullname,
                            surname=surname, 
                            phone=phone,
                            userId=userId,
                            unlimited=unlimited
                            )
                        details.expiry_date =  today + datetime.timedelta(days=(int(30)))
                        details.save()


                    agentx = Agents.objects.filter(pid=pid)   

                    for agent in agentx:
                        agent.token = token
                        agent.save() 
                        
                             
                    messages.success(request, 'Login Successful') 
                    return redirect('superuser:index') 
                    
            else:

                # joshuamintah@gmail.com 
                # 0558587873

                try:
                    agent = Agents.objects.get(email=email)

                    password_matches = check_password(password, agent.password)

                    if password_matches:
                        

                        if agent.account == "unlimited":
                            

                            items = []
                            url = base_url+"/login"
                            payload = json.dumps({"phone_email": env('EMAIL'), "password": env('PASSWORD')})
                            headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}
                            key = requests.request("POST", url, headers=headers, data=payload).json()
                            user = requests.request("POST", url, headers=headers, data=payload).json()

                            for item in key.keys():
                                items.append(item)
                            if "non_field_errors" in items: 
                                response = HttpResponse("You have been logged out.") 
                                response.delete_cookie('session_id')

                                messages.error(request, 'Incorrect email or password') 
                                return HttpResponseRedirect(reverse('login:login'))   
                            
                            else:
                                
                                token = key['token']
                                userId = user['user']['id']
                                account_id = user['user']['accountId']
                                branch_id = user['user']['branchId']
                                # firstname = user['user']['firstname']
                                # surname = user['user']['surname']
                                # phone = user['user']['phone']
                                # fullname = f'{firstname} {surname}'
                                
                                payload = json.dumps({})


                                headers = {
                                'Authorization': f'Token {token}',
                                'Content-Type': 'application/json',
                                'Cookie': 'csrftoken=L7T0btpjJQY6ui0vF4Q7xZJHRVa4w4ZGwTIDnhrpxekccH2TugoVOGMmvNrc7YsI; sessionid=vtslfhyk77anv2ha7loicgehrj5rafq3'
                                }

                            

                                account_url = f"https://db-api-v2.akwaabasoftware.com/clients/account/{account_id}"
                                
                                pid = requests.request("GET", account_url, headers=headers, data=payload).json()['data']['id']
                                # pid = requests.request("GET", account_url, headers=headers, data=payload)
                                account_name = requests.request("GET", account_url, headers=headers, data=payload).json()['data']['name']


                                branch_url =  f"{base_url}/branch/{branch_id}"

                                try:
                                    branch = requests.request("GET", branch_url, headers=headers, data=payload).json()['data']['name']
                                except:
                                    branch = "Main Branch"    


                                # access_url = f"{base_url}/user-access?userId={userId}"


                                # access = requests.request("GET", access_url, headers=headers, data=payload).json()['data']
                                unlimited = False
                            
                                try:
                                    details = AdminDetails.objects.get(session_id=session_id)
                                    details.pid=pid
                                    details.account_name = agent.account_name
                                    details.branch = branch
                                    details.email = agent.email
                                    details.password = agent.password
                                    details.phone = agent.contact
                                    details.token = token
                                    details.firstname=agent.firstname
                                    details.surname=agent.surname
                                    details.fullname=agent.fullname
                                    details.userId=userId
                                    details.unlimited=unlimited
                                    
                                    details.expiry_date =  today + datetime.timedelta(days=(int(30)))
                                    details.save()
                                    
                                except:
                                    details = AdminDetails.objects.create(
                                        session_id=session_id,
                                        account_name=agent.account_name, 
                                        branch=agent.branch, 
                                        pid=pid, 
                                        token=token, 
                                        email=agent.email,
                                        password=agent.password, 
                                        firstname=agent.firstname, 
                                        fullname=agent.fullname,
                                        surname=agent.surname, 
                                        phone=agent.contact,
                                        userId=userId,
                                        unlimited=unlimited
                                        )
                                    details.expiry_date =  today + datetime.timedelta(days=(int(30)))
                                    details.save()


                            messages.success(request, 'Login Successful') 
                            return redirect('superuser:index')         

                        else:

                            try:
                                details = ClientDetails.objects.get(session_id=session_id)
                                details.pid = agent.pid
                                details.account_name = agent.account_name
                                details.branch = agent.branch
                                details.email = agent.email
                                details.password = make_password(agent.password)
                                details.phone = agent.contact
                                details.token = agent.token
                                details.firstname=agent.firstname
                                details.surname=agent.surname
                                details.fullname = f'{agent.firstname} {agent.surname}'
                                details.usercode=agent.usercode
                                details.unlimited = False
                                
                                details.expiry_date =  today + datetime.timedelta(days=(int(30)))
                                details.save()
                                
                            except:
                                details = ClientDetails.objects.create(
                                    session_id=session_id,
                                    account_name=agent.account_name, 
                                    branch=agent.branch, 
                                    pid=agent.pid, 
                                    token=agent.token, 
                                    email=agent.email,
                                    password=make_password(agent.password), 
                                    firstname=agent.firstname, 
                                    fullname=agent.fullname,
                                    surname=agent.surname, 
                                    phone=agent.contact,
                                    usercode=agent.usercode,
                                    )
                                details.expiry_date =  today + datetime.timedelta(days=(int(30)))
                                details.save()


                            messages.success(request, 'Login Successful') 
                            return redirect('client:index')  


                    else:
                        messages.error(request, 'Incorrect email or password. Please contact admin') 
                        return HttpResponseRedirect(reverse('login:login'))  


                except:
                    messages.error(request, 'Invalid login credentials. Please contact admin') 
                    return HttpResponseRedirect(reverse('login:login'))             


        else:               
            return render(request,  template_name)
     


def verifyEmail(request):
    template_name = 'login/verify-email.html'

    if request.method == "POST":
        # role = request.POST.get('role')
        email = request.POST.get('email') 

        try:
            emailx = Agents.objects.get(email=email)

            code = random.randint(100000, 999999)
            

            subject = 'EMAIL VERIFICATION CODE'
            message = f"Your verification code is {code}."

            from_email = settings.EMAIL_HOST_USER
            recipient_list = [f'{email}']


            verifix = Verifications.objects.create(firstname=f"User{code}", contact="1234567890", email=email, code=code)
            verifix.save()

            send_mail(subject, message, from_email, recipient_list)



            messages.success(request, 'Verification code sent successfully.') 
            return redirect('login:verifyCode') 

        except:
            messages.error(request, 'Invalid user email. Please contact admin.') 
            return redirect('login:verifyEmail')  
    
        
    return render(request, template_name, {})
        


def verifyCode(request):
    template_name = 'login/verify-code.html'

    if request.method == "POST":
        code = request.POST.get('code') 

        try:
            verification = Verifications.objects.get(code=code)

            code = base64.b64encode(code.encode("utf-8")).decode("utf-8")

            messages.success(request, 'Verification successful. Enter password to proceed.') 
            return redirect('login:changePassword', code) 

        except:
            messages.error(request, 'Incorrect code. Please check your email for correct code.') 
            return redirect('login:verifyCode')  
    
    return render(request, template_name, {})
        


def changePassword(request, **kwargs):
    template_name = 'login/change-password.html'
    codex = kwargs.get('code')

    # Decode the encoded string
    code = base64.b64decode(codex).decode("utf-8")


    if request.method == "POST":
        password = request.POST.get('password')

        try:
            verifix = Verifications.objects.get(code=code)
            email = verifix.email

            agent = Agents.objects.get(email=email)
            agent.password = make_password(password)
            agent.save()

            verifix.delete()

            messages.success(request, 'Password changed successfully. Login to continue') 
            return redirect('login:login') 
        
        except:
            messages.error(request, 'Password mismatch') 
            return redirect('login:changePassword', codex)     
    
    return render(request, template_name, {})