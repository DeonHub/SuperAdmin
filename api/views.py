from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from .serializers import *
# from .models import Token
from rest_framework.views import APIView
from superuser.models import *
from client.models import *
from login.models import *
import datetime
import requests
import json
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
import secrets
import random
import string
from .models import *

import environ


env = environ.Env()
environ.Env.read_env()

# Create your views here.

fee_url = "https://cash.akwaabasoftware.com/api"
# fee_url = "http://127.0.0.1:8000/api"


def random_char(y):
    return ''.join(random.choice(string.ascii_uppercase) for x in range(y))



class GetSizes(APIView):
    
    def get(self, request):
        subscribers = MembershipSizes.objects.all()
        all_type = SizesSerializer(subscribers, many=True)
        data = {
            "count":len( MembershipSizes.objects.all()),
            "data":all_type.data
        }
        return Response(data)



class AddMembershipSize(APIView):

    def post(self, request, *args):

        today = datetime.date.today()

        members = MemberSizeSerializer(data=request.data)

        if members.is_valid():
            client_id = members.data['client_id']
            client_name = members.data['client_name']
            size_id = members.data['size_id']
            pid = members.data['pid']
            usercode = members.data['usercode']

            size = MembershipSizes.objects.get(id=size_id)


            if usercode != "None":

                agent_name = Agents.objects.get(usercode=usercode).fullname
                # account_name = Agents.objects.get(usercode=usercode).account_name
                

                hash_url = "https://db-api-v2.akwaabasoftware.com/clients/hash-hash"

                payload = json.dumps({ "accountId": pid })
                headers = {
                'Content-Type': 'application/json',
                'Cookie': 'csrftoken=B8Cuhwl9fJdxIZnuRLRAhX32YhYTHPpn; sessionid=lpsj10ap33zyaog6fmatps53d99l1c08'
                }

                token = requests.request("POST", hash_url, headers=headers, data=payload).json()['token']

                
                base_url = "https://db-api-v2.akwaabasoftware.com/clients"

                
                url = f"{base_url}/account/{pid}"

                payload = json.dumps({})


                headers = {
                'Authorization': f'Token {token}',
                'Content-Type': 'application/json',
                'Cookie': 'csrftoken=Hf5Wd7yKmiDjeyREEwvlbZUZzfYR1vzVYaUpdIO01NjhxGBEM19MJTn2ioMrJbBI; sessionid=ca7rumjb8xhn9md452xwgsv7zwgvjzq2'
                }


                response = requests.request("GET", url, headers=headers, data=payload).json()['data']
                account_name = response['name']
                email = response['applicantEmail']
                contact = response['applicantPhone']
                gender = response['applicantGender']


                try:
                    new_client = AgentClients.objects.get(client_id=client_id)
                    new_client.client_name=client_name
                    new_client.account_name=account_name
                    new_client.pid=pid
                    new_client.gender=gender
                    new_client.email=email
                    new_client.contact=contact
                    
                    new_client.usercode=usercode
                    new_client.size=size.size
                    new_client.agent_name = agent_name
                    new_client.save()
                except:
                    new_client = AgentClients.objects.create(
                        client_id=client_id,
                        client_name=client_name,
                        account_name=account_name,
                        gender=gender,
                        email=email,
                        contact=contact,
                        pid=pid,
                        usercode=usercode,
                        size=size.size,
                        agent_name = agent_name,
                    )
                    new_client.save()

            else:
                pass        

            
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


            data = {
                    "success": True,
                    "status":"Saved successfully"
                    }
            
                    
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(members.errors, status=status.HTTP_400_BAD_REQUEST)  





class GetSize(APIView):
    
    def get(self, request, **kwargs):

        client_id = kwargs.get('client_id')

        size_id = MembershipSizes.objects.get(id = ClientSizes.objects.get(pid=client_id).client_size.id)

        data = {
            "success": True,
            "size_id": size_id.id
         }
        return Response(data)



class GetLimit(APIView):
    
    def get(self, request, **kwargs):

        client_id = kwargs.get('client_id')

        size_id = MembershipSizes.objects.get(id=ClientSizes.objects.get(pid=client_id).client_size.id)

        data = {
            "client_id": client_id,
            "limit": int(size_id.size.split("-")[1])
         }
        
        return Response(data)



