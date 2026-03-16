from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.quiz.models.quiz import Quiz
from apps.quiz.services.quiz_result import submit_quiz
from common.serializers.quiz.serializer import QuizCreateSerializer, QuizUpdateSerializer, QuizListSerializer, \
    QuizDetailSerializer, QuizSubmitSerializer


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.select_related('lesson').annotate(questions_count=Count("questions"))
    http_method_names = ['get', 'post', 'patch', 'delete']


    def get_serializer_class(self):
        if self.action == 'create':
            return QuizCreateSerializer

        elif self.action == 'retrieve':
            return QuizDetailSerializer

        elif self.action in ['update', 'partial_update']:
            return QuizUpdateSerializer

        elif self.action == 'submit':
            return QuizSubmitSerializer

        return QuizListSerializer



    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


    @action(detail=True, methods=["post"], url_path="submit")
    def submit(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quiz = self.get_object()
        answers = []

        for item in serializer.validated_data["answers"]:
            try:
                question = quiz.questions.get(id=item["question"])
            except quiz.questions.model.DoesNotExist:
                raise ValidationError({"question": "Invalid question for this quiz."})

            try:
                variant = question.variants.get(id=item["variant"])
            except question.variants.model.DoesNotExist:
                raise ValidationError({"variant": "Invalid variant for this question."})

            answers.append({
                "question": question,
                "variant": variant,
            })

        result = submit_quiz(
            user=request.user,
            quiz=quiz,
            answers=answers,
        )

        return Response(
            {
                "quiz": str(result.quiz.id),
                "user": result.user.username,
                "correct_answers": result.correct_answers,
                "wrong_answers": result.wrong_answers,
                "total_questions": result.total_questions,
                "total": str(result.total),
                "status": result.status,
            },
            status=status.HTTP_200_OK,
        )

