from django.db import models
from apps.course.models.units import CourseUnit
from common import BaseModel


class Lessons(BaseModel):
    course_unit = models.ForeignKey(CourseUnit, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=120)
    desc = models.TextField()
    video = models.FileField(upload_to='lessons/video', blank=True, null=True)
    presentation = models.FileField(upload_to='lessons/presentation', blank=True, null=True)
    additional_task = models.CharField(max_length=120)


    class Meta:
        db_table = 'lessons'

    def __str__(self):
        return f"{self.title} - {self.id}"