class GetActivation(APIView):
    
    def get(self, request, *args, **kwargs):

        membership_size = kwargs.get('membership_size')
        membership_size=int(membership_size)        

        try:
            subscribers = ActivationFee.objects.get(membership_size=membership_size)
            all_type = ActivationSerializer(subscribers)

            data = {
                "success": True,
                "activation_fee":subscribers.activation_fee,
                "duration":subscribers.duration
                }

            return Response(data)

        except:
            info = [x.activation_fee for x in ActivationFee.objects.all()]
            least = min(info)
            dur = ActivationFee.objects.filter(activation_fee=least).first()
            duration = dur.duration

            data = {
                "success": True,
                "activation_fee": least,
                "duration": duration
                }

            return Response(data)



class GetModules(APIView):
    
    def get(self, request):
        subscribers = Modules.objects.all()
        all_type = ModulesSerializer(subscribers, many=True)
        data = {
            "count":len(Modules.objects.all()),
            "data":all_type.data
        }
        return Response(data)




class GetDatabaseDetails(APIView):
    
    def get(self, request, **kwargs):
        client_id = kwargs.get('client_id')
        today = datetime.date.today()
        now = datetime.datetime.now()

        try:
            subscribers = DatabaseDetails.objects.get(client_id=client_id)
            all_type = DatabaseSerializer(subscribers)

            if today < subscribers.expires_on:

                data = {
                        "success": True,
                        "status":"Active"
                        }
                
                return Response(data)

            else:
                data = {
                        "success": False,
                        "status":"Expired"
                        }
                    
                return Response(data)
        except:
            data = {
                "success": False,
                "status":"Does not exist"
                }
                
            return Response(data)





class ClientActivation(APIView):
    
    def get(self, request, **kwargs):

        client_id = kwargs.get('client_id')

        try:
            subscribers = OneTimeDetails.objects.get(client_id=client_id)
            all_type = OneTimeSerializer(subscribers)

            data = {
                "success": True,
                "status":"Paid"
                }
                
            return Response(data)
        except:
            data = {
                "success": False,
                "data":"Unpaid"
                }
                
            return Response(data)






class GetSubscribedModules(APIView):
    
    def get(self, request, **kwargs):

        client_id = kwargs.get('client_id')

        try:
            try:
                subscribers = AccountSubscription.objects.get(client_id=client_id)
            except:
                subscribers = AccountSubscription.objects.filter(client_id=client_id).last()

            all_type = SubscribedModulesSerializer(subscribers)

            data = {
                "success":True,
                "data":all_type.data
            }

            return Response(data)

        except:
            data = {
                "success": False,
                "data":[]
                }
                
            return Response(data)




class PayOneTime(APIView):


    def get(self, request, **kwargs):
        today = datetime.date.today()
    
        client_id = kwargs.get('client_id')
        
        expires_on =  today + datetime.timedelta(days=(int(100)))

        try:
            subscribers = OneTimeDetails.objects.get(client_id=client_id, paid=True)
        except:
            subscribers = OneTimeDetails.objects.create(client_id=client_id, paid=True, expires_on=expires_on)
            subscribers.save()

        data = {
                "success": True,
                "status":"Paid Successfully"
                }
                
        return Response(data, status=status.HTTP_200_OK)





class GetModule(APIView):
    
    def get(self, request, **kwargs):
        module_id = kwargs.get('module_id')

        mode = Modules.objects.get(id=module_id)

        all_type = ModulesSerializer(mode)

        data = {
            "data":all_type.data
            }
        return Response(data)






class GetClientEmailDetails(APIView):

    def get(self, request, **kwargs):
        
        client_id = kwargs.get('client_id')

        details = EmailDetails.objects.get(client_id=client_id)
        email = details.email
        password = details.password
        
        # heroes = PaymentHistorySerializer(all_payments, many=True)

        user_history = {
            "success": True,
            "email": email,
            "password": password
        }
        
        return Response(user_history)



