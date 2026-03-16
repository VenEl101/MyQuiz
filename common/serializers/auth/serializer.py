from django.contrib.auth import authenticate
from rest_framework import serializers
from apps.user.models import User
from django.contrib.auth.password_validation import validate_password



class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        email = data.get("email")
        username = data.get("username")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists.")

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already exists.")

        return data


class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)



class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "User with this email does not exist."}
            )

        authenticated_user = authenticate(
            email=user.email,
            password=password,
        )

        if not authenticated_user:
            raise serializers.ValidationError(
                {"password": "Incorrect password."}
            )

        data["user"] = authenticated_user
        return data



class UpdatePasswordSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(required=True, write_only=True)
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate_new_password1(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        if data.get("new_password1") != data.get("new_password2"):
            raise serializers.ValidationError({"new_password1": "New passwords must match."})
        return data

    def save(self, user, **kwargs):
        user.set_password(self.validated_data["new_password1"])
        if getattr(user, "is_temporary_password", False):
            user.is_temporary_password = False
        user.save()
        return user

