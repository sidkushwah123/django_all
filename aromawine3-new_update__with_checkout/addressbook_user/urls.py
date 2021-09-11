from django.urls import path
from . import views

urlpatterns = [
    path('', views.AddressBookList.as_view(),name="addressbooklist"),
    path('add-new-address', views.AddNewAddress.as_view(),name="add_new_address"),
    path('<pk>/update-address', views.AddressUpdateView.as_view(),name="update_address"),
    path('<pk>/remove-address', views.RemoveAddress,name="RemoveAddress"),

    #********************==========================API PATH===============*************************
    path('api', views.AddressBookListapi.as_view(),name="AddressBookListapi"),
    path('add-new-address/api', views.AddNewAddressapi.as_view(),name="add_new_address_api"),
    path('remove-address/api', views.RemoveAddress_api.as_view(),name="RemoveAddress_api"),
    path('update-address/api', views.AddressUpdateView_api.as_view(),name="AddressUpdateView_api"),



]