# auth_app/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    class Meta:
        model = User
        fields = ("name", "phone", "email", "password")

    def validate(self, attrs):
        # additional checks can be added here (e.g., phone format)
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        # role will be set in view (first user => ADMIN) or keep default
        user.save()
        return user

class UserSafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Do not include password or refresh_token
        fields = ("id", "name", "phone", "email", "role", "created_at")
