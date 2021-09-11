
from rest_framework import serializers
from admin_manage_products.models import AwProductPrice,AwProducts,AwProductImage
from orders.models import AwAddToCard
from django.contrib.auth.models import User
from rest_framework import  exceptions
from django.shortcuts import get_object_or_404


class ProductPriceSeriSerializer(serializers.ModelSerializer):
    class Meta:
        model =  AwProductPrice
        fields = ('id', 'Product','Vintage_Year','Bottle', 'Retail_Cost','Retail_Stock', 'Descount_Cost' ,'Duty','GST','Bond_Cost','Bond_Stock','Bond_Descount_Cost','Other_info','Created_by','Created_date','Updated_by','Updated_date')



class ProductImageSerializer(serializers.HyperlinkedModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(queryset=AwProducts.objects.all(), source='AwAddToCard.Product.id')

    class Meta:
        model = AwProductImage
        fields = ('id', 'Image_Type', 'Image', 'Product','parent_id')

    def create(self, validated_data):
        subject = AwProductImage.objects.create(Product=validated_data['AwAddToCard']['Product']['id'], Image_Type=validated_data['Type'])
        return child


class AwAddToCardSerializer(serializers.ModelSerializer):

   
    AwProductImage_Product = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model =  AwAddToCard
        fields = ('id','User','Cookies_id','Order_Type','Product_Cellar','Product_Delivered','Event_Ticket','Year','Type','Old_Cost','Case_Formate','Quentity','Date','AwProductImage_Product')
        


class Getidvalidation(serializers.Serializer):
    user_ins = serializers.CharField(style={"inpupt_type": "text"}, write_only=True,required=False,allow_blank=True)
   
    def validate(self, data):
        
        user_id = data.get("user_ins","")
        
        User_id_data = None
        if user_id :
            if User.objects.filter(id=user_id).exists():
                User_id_data = get_object_or_404(User,id=user_id)
                # User_id_data = User.objects.get(id=user_id)
            else:
                mes = "id is incorrect "
                raise exceptions.ValidationError(mes)
        else:
            User_id_data = ""
        return User_id_data


class userserializer(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = "__all__"

class MyCardapiViewserializer(serializers.ModelSerializer):

    class Meta:
        model =  AwAddToCard
        fields = ('id','User','Cookies_id','Order_Type','Product_Cellar','Product_Delivered','Event_Ticket','Year','Type','Old_Cost','Case_Formate','Quentity','Date' )
        depth = 2

class Getcheakvalidation(serializers.Serializer):
    product_id = serializers.CharField(style={"inpupt_type": "text"}, write_only=True,required=True,allow_blank=False)
    Year = serializers.CharField(style={"inpupt_type": "text"}, write_only=True,required=True,allow_blank=False)
    Type = serializers.CharField(style={"inpupt_type": "text"}, write_only=True,required=True,allow_blank=False)
    Case_Formate_id = serializers.CharField(style={"inpupt_type": "text"}, write_only=True,required=True,allow_blank=False)
    Quentity_set = serializers.CharField(style={"inpupt_type": "text"}, write_only=True,required=True,allow_blank=False)
    order_type = serializers.CharField(style={"inpupt_type": "text"}, write_only=True,required=True,allow_blank=False)


   