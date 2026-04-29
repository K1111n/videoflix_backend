from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Validate and create a new inactive user from email and password."""

    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirmed_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """Ensure passwords match and the email is not already registered."""
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError('Passwords do not match.')
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Please check your inputs and try again.')
        return data

    def create(self, validated_data):
        """Create and return a new user, removing the confirmation field first."""
        validated_data.pop('confirmed_password')
        return User.objects.create_user(**validated_data)


class PasswordConfirmSerializer(serializers.Serializer):
    """Validate that new_password and confirm_password match."""

    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Raise a validation error if both password fields are not identical."""
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError('Passwords do not match.')
        return data


class LoginSerializer(serializers.Serializer):
    """Deserialize and validate email and password for login."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
