from django.urls import path

from api.users.auth.views import RegisterAPIView, LoginAPIView, ResetPasswordAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('reset-password/<uuid:user_id>/password/', ResetPasswordAPIView.as_view(), name='reset-password'),
]