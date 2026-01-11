from django.urls import path, include



urlpatterns = [
    path('auth/', include('api.users.auth.urls')),
    path('my-quiz/', include('api.users.my_quiz.urls')),
    path('quiz/', include('api.users.quizzes.urls')),
]