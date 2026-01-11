
from django.db import models
import uuid
from django.utils.text import slugify
from apps.user.models import User
from common import BaseModel


class Quiz(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes")
    quiz_img = models.ImageField(upload_to="quizzes/", null=True, blank=True)
    title = models.CharField("Title", max_length=255)
    description = models.TextField()
    password = models.CharField("Password", max_length=255, blank=True, null=True)
    time_limit = models.IntegerField("Time Limit", blank=True, null=True)
    is_finished = models.BooleanField("Finished", default=False)

    slug = models.SlugField(
        max_length=300,
        unique=True,
        blank=True,
        editable=False
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            while True:
                random_part = uuid.uuid4().hex[:6]
                slug = f"{base_slug}--{random_part}"
                if not Quiz.objects.filter(slug=slug).exists():
                    self.slug = slug
                    break

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Quizzes"
        verbose_name_plural = "Quizzes"
        db_table = "quizzes"

    def __str__(self):
        return self.title