from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter

# from api.user.payments.views import PaymentViewSet
from .views import welcome, get_logged_errors
from api.users.urls import urlpatterns as users_urlpatterns
# --- Admin API Swagger ---
# admin_schema_view = get_schema_view(
#     openapi.Info(
#         title="Save Meal Admin API",
#         default_version='v1',
#         description="Swagger documentation for Admin API endpoints.",
#         contact=openapi.Contact(email="admins@savemeal.uz"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     patterns=[
#         path('api/admins/', include('api.admin.urls')),
#     ]
# )
#
# # --- User API Swagger ---
user_schema_view = get_schema_view(
    openapi.Info(
        title="Save Meal User API",
        default_version='v1',
        description="Swagger documentation for User API endpoints.",
        contact=openapi.Contact(email="user@savemeal.uz"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    patterns=[
        path('api/users/', include('api.users.urls')),
    ]
)

teachers_schema_view = get_schema_view(
    openapi.Info(
        title="Save Meal User API",
        default_version='v1',
        description="Swagger documentation for User API endpoints.",
        contact=openapi.Contact(email="user@savemeal.uz"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    patterns=[
        path('api/teachers/', include('api.teachers.urls')),
    ]
)



router = DefaultRouter()
# router.register("payment", PaymentViewSet, basename="payments")

urlpatterns = [
    path('', welcome, name='index'),
    path('logs-all/', get_logged_errors, name='errors'),
    path('admin/', admin.site.urls),

    # API routes
    # path('api/admins/', include('api.admin.urls')),
    path('api/users/', include('api.users.urls')),
    path('api/teachers/', include('api.teachers.urls')),


    # --- Admin Swagger Docs ---
    # path('swagger/admins/', admin_schema_view.with_ui('swagger', cache_timeout=0), name='admins-swagger-ui'),
    #
    # --- User Swagger Docs ---
    path('swagger/users/', user_schema_view.with_ui('swagger', cache_timeout=0), name='user-swagger-ui'),
    path('swagger/teachers/', teachers_schema_view.with_ui('swagger', cache_timeout=0), name='user-swagger-ui'),

    # --- Business Swagger Docs ---
] + router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
