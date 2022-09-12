from users.views import (UserSignUpAPIView,
                         VerifyEmailAPIView,
                         UserLoginAPIView,
                         CompleteUserProfileAPIView)
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/signup/', UserSignUpAPIView.as_view(), name='signup'),
    path('users/complete-profile/', CompleteUserProfileAPIView.as_view(), name='complete-profile'),
    path('user/email-verification', VerifyEmailAPIView.as_view(), name='email_verification'),
    path('users/login/', UserLoginAPIView.as_view(), name='login'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
