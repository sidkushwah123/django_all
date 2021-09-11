from rest_framework import serializers
from admin_manage_products.models import AwProductPrice,AwProducts,AwProductImage
from orders.models import AwAddToCard
from django.contrib.auth.models import User
from rest_framework import  exceptions
from django.shortcuts import get_object_or_404
from .models import AwWishList



class MywishlistapiViewserializer(serializers.ModelSerializer):
    
    class Meta:
        model =  AwWishList
        fields = "__all__"
        depth = 2


