from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from apps.quiz.models import Quiz
from common.serializers.quiz.serializer import QuizListSerializer, QuizDetailSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class QuizViewSet(ReadOnlyModelViewSet):
    queryset = Quiz.objects.select_related("user")


    def get_serializer_class(self):
        if self.action == "retrieve":
            return QuizDetailSerializer
        return QuizListSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'slug',
                openapi.IN_QUERY,
                description="Slug of the quiz (required)",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        slug = request.query_params.get("slug")
        if not slug:
            return Response({"detail": "Slug query parameter is required."}, status=400)

        queryset = self.get_queryset().filter(slug=slug, is_finished=False)
        if not queryset.exists():
            return Response({"detail": "Quiz not found or already finished."}, status=404)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


