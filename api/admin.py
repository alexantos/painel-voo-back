from django.contrib import admin

from api.models import Cidade, Aeroporto, Voo, Companhia, StatusVoo, PosicaoVoo, DetalheHorarioVoo

admin.site.register(Cidade)
admin.site.register(Aeroporto)
admin.site.register(Companhia)
admin.site.register(Voo)
admin.site.register(StatusVoo)
admin.site.register(PosicaoVoo)
admin.site.register(DetalheHorarioVoo)
