from django.urls import include, path
from rest_framework import routers

from api.views import PainelView

router = routers.DefaultRouter()
router.register(r"painel", PainelView)

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
