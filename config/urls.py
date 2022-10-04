from users.views import (UserSignUpAPIView,
                         VerifyEmailAPIView,
                         UserLoginAPIView,
                         CompleteUserProfileAPIView)
from wpo_logic.views import (CodigosPostalesAPIView,
                             SportsLocationAPIView,
                             SportsLocationUploadImage)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/signup/', UserSignUpAPIView.as_view(), name='signup'),
    path('users/complete-profile/', CompleteUserProfileAPIView.as_view(), name='complete-profile'),
    path('user/email-verification', VerifyEmailAPIView.as_view(), name='email_verification'),
    path('users/login', UserLoginAPIView.as_view(), name='login'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('wpo_logic/codigos-postales/', CodigosPostalesAPIView.as_view(), name='codigos postales'),
    path('wpo_logic/sport-locations/', SportsLocationAPIView.as_view(), name='sport locations'),
    path('wpo_logic/sport-locations/upload-image/', SportsLocationUploadImage.as_view(), name='sport locations image'),
]
