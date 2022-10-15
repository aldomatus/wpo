import re
from django.contrib.auth import password_validation

#  Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

#  Models
from users.models import (CustomUser, CtDomainWhitelist, CtState)


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""
    class Meta:
        """Meta class."""

        model = CustomUser
        fields = (
            'user_name',
            'user_last_name',
            'email',
            'state_id'
        )


class UserSignUpSerializer(serializers.Serializer):
    """User sign up serializer.
    Handle sign up data validation and user/profile creation.
    """
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    # Password
    password = serializers.CharField(min_length=8)
    password_confirmation = serializers.CharField(min_length=8)

    # Name
    user_name = serializers.CharField(min_length=2, max_length=100)
    user_last_name = serializers.CharField(min_length=2, max_length=100)

    # Estado
    state_id = serializers.IntegerField()

    def validate(self, data):
        """Verify passwords match."""
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords don't match.")
        password_validation.validate_password(passwd)
        return data

    @staticmethod
    def domain_validator(email):
        wl_results = CtDomainWhitelist.objects.all()
        white_list = [i.domain_wl_dominio for i in wl_results]
        pat = "^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,3}$"
        if not re.match(pat, email):
            raise Exception("Invalid Email")
        res = email[email.index('@') + 1:]

        if res in white_list:
            return True
        else:
            return False

    def create(self, data):
        """Handle user and profile creation."""
        data.pop('password_confirmation')
        data['state_id'] = CtState.objects.get(state_id=data['state_id']).state_id
        data['is_active'] = False
        user = CustomUser.objects.create_user(**data)
        # profile = profiles.objects.create(user=user)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
