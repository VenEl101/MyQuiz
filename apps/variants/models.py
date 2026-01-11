from django.db import models

from apps.questions.models import Questions
from common import BaseModel


class Variant(BaseModel):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='variants')
    text = models.TextField()
    is_true = models.BooleanField(default=False)
