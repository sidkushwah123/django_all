from django.shortcuts import render,get_object_or_404
from django.template.defaulttags import register
from admin_manage_products.models import AwProducts
from .models import AwWishList
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from orders.models import AwProductPrice
from django.contrib.auth.models import User

#api 
from .serializer import MywishlistapiViewserializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import  exceptions

# Create your views here.





@method_decorator(login_required , name="dispatch")
class WishListVidw(generic.ListView):  
    model = AwWishList
    template_name = "web/user/page/wishlist/wish_list.html"
    queryset = None
    paginate_by = 10

    def get_queryset(self, **kwargs):
        get_order_items = ""
        if AwWishList.objects.filter(user_info=self.request.user).exists():
            get_order_items = AwWishList.objects.filter(user_info=self.request.user)
        return get_order_items

    def get_context_data(self, *args, **kwargs):
        context = super(WishListVidw, self).get_context_data(*args, **kwargs)
        context['Page_title'] = "Wish List"
        return context

class WishListVidwapi(APIView):

    def post(self,request):
        user = request.data['User_id']
        message = None
        data = None

        if user == "":
            message = "id is incorrect "

        else:

            if User.objects.filter(id=user).exists():
                User_id_data = get_object_or_404(User,id=user)

                if AwWishList.objects.filter(user_info=User_id_data).exists():
                    get_order_items = AwWishList.objects.filter(user_info=User_id_data)

                    get_data = MywishlistapiViewserializer(get_order_items, many=True)
                    data = get_data.data
                    message = str(len(get_order_items)) + " Item In card"
                else:

                    message = "no item in wishlist"
                    
            else:
                message = "id is incorrect "
            
        return Response({ "message": message,"data":data})



def add_product_in_wishlist(request,product_id,vintage_year):
    status = "0"
    if AwProducts.objects.filter(id=product_id).exists():
        product_ins = get_object_or_404(AwProducts,id=product_id)
        user = request.user
        year = vintage_year
        if AwProductPrice.objects.filter(Product=product_ins).filter(Vintage_Year__Vintages_Year=year).exists():
            vinrage_year_ins = AwProductPrice.objects.filter(Product=product_ins).filter(Vintage_Year__Vintages_Year=year).first()
            if AwWishList.objects.filter(user_info=user).filter(Product=product_ins).filter(Case_Formate=vinrage_year_ins).exists():
                AwWishList.objects.filter(user_info=user).filter(Product=product_ins).filter(
                    Case_Formate=vinrage_year_ins).delete()
                status = "0"
                message = "Product is removed from your wishlist."
            else:
                add_data = AwWishList(user_info=user, Product=product_ins, Case_Formate=vinrage_year_ins)
                add_data.save()
                status = "1"
                message = "Product add in your wishlist successfully."
        else:
            message = "vintage_id is in icorrected."
    else:
        message = "product_id is incorrect."
    return JsonResponse({"status": status, "message": message})


class add_product_in_wishlist_api(APIView):
    
    def post(self,request):

        user = request.data['User_id']
        product_id = request.data['Product_id']
        vintage_year = request.data['vintage_year']
        message = None
        status = "0"
        serializer = MywishlistapiViewserializer(data=request.data)
        data_response = {}
        if serializer.is_valid():
            if user == "":
                message = "id is incorrect "
            else:
                if User.objects.filter(id=user).exists():
                    User_id_data = get_object_or_404(User,id=user)
                    if product_id == "":
                        message = "product id is inccorect"
                    else:
                        if AwProducts.objects.filter(id=product_id).exists():
                            product_ins = get_object_or_404(AwProducts,id=product_id)
                            user = User_id_data
                            year = vintage_year
                            if AwProductPrice.objects.filter(Product=product_ins).filter(Vintage_Year__Vintages_Year=year).exists():
                                vinrage_year_ins = AwProductPrice.objects.filter(Product=product_ins).filter(Vintage_Year__Vintages_Year=year).first()
                                if AwWishList.objects.filter(user_info=user).filter(Product=product_ins).filter(Case_Formate=vinrage_year_ins).exists():
                                    AwWishList.objects.filter(user_info=user).filter(Product=product_ins).filter(Case_Formate=vinrage_year_ins).delete()
                                    status = "0"
                                    message = "Product is removed from your wishlist."
                                else:
                                    add_data = AwWishList(user_info=user, Product=product_ins, Case_Formate=vinrage_year_ins)
                                    add_data.save()
                                    status = "1"
                                    message = "Product add in your wishlist successfully."
                            else:
                                message = "vintage_id is in icorrected."
                        else:
                            message = "product id is inccorect"                  
                else:
                    message = "id is incorrect "  
        else:
            data_response = serializer.errors 
        return Response({"status":status,"message": message})
       




@register.filter(name='check_in_wish_list')
def check_in_wish_list(user_ins,product_ins):
    message = ""
    if AwWishList.objects.filter(user_info=user_ins).filter(Product=product_ins).exists():
        message = "whistist-active"
    return message