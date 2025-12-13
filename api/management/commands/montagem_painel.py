import datetime
from datetime import timedelta

from django.core.management.base import BaseCommand
from time import sleep

from api.models import Voo, DetalheHorarioVoo, StatusVoo


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando task background...'))
        try:
            while True:
                try:
                    self.atualiza_voos_ativos()
                except Exception as e:
                    print("Ocorreu um erro inesperado: ", e)
                    self.stdout.write(self.style.ERROR('Falha ao realizar a integração: '))
                sleep(3)  # Aguarda 5 segundos para próxima chamada

        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('Task voos finalizada'))

    def atualiza_voos_ativos(self):
        voos = Voo.objects.filter(ativo=True)
        for voo in voos:
            detalhe_horario_voo = DetalheHorarioVoo.objects.filter(voo=voo).first()
            if not StatusVoo.objects.filter(voo=voo).exists():
                StatusVoo.objects.create(
                    voo=voo,
                    status="CONFIRMADO",
                )
            agora = datetime.datetime.now()
            horario_embarque = detalhe_horario_voo.previsao_decolagem - timedelta(seconds=15)
            if agora > horario_embarque:
                StatusVoo.objects.create(
                    voo=voo,
                    status="EMBARCANDO",
                )
            ultima_chamada = detalhe_horario_voo.previsao_decolagem - timedelta(seconds=5)
            if agora > ultima_chamada:
                StatusVoo.objects.create(
                    voo=voo,
                    status="ULTIMA_CHAMADA",
                )
            decolado = detalhe_horario_voo.horario_decolagem
            if decolado is not None:
                StatusVoo.objects.create(
                    voo=voo,
                    status="DECOLADO",
                )
            aproximando = detalhe_horario_voo.previsao_pouso - timedelta(seconds=10)
            if agora > aproximando:
                StatusVoo.objects.create(
                    voo=voo,
                    status="APROXIMANDO",
                )

            pousado = detalhe_horario_voo.previsao_pouso - timedelta(seconds=5)
            if agora > pousado:
                StatusVoo.objects.create(
                    voo=voo,
                    status="POUSADO",
                )
            desembarcando = detalhe_horario_voo.previsao_pouso
            if desembarcando is not None:
                StatusVoo.objects.create(
                    voo=voo,
                    status="DESEMBARCANDO",
                )
