from django.forms import ValidationError
from rest_framework import serializers
from client.models import *
from superuser.models import *

# from jsonfield import JSONField
# import json

# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()


#     def validate_email(self, value):
#         if len(value) < 5:
#             raise ValidationError("No Jokes please")
#         return value 
    
#     def validate_password(self, value):
#         if value == "":
#             raise ValidationError("No Jokes please")
#         return value 




# class TokenSerializer(serializers.Serializer):
#     token = serializers.CharField()

#     def validate_token(self, value):
#         if value == "":
#             raise ValidationError("This field is required")
#         return value         



# class IdSerializer(serializers.Serializer):
#     client_id = serializers.CharField()

#     def validate_client_id(self, value):
#         if value == "":
#             raise ValidationError("This field is required")
#         return value 



class DatabaseSerializer(serializers.Serializer):
    client_id = serializers.CharField()

    def validate_client_id(self, value):
        if value == "Joker":
            raise ValidationError("No Jokes please")
        return value  



class OneTimeSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = OneTimeDetails
        fields = "__all__"




class SubscribedModulesSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = AccountSubscription
        fields = "__all__"




class PayOneTimeSerializer(serializers.Serializer):
    client_id = serializers.CharField()

    def validate_client_id(self, value):
        if value == "Joker":
            raise ValidationError("No Jokes please")
        return value  



class OutstandingServiceFeeSerializer(serializers.Serializer):
    client_id = serializers.CharField()
    service_fee = serializers.CharField()
    action = serializers.CharField()

    def validate_client_id(self, value):
        if value == "Joker":
            raise ValidationError("No Jokes please")
        return value  


class RegisterUsersSerializer(serializers.Serializer):
    firstname = serializers.CharField()
    surname = serializers.CharField()
    email = serializers.EmailField()
    contact = serializers.CharField()
    country = serializers.CharField()
    medium = serializers.CharField()
    image = serializers.ImageField(required=False)


    def get_validation_exclusions(self):
        exclusions = super(RegisterUsersSerializer, self).get_validation_exclusions()
        return exclusions + ['middlename']

    def validate_firstname(self, value):
        if value == "Joker":
            raise ValidationError("No Jokes please")
        return value  



class VerifyUserSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate_code(self, value):
        if value == "Joker":
            raise ValidationError("No Jokes please")
        return value  



class ResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if value == "Joker":
            raise ValidationError("No Jokes please")
        return value  



# # class HeroSerializer(serializers.ModelSerializer):
# #     description = serializers.SerializerMethodField()

# #     class Meta():
# #         model = Hero
# #         fields = '__all__'

# #     def validate_name(self, value):
# #         if value == "Joker":
# #             raise ValidationError("No Jokes please")
# #         return value   

# #     def validate(self, data):
# #         if len(data["name"]) < 5 or len(data["alias"]) < 5:
# #             raise ValidationError("Name should be more than 5")  
# #         return data     

# #     def get_description(self, data):
# #         return "This is " + data.name +"."   





# class ClientsSerializer(serializers.ModelSerializer):

#     class Meta():
#         model = ClientUser
#         fields = (
#                     "user",
#                     "client_id",
#                     "organization_name",
#                     "organization_logo",
#                     "contact_person_firstname",
#                     "contact_person_lastname",
#                     "contact_person_email",
#                     "contact_person_contact",
#                     "contact_person_photo",
#                     "membership_size",
#                     "registered_modules",
#                 )



# class ModulesSerializer(serializers.ModelSerializer):

#     class Meta():
#         model = ClientUser
#         fields = ["client_id", "registered_modules"]





# class SubscribersSerializer(serializers.ModelSerializer):




# class FeeTypeSerializer(serializers.ModelSerializer):
    
#         class Meta():
#             model = FeeType
#             fields = "__all__"


# class AssignPaymentDurationSerializer(serializers.ModelSerializer):

#     class Meta():
#         model = AssignPaymentDuration
#         fields = "__all__"


class SizesSerializer(serializers.ModelSerializer):

    class Meta():
        model = MembershipSizes
        fields = ("id", "size")


class MemberSizeSerializer(serializers.Serializer):
    client_id = serializers.CharField()
    client_name = serializers.CharField()
    size_id = serializers.CharField()
    pid = serializers.CharField()
    usercode = serializers.CharField(required=False)
    
    def get_validation_exclusions(self):
        exclusions = super(RegisterUsersSerializer, self).get_validation_exclusions()
        return exclusions + ['usercode']



class ActivationSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = ActivationFee
        fields = ("activation_fee", "duration")



class ModulesSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Modules
        fields = "__all__"



class UnitedOrganizationsSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = UnitedOrganizations
        fields = "__all__"        



class ServiceFeeSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = ServiceFee
        fields = ("client_id", "service_fee", "limit")


class MemberCodeSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = TuakaUsers
        fields = "__all__"
