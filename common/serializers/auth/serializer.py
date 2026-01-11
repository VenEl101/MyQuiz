import secrets
from django.contrib.auth import authenticate
from rest_framework import serializers
from apps.user.models import User
from django.contrib.auth.password_validation import validate_password


class TelegramUserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone", "first_name", "lastname"]

    def create(self, validated_data):
        # Random temporary password yaratish
        temp_password = secrets.token_urlsafe(16)

        user = User(
            phone=validated_data["phone"],
            first_name=validated_data["first_name"],
            lastname=validated_data["lastname"],
            username=validated_data["phone"]
        )
        user.save()

        # Shu random password kerak bo'lsa, qaytarish mumkin (faqat logikada)
        user.temp_password = temp_password
        return user



class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        phone = data.get("phone")
        password = data.get("password")

        # Foydalanuvchini topish
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError({"phone": "User with this phone does not exist."})

        if user.is_temporary_password:
            data["user"] = user
            return data

        # Normal credential tekshirish
        authenticated_user = authenticate(username=user.username, password=password)
        if not authenticated_user:
            raise serializers.ValidationError({"password": "Incorrect password."})

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

