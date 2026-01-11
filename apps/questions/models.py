from django.db import models

from apps.quiz.models import Quiz
from common import BaseModel


class Questions(BaseModel):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    points = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Questions"
        verbose_name_plural = "Questions"
        db_table = "questions"

    def __str__(self):
        return self.text



