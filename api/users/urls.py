from django.urls import path, include



urlpatterns = [
    path('auth/', include('api.users.auth.urls')),
    path('quiz/', include('api.users.quizzes.urls')),
    path('orders/', include('api.users.orders.urls')),
]
