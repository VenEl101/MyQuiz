from rest_framework import serializers

from apps.course.models.units import CourseUnit
from common.serializers.courses.lessons import LessonCreateSerializer, LessonUpdateSerializer


class CourseUnitCreateSerializer(serializers.ModelSerializer):
    lessons = LessonCreateSerializer(many=True)

    class Meta:
        model = CourseUnit
        fields = [
            "title",
            "desc",
            "lessons",
        ]




class CourseUnitUpdateSerializer(serializers.ModelSerializer):
    lessons = LessonUpdateSerializer(many=True)

    class Meta:
        model = CourseUnit
        fields = [
            "title",
            "desc",
            "lessons",
        ]