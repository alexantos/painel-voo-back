from rest_framework import serializers

from api.models import Voo, Companhia, Aeroporto, Cidade, StatusVoo


class PainelSerializer(serializers.ModelSerializer):
    companhia = serializers.SerializerMethodField()
    destino = serializers.SerializerMethodField()
    portao = serializers.SerializerMethodField()
    hora = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Voo
        fields = ["codigo", "companhia", "destino", "portao", "hora", "status"]

    def get_companhia(self, obj):
        return Companhia.objects.get(id=obj.companhia.id).nome

    def get_destino(self, obj):
        return Cidade.objects.get(nome=Aeroporto.objects.get(id=obj.destino.id).cidade).nome

    def get_portao(self, obj):
        return StatusVoo.objects.filter(voo=obj).last().portao

    def get_hora(self, obj):
        return StatusVoo.objects.filter(voo=obj).last().data_hora

    def get_status(self, obj):
        return StatusVoo.objects.filter(voo=obj).last().status