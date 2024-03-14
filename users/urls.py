from users.api.viewsets import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserAPIView)
urlpatterns = router.urls


# urlpatterns = [
#     path('users/', UserAPIView.as_view()),
#     path('users/<str:slug>/', UserAPIView.as_view()),
# ]
