from rest_framework import routers

from api.users.my_quiz.views import QuizModelViewSet

router = routers.DefaultRouter()

router.register("", QuizModelViewSet, basename="my_quizzes")

urlpatterns = router.urls