class GetClientPaymentDetails(APIView):
    
    def get(self, request, **kwargs):
        
        client_id = kwargs.get('client_id')

        try:
            details = PaymentDetails.objects.get(client_id=client_id)
            merchant_account_number = details.merchant_account_number
            success = True
            
        except:
            success = False
            merchant_account_number = None


        user_history = {
            "success": success,
            "merchant_account_number": merchant_account_number
        }
        
        return Response(user_history)






class GetServiceFee(APIView):

    def get(self, request, **kwargs):
        client_id = kwargs.get('client_id')

        try:
            details = ServiceFee.objects.get(client_id=client_id)
            all_type = ServiceFeeSerializer(details)


            data = {
                "client_id":details.client_id,
                "service_fee":details.service_fee,
                "limit":details.limit,
                "outstanding_fee":details.outstanding_fee,
                }

            return Response(data, status=status.HTTP_200_OK)

        except:

            data = {
                "client_id": client_id,
                "service_fee":0,
                "limit":0,
                "outstanding_fee":0,
                }

            return Response(data, status=status.HTTP_200_OK)   



class OutstandingServiceFee(APIView):


    def post(self, request, *args):

        today = datetime.date.today()
        year = datetime.datetime.now().year
        year = str(year) + "0000"

        members = OutstandingServiceFeeSerializer(data=request.data)

        if members.is_valid():
            client_id = members.data['client_id']
            service_fee = members.data['service_fee']
            action = members.data['action']


            if action == "increase":

                try:
                    service = ServiceFee.objects.get(client_id=client_id)
                    service.outstanding_fee += float(service_fee)
                    service.save()
                except:
                    service = ServiceFee.objects.create(client_id=client_id, outstanding_fee=service_fee)
                    service.save()

                data = {
                        "success": True,
                        "status":"Updated Successfully"
                        }
                        
                return Response(data, status=status.HTTP_200_OK)

            elif action == "decrease":
                try:
                    service = ServiceFee.objects.get(client_id=client_id)
                    service.outstanding_fee = 0.00
                    service.save()
                except:
                    service = ServiceFee.objects.create(client_id=client_id, outstanding_fee=0.00)
                    service.save()

                data = {
                        "success": True,
                        "status":"Paid Successfully"
                        }
                        
                return Response(data, status=status.HTTP_200_OK)
                
            else:

                data = {
                        "success": False,
                        "status":"Invalid action"
                        }
                        
                return Response(data, status=status.HTTP_400_BAD_REQUEST)  

        else:
            return Response(members.errors, status=status.HTTP_400_BAD_REQUEST)  






class RegisterUser(APIView):

    # parser_classes = [MultiPartParser]

    def post(self, request, *args):

        today = datetime.date.today()
        year = datetime.datetime.now().year
        year = str(year) + "0000"

        members = RegisterUsersSerializer(data=request.data)

        if members.is_valid():
            firstname = members.data['firstname']
            surname = members.data['surname']
            email = members.data['email']
            contact = members.data['contact']
            country = members.data['country']
            medium = members.data['medium']

            try:
                image = members.data['image']
            except:
                image = None


            try:
                user = TuakaUsers.objects.get(email=email)

                data = {
                    "success": False,
                    "status":"User exists"
                    }

                return Response(data, status=status.HTTP_400_BAD_REQUEST)     

            except:

                user = TuakaUsers.objects.create(firstname=firstname, surname=surname, email=email, contact=contact, country=country, image=image)
                user.save()

                code = random.randint(100000, 999999)

                verifications = Verifications.objects.create(firstname=firstname, email=email, contact=contact, code=code)
                verifications.save()


                if medium == "email":

                    # Send email
                    subject = f'ACCOUNT VERIFICATION CODE'
                    body = f"""
                                Hello {firstname}, 

                                Your Verification Code is {code}.
                                Enter this code to verify your account.
                                This code will expire after 5 days.
                                Thank you.
                            """
                    senders_mail = settings.EMAIL_HOST_USER
                    to_address = [f'{email}']



                    email = EmailMessage(subject, body, senders_mail, to_address)

                    try:
                        email.send()
                        # pass
                    except: 
                        print("Server error")
                        pass


                else:

                    private_key = env('PRIVATE_KEY')
                    public_key = env('PUBLIC_KEY')

                    if contact.startswith('0'):
                        contact = f'233{int(contact)}'


                    body = f"Your verification code is {code}."
 
                    url = f"https://api.msmpusher.net/v1/send?privatekey={private_key}&publickey={public_key}&sender=UNAGH&numbers={contact}&message={body}"

                    payload = {}
                    headers = {}

                    try:
                        response = requests.request("GET", url, headers=headers, data=payload).json()
                    except:
                        pass    



                data = {
                        "success": True,
                        "status":"Verification code sent successfully!"
                    }
                        
                return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(members.errors, status=status.HTTP_400_BAD_REQUEST)  




