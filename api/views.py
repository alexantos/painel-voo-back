from django.shortcuts import render
from rest_framework import viewsets

from api.models import Voo
from api.serializers import PainelSerializer


class PainelView(viewsets.ModelViewSet):
    queryset = Voo.objects.all()
    serializer_class = PainelSerializer
    permission_classes = []  # permissions.IsAuthenticated
