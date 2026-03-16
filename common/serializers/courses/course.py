from rest_framework import serializers

from apps.course.models.course import Course
from apps.course.models.lessons import Lessons
from apps.course.models.units import CourseUnit
from common.serializers.courses.units import CourseUnitCreateSerializer, CourseUnitUpdateSerializer


class CourseUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "desc", "base_price", "discount_price"]




class CourseCreateSerializer(serializers.ModelSerializer):
    units = CourseUnitCreateSerializer(many=True)

    class Meta:
        model = Course
        fields = [
            "title",
            "desc",
            "base_price",
            "discount_price",
            "units",
        ]

    def create(self, validated_data):
        units_data = validated_data.pop("units", [])

        course = Course.objects.create(**validated_data)

        for unit_data in units_data:
            lessons_data = unit_data.pop("lessons", [])
            unit = CourseUnit.objects.create(course=course, **unit_data)

            for lesson_data in lessons_data:
                Lessons.objects.create(course_unit=unit, **lesson_data)

        return course



class CourseUpdateSerializer(serializers.ModelSerializer):
    units = CourseUnitUpdateSerializer(many=True)

    class Meta:
        model = Course
        fields = ["title", "desc", "base_price", "discount_price", "units"]


    def update(self, instance, validated_data):
        units_data = validated_data.pop("units", None)

        instance = super().update(instance, validated_data)

        if units_data is not None:
            instance.units.all().delete()

            for unit_data in units_data:
                lessons_data = unit_data.pop("lessons", [])
                unit = CourseUnit.objects.create(course=instance, **unit_data)

                for lesson_data in lessons_data:
                    Lessons.objects.create(course_unit=unit, **lesson_data)

        return instance
