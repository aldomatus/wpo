from django.urls import path
from users.views import (UserSignUpAPIView, VerifyEmailAPIView, UserLoginAPIView)
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/signup/', UserSignUpAPIView.as_view(), name='signup'),
    path('user/email-verification', VerifyEmailAPIView.as_view(), name='email_verification'),
    path('users/login/', UserLoginAPIView.as_view(), name='login'),
]