class VerifyUser(APIView):

    def post(self, request, *args):
    
        year = datetime.datetime.now().year
        year = str(year) + "0000"

        members = VerifyUserSerializer(data=request.data)

        if members.is_valid():
            code = members.data['code']
 
            try:
                verifications = Verifications.objects.get(code=code)
                email = verifications.email
                firstname = verifications.firstname
                contact = verifications.contact


                user = TuakaUsers.objects.get(email=email)
                user.verified = True

 
                codex = random.randint(10000, 99999)
                chars = random_char(3)
                usercode = f'{chars}{codex}'

                try:
                    existing_code = TuakaUsers.objects.get(usercode=usercode).usercode

                    while True:
                        if usercode == existing_code:
                            codex = random.randint(10000, 99999)
                            chars = random_char(3)

                            usercode = f'{chars}{codex}'
                        else:
                            break    

                except:
                    pass


                user.usercode = usercode
                user.save()

 
                # Send email
                subject = f'ACCOUNT ACCESS CODE'
                body = f"""
                            Hello {firstname}, 

                            You have successfully created your UN Membership Fees Payment account. 
                            Your access code is {usercode}
                        """

                senders_mail = settings.EMAIL_HOST_USER
                to_address = [f'{email}']


                email = EmailMessage(subject, body, senders_mail, to_address)

                try:
                    email.send()
                except: 
                    print("Server error")
                    pass


                verifications.delete()
                verifications.save()






                data = {
                        "success": True,
                        "status":"User verified successfully!"
                        }
                        
                return Response(data, status=status.HTTP_200_OK)



            except:

                data = {
                    "success": False,
                    "status":"Invalid code"
                    }

                return Response(data, status=status.HTTP_400_BAD_REQUEST)  

        else:
            return Response(members.errors, status=status.HTTP_400_BAD_REQUEST)  





class ValidateCode(APIView):
    
    def get(self, request, **kwargs):
        
        usercode = kwargs.get('usercode')

        try:
            code = TuakaUsers.objects.get(usercode=usercode)
            print(code)
            
            user_history = {
                "success": "True",
            }
            
            return Response(user_history, status=status.HTTP_200_OK)
   
        except:
            error = {
                "success": "False",
                }

            return Response(error, status=status.HTTP_400_BAD_REQUEST)  




class ResetCode(APIView):

    def post(self, request, *args):

        year = datetime.datetime.now().year
        year = str(year) + "0000"

        members = ResetCodeSerializer(data=request.data)

        if members.is_valid():
            email = members.data['email']
            
 
            try:

                user = TuakaUsers.objects.get(email=email)
                email = user.email
                firstname = user.firstname
                codx = user.usercode


                codex = random.randint(10000, 99999)
                chars = random_char(3)
                usercode = f'{chars}{codex}'

                try:
                    existing_code = TuakaUsers.objects.get(usercode=usercode).usercode

                    while True:
                        if usercode == existing_code:
                            codex = random.randint(10000, 99999)
                            chars = random_char(3)

                            usercode = f'{chars}{codex}'
                        else:
                            break    

                except:
                    pass


                user.usercode = usercode
                user.save()

 
                # Send email
                subject = f'RESET ACCESS CODE'
                body = f"""
                            Hello {firstname}, 
                            Your new access code is {usercode}.
                            Use this code to login to your account.
                            Thank you.
                        """

                senders_mail = settings.EMAIL_HOST_USER
                to_address = [f'{email}']


                email = EmailMessage(subject, body, senders_mail, to_address)

                try:
                    email.send()
                except: 
                    print("Server error")
                    pass



                try:
                    member_url = f"{fee_url}/member-details/{codx}/"
                    
                    headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}

                    member = requests.request("GET", member_url, headers=headers).json()['data']


                    member_id = member['member_id']

                    
                    update_url = f"{fee_url}/update-usercode/"
                    headers = {
                    'Content-Type': 'application/json',
                    'Cookie': 'csrftoken=ugVDmJWTsUSPEymPZ7fLtVC0Q8j6IeLG8TgyrkTe6IbLRbsFYEB89jLoB99sCzAZ; sessionid=vjnl5bhycfm5e1z1lb46jh06ec3nzunq'
                    }

                    payload = json.dumps({
                        "member_id": member_id,
                        "usercode": usercode
                    })

                    done = requests.request("POST", update_url, headers=headers, data=payload).json()['success']

                except:
                    member_id = ""  


                data = {
                        "success": True,
                        "member_id": member_id,
                        "usercode": usercode,
                        "status":"Access Code reset successfully!"
                        }
                        
                return Response(data, status=status.HTTP_200_OK)



            except:

                data = {
                    "success": False,
                    "status":"Invalid email"
                    }

                return Response(data, status=status.HTTP_400_BAD_REQUEST)  

        else:
            return Response(members.errors, status=status.HTTP_400_BAD_REQUEST)  




