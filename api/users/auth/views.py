from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.models import User
from common.serializers.auth.serializer import TelegramUserRegisterSerializer, LoginSerializer, UpdatePasswordSerializer


class RegisterAPIView(CreateAPIView):
    serializer_class = TelegramUserRegisterSerializer


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')


        if user.is_temporary_password:
            return Response({
                "detail": "You need to set your password first.",
                "user_id": user.id
            }, status=400)

        # JWT token yaratish
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "message": f"Welcome {user.first_name}!",
            "user_id": user.id,
            "phone": user.phone,
            "access": access_token,
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)



class ResetPasswordAPIView(GenericAPIView):
    serializer_class = UpdatePasswordSerializer

    def patch(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        # Yangi JWT token (faqat agar o'z useri bo'lsa qaytarish mumkin)
        tokens = {}
        if user == request.user:
            refresh = RefreshToken.for_user(user)
            tokens = {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }

        return Response({
            "message": "Password updated successfully",
            **tokens
        }, status=status.HTTP_200_OK)