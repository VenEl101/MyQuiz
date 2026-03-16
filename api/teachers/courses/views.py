from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.course.models.course import Course
from common.permission import IsCourseTeacherOrAdmin
from common.serializers.courses.course import CourseCreateSerializer, CourseUpdateSerializer, CourseUserListSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = [IsAuthenticated, IsCourseTeacherOrAdmin]

    def get_serializer_class(self):
        if self.action == 'create':
            return CourseCreateSerializer

        if self.action in ['update', 'partial_update']:
            return CourseUpdateSerializer

        return CourseUserListSerializer


    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)