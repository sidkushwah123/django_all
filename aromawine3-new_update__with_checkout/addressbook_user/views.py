from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from .forms import AwAddressBookForm
from django.urls import reverse_lazy
from .models import AwAddressBook
from datetime import datetime
from wineproject import settings
from django.contrib import messages
from django.contrib.auth.models import User
from admin_manage_setting.models import AwManageShipping

#api 
from .serializer import AddressBookListapiserializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import  exceptions
# Create your views here.

@method_decorator(login_required , name="dispatch")
class AddressBookList(generic.TemplateView):
    template_name = "web/user/page/addressbook/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Page_title'] = "Address-book"
        context['BASE_URL'] = settings.BASE_URL
        get_address = None
        if AwAddressBook.objects.filter(User=self.request.user).exists():
            get_address = AwAddressBook.objects.filter(User=self.request.user)
        context['object_list'] = get_address
        return context

class AddressBookListapi(APIView):

    def post(self,request):
        user = request.data['User_id']
        messages = None
        data = None
        if user == "":
            messages = "user id is incorrect"
        else:
            if User.objects.filter(id=user).exists():
                User_id_data = get_object_or_404(User,id=user)
                if AwAddressBook.objects.filter(User=User_id_data).exists():
                    get_address = AwAddressBook.objects.filter(User=User_id_data)
                    get_data = AddressBookListapiserializer(get_address, many=True)
                    data = get_data.data
                    messages = str(len(get_address)) + " address available"
                else:
                    messages = "no address available."                                 
            else:
                messages = "id is incorrect "           
        return Response({ "message": messages,"address":data})



@method_decorator(login_required , name="dispatch")
class AddNewAddress(SuccessMessageMixin,generic.CreateView):
    form_class = AwAddressBookForm
    template_name = 'web/user/page/addressbook/create.html'
    success_url = reverse_lazy('addressbook_user:addressbooklist')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Page_title'] = "Add-New-Address"
        return context

    def get_success_message(self, cleaned_data):
        return "Address add successfully."

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.User = self.request.user
        self.object.save()
        form.save()
        return super().form_valid(form)

class AddNewAddressapi(APIView):

    def post(self,request):
        user = request.data['User_id']
        First_Name = request.data['First_Name']
        Last_Name = request.data['Last_Name']
        Email = request.data['Email']
        Pnone_no = request.data['Pnone_no']
        Conpany_Name = request.data['Conpany_Name']
        Country = request.data['Country']
        City = request.data['City']
        State = request.data['State']
        Address = request.data['Address']
        Address_2 = request.data['Address_2']
        Postcode = request.data['Postcode']
        Landmark = request.data['Landmark']

        messages = None
        status = "0"
        
        serializer = AddressBookListapiserializer(data=request.data)
        data_response = {}
        if serializer.is_valid():
            if user == "":
                messages = "user id is incorrect"
            else:
                if User.objects.filter(id=user).exists():               
                    if Country == "":
                        messages = "incorect country id"
                    else :   
                        Country2 = get_object_or_404(AwManageShipping,id=Country)
                        User_id_data = get_object_or_404(User,id=user)
                        data = AwAddressBook(User=User_id_data,First_Name=First_Name,Last_Name=Last_Name,Email=Email,Pnone_no=Pnone_no,Conpany_Name=Conpany_Name,Country=Country2,City=City,State=State,Address=Address,Address_2=Address_2,Postcode=Postcode,Landmark=Landmark)
                        data.save()  
                        status = "1"   
                        messages = "address save succesfully"                         
                else:
                    messages = "id is incorrect" 
        else:
            data_response = serializer.errors
            return Response({"status":status,"message": messages,"error":data_response})
        return Response({"status":status,"message": messages})


@method_decorator(login_required , name="dispatch")
class AddressUpdateView(SuccessMessageMixin,generic.UpdateView):
    form_class = AwAddressBookForm
    template_name = 'web/user/page/addressbook/create.html'
    queryset = AwAddressBook.objects.all()
    success_url = reverse_lazy('addressbook_user:addressbooklist')

    def get_success_message(self, cleaned_data):
        return "Address update successfully."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Page_title'] = "Edit-Address"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.Update_Date = datetime.now()
        self.object.save()
        form.save()
        return super().form_valid(form)


class AddressUpdateView_api(APIView):
    
    def post(self,request):
        address_id = request.data['address_id']
        user = request.data['User_id']
        First_Name = request.data['First_Name']
        Last_Name = request.data['Last_Name']
        Email = request.data['Email']
        Pnone_no = request.data['Pnone_no']
        Conpany_Name = request.data['Conpany_Name']
        Country = request.data['Country']
        City = request.data['City']
        State = request.data['State']
        Address = request.data['Address']
        Address_2 = request.data['Address_2']
        Postcode = request.data['Postcode']
        Landmark = request.data['Landmark']

        messages = None
        status = "0"

        if address_id == "":
            messages = "addresh_id is incorect"



        else:
            if AwAddressBook.objects.filter(id=address_id).exists():
                serializer = AddressBookListapiserializer(data=request.data)
                data_response = {}
                if serializer.is_valid():
                    if user == "":
                        messages = "user id is incorrect"
                    else:
                        if User.objects.filter(id=user).exists():               
                            if Country == "":
                                messages = "incorect country id"
                            else :   
                                Country2 = get_object_or_404(AwManageShipping,id=Country)
                                User_id_data = get_object_or_404(User,id=user)
                                AwAddressBook.objects.filter(id=address_id).update(User=User_id_data,First_Name=First_Name,Last_Name=Last_Name,Email=Email,Pnone_no=Pnone_no,Conpany_Name=Conpany_Name,Country=Country2,City=City,State=State,Address=Address,Address_2=Address_2,Postcode=Postcode,Landmark=Landmark)
                                status = "1"   
                                messages = "address update succesfully"                         
                        else:
                            messages = "id is incorrect" 
                else:
                    data_response = serializer.errors
                    return Response({"status":status,"message": messages,"error":data_response})
            else:
                messages = "addresh_id is incorect"
        return Response({"status":status,"message": messages})

        
    








@login_required
def RemoveAddress(request,pk):
    if AwAddressBook.objects.filter(id=pk).filter(User = request.user):
        get_instance = get_object_or_404(AwAddressBook, id=pk,User = request.user)
        get_instance.delete()
        messages.info(request, 'Address remove successfully')
    else:
        messages.error(request, "Adress is not deleted.")
    return redirect(settings.BASE_URL+"user/addressbook/")



class RemoveAddress_api(APIView):

    def post(self,request):

        address_id = request.data['address_id']
        messages = None
        status = "0"

        
        if address_id == "":
            messages = "Address id is incorrect"
        else:
            if AwAddressBook.objects.filter(id=address_id).exists():
                get_instance = get_object_or_404(AwAddressBook, id=address_id)
                get_instance.delete()
                status = "1"
                messages =  "Address remove successfully"
            else:
                messages = "Address id is incorrect"

        return Response({"status":status,"message": messages})



