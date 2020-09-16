from rest_framework import routers
from .views import PostViewSet

app_name = 'blog_app'

router = routers.DefaultRouter()
router.register(r'post', PostViewSet, basename='post')

urlpatterns = router.urls
