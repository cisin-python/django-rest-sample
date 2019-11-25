"""Registration serializer managed here."""

from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""

    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate_password(self, password):
        """Check password validation."""
        if password == "":
            raise serializers.ValidationError(_("fill the password field"))
        return password

    def validate(self, data):
        """Validation on both of the fields."""
        username = data.get('username')
        password = self.validate_password(data.get('password'))
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError(_("Username does not exists"))
        authenticated_user = authenticate(
            username=user.username, password=password,)
        if authenticated_user:
            data['authenticated_user'] = authenticated_user
        else:
            raise serializers.ValidationError(_("Invalid credentials"))
        return data
