from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.quiz.models import Quiz
from common.serializers.quiz.serializer import QuizCreateSerializer, QuizUpdateSerializer, QuizListSerializer, \
    QuizDetailSerializer


class QuizModelViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.select_related("user").distinct()
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = [IsAuthenticated]
    # serializer_class = QuizListSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return QuizCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return QuizUpdateSerializer
        elif self.action == "retrieve":
            return QuizDetailSerializer
        return QuizListSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response({
            "message": "Quiz yaratildi!",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response({
            "message": "Quiz o'zgartirildi!",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            "message": "Quiz o'chirildi!",
        }, status=status.HTTP_200_OK)


