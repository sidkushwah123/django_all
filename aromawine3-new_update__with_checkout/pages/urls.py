from django.urls import path
from . import views


urlpatterns = [
    path('<slug:type>/', views.PageContentView.as_view(),name="page"),
]