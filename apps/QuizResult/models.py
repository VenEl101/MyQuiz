from django.db import models

from apps.quiz.models import Quiz
from apps.user.models import User
from common import BaseModel



class QuizResult(BaseModel):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.IntegerField(default=0)
    correct = models.IntegerField(default=0)
    incorrect = models.IntegerField(default=0)
    status = models.CharField(default=0)