class GetMemberDetails(APIView):
    

    def get(self, request, **kwargs):
            
        usercode = kwargs.get('usercode')

        try:
            user = TuakaUsers.objects.get(usercode=usercode)

            heroes = MemberCodeSerializer(user)

            user_history = {
                "success": True,
                "data": heroes.data
            }
            
            return Response(user_history)

        except:
            error = {
                "success": False,
                "data": []
                }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)  




class GetUnitedOrganizations(APIView):
    
    def get(self, request):
        subscribers = UnitedOrganizations.objects.all()
        all_type = UnitedOrganizationsSerializer(subscribers, many=True)
        data = {
            "count":len(UnitedOrganizations.objects.all()),
            "data":all_type.data
        }
        return Response(data)







class GetApp(APIView):
    
    def get(self, request, *args, **kwargs):

        today = datetime.date.today()

        token = kwargs.get('token')

        redirect_url = "https://play.google.com/store/apps/details?id=com.akwaaba.app.akwaaba"

        return redirect(redirect_url) 




class ClientSubscription(APIView):
    

    def get(self, request, *args, **kwargs):

        today = datetime.date.today()

        token = kwargs.get('token')

        items = []
        base_url = "https://db-api-v2.akwaabasoftware.com/clients"
        url = base_url+"/verify-token"
        payload = json.dumps({ "token": token })

        headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}

        key = requests.request("POST", url, headers=headers, data=payload).json()
        user = requests.request("POST", url, headers=headers, data=payload).json()

        for item in key.keys():
            items.append(item)

        if "detail" in items: 
            messages.error(request, 'Invalid token') 
            redirect_url = "https://super.akwaabasoftware.com/"

        else:
            token = key['token']
            account_id = user['user']['accountId']
            
            branch_id = user['user']['branchId']
            email = user['user']['email']
            
            payload = json.dumps({})

            headers = {
            'Authorization': f'Token {token}',
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
                details = ClientDetails.objects.get( pid=pid )
                details.account_name = account_name
                details.branch = branch
                details.token = token
                details.save()

            except:      
                details = ClientDetails.objects.create( account_name=account_name, branch=branch, pid=pid, token=token)
                details.save()
            

            try:
                dasho = Dasho.objects.get(pid=pid)
                dasho.redirected = True
                dasho.save()
            except:
                dasho = Dasho.objects.create(pid=pid, redirected=True)
                dasho.save()


            try:
                datadetail = DatabaseDetails.objects.get(client_id=pid)

                if datadetail.subscribed == True:
                    if today <= datadetail.expires_on:
                        database = True
                    else:
                        database = False    
                else:
                    database = False    
            except:
                database = False  
            

            if database == True:
                redirect_url = f"https://super.akwaabasoftware.com/client/account-subscription/{pid}/"
            else:
                redirect_url = f"https://super.akwaabasoftware.com/client/database-subscription/{pid}/"
                   

        return redirect(redirect_url) 

