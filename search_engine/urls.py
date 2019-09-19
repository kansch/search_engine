from django.urls import path, include

from rest_framework import routers

from data import views


router = routers.DefaultRouter()
router.register(r'campers', views.CamperViewSet, 'camper')


urlpatterns = [
    path('api/', include(router.urls)),
]
