from django.contrib import admin

from apps.course.models.course import Course
from apps.course.models.lessons import Lessons
from apps.course.models.student import CourseStudent

# Register your models here.


admin.site.register(Course)
admin.site.register(CourseStudent)
admin.site.register(Lessons)