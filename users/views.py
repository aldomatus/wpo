"""Users views."""
# Imports
import jwt
import sys
import traceback
import phonenumbers

# Django
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings

# Django REST Framework
from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

# Others libraries
from phonenumbers import timezone, parse

# Simple JWT
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models.info_users import CtLocation

# Serializers
from users.serializers import (
    UserSignUpSerializer,
    UserModelSerializer
)

# Models
from users.models import (CustomUser, Profile)
from wpo_logic.models import CtSport

from .utils import Util

# for reset password email
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created


class UserSignUpAPIView(APIView):
    """User sign up API view."""
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        try:
            serializer = UserSignUpSerializer(data=request.data)
            if not serializer.domain_validator(request.data["email"]):
                raise Exception("Invalid email domain")

            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            data = UserModelSerializer(user).data

            user_token = CustomUser.objects.get(email=data['email'])
            token = RefreshToken.for_user(user_token).access_token
            current_site = get_current_site(request).domain
            relativeLink = reverse('email_verification')
            absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
            email_body = 'Hi ' + str(user_token.user_name) + ' use the next link to verify your email: ' + str(absurl)
            data = {'email_body': email_body, 'to_email': user_token.email, 'email_subject': 'Verify your email'}
            Util.send_email(data)
            return Response(data, status=status.HTTP_201_CREATED)

        except Exception as e:
            exc_tb = sys.exc_info()[2]
            return Response({"message": "something bad ocurred!",
                             "error": f"{str(e)} line: {exc_tb.tb_lineno}"
                             },
                            status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailAPIView(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = CustomUser.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()

            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as e:
            print(e)
            return Response({'error': 'Activation expired'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as e:
            print(e)
            return Response({'error': 'Decode error'}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(TokenObtainPairView):
    """User login API view."""
    permission_classes = [permissions.AllowAny]
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        user = authenticate(
            email=email,
            password=password
        )
        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = UserModelSerializer(user)

                return Response({
                    'access_token': login_serializer.validated_data.get('access'),
                    'refresh_token': login_serializer.validated_data.get('refresh'),
                    'user': user_serializer.data,
                    'message': 'Inicio de sesión exitoso'
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Contraseña incorrecta'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Contraseña incorrecta'}, status=status.HTTP_400_BAD_REQUEST)


class CompleteUserProfileAPIView(APIView):
    """User sign up API view."""

    # permission_classes = (IsAuthenticated,)

    def __init__(self):
        self.data = None

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        self.data = request.data
        try:
            self.data['location_id'] = CtLocation.objects.filter(
                location_id=self.data.pop('location_id')).first().location_id
            self.data['user_id'] = CustomUser.objects.filter(id=self.data.pop('user_id')).first().id
            self.data['sport_id'] = CtSport.objects.filter(sport_id=self.data.pop('sport_id')).first().sport_id

            if self.valid_phone_checker():
                profile = Profile.objects.create(**self.data)
                if profile:
                    response = {
                        "status": "OK",
                        "status_codes": 201,
                        "status_messages": f"{self.data['user_id']} completed profile"
                    }
                    return Response(response, status=status.HTTP_201_CREATED)
            else:
                raise Exception("Invalid phone number")

        except Exception as e:
            print(e)
            exc_info = sys.exc_info()
            print(''.join(traceback.format_exception(*exc_info)))
            return Response({"message": "something bad ocurred!",
                             "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def valid_phone_checker(self):
        phone = parse(self.data["profile_phone"], "GB")
        if phonenumbers.is_valid_number(phone):
            if 'America/Mexico_City' in timezone.time_zones_for_number(phone):
                return True
        return False


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.email,
        'firstName': reset_password_token.user.user_name,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('user_reset_password.html', context)
    email_plaintext_message = render_to_string('user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="We Play One"),
        # message:
        email_plaintext_message,
        # from:
        "contact@weplay.one",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
