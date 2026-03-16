from django.urls import path, include



urlpatterns = [
    path('course/', include('api.teachers.courses.urls')),
]