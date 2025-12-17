from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('resumes', views.ResumeViewSet, basename='resume')

urlpatterns = router.urls