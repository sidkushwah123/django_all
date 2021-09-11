from rest_framework import serializers
from rest_framework import  exceptions
from django.shortcuts import get_object_or_404
from .models import AwAddressBook
from admin_manage_country.models import AwCountryUser



class AddressBookListapiserializer(serializers.ModelSerializer):
   

    class Meta:
        model = AwAddressBook
        fields = "__all__"
        depth = 2
    
    


