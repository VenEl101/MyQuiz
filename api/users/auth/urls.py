from rest_framework import routers

from api.users.auth.views import AuthViewSet

router = routers.DefaultRouter()


router.register('', AuthViewSet, basename='auth')

urlpatterns = router.urls