from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'user', views.UserViewSet)

app_name = 'accounts_api'

urlpatterns = router.urls
