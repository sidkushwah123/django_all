from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.UserProfileView.as_view(),name="profile"),
    path('edit-presonal-details', views.PresonalDetailsView.as_view(),name="presonaldetails"),
    path('change-email-address', views.ChangeEmailView.as_view(),name="changeemail"),
    path('password_change', auth_view.PasswordChangeView.as_view(template_name='web/user/page/profile/chnage_password.html'),name="password_chaneg"),

]