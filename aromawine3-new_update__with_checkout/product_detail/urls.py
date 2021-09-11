from django.urls import path
from . import views

urlpatterns = [
    path('', views.DetailView.as_view(),name="product_detail"),
    path('/api', views.DetailapiView.as_view(),name="product_detail_api"),
]