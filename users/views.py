"""Users views."""
# Imports
import jwt
import sys

# Django
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings

# Django REST Framework
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

# Simple JWT
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Serializers
from users.serializers import (
    UserSignUpSerializer,
    UserModelSerializer
)

# Models
from users.models import (CustomUser,)

from .utils import Util


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
                    'refresh-token': login_serializer.validated_data.get('refresh'),
                    'user': user_serializer.data,
                    'message': 'Inicio de sesión exitoso'
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Contraseña incorrecta'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Contraseña incorrecta'}, status=status.HTTP_400_BAD_REQUEST)