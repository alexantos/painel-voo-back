from datetime import timedelta

from django.core.management.base import BaseCommand
from time import sleep

from django.utils import timezone

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
            status_voo = StatusVoo.objects.filter(voo=voo)
            if not status_voo.exists():
                StatusVoo.objects.create(
                    voo=voo,
                    status="CONFIRMADO",
                )
            agora = timezone.localtime(timezone.now())
            if detalhe_horario_voo.previsao_decolagem is not None:
                horario_embarque = detalhe_horario_voo.previsao_decolagem - timedelta(seconds=15)
                if agora > horario_embarque and not status_voo.filter(status="EMBARCANDO").exists():
                    StatusVoo.objects.create(
                        voo=voo,
                        status="EMBARCANDO",
                    )
                ultima_chamada = detalhe_horario_voo.previsao_decolagem - timedelta(seconds=5)
                if ultima_chamada is not None and agora > ultima_chamada and not status_voo.filter(status="ULTIMA_CHAMADA").exists():
                    StatusVoo.objects.create(
                        voo=voo,
                        status="ULTIMA_CHAMADA",
                    )
            decolado = detalhe_horario_voo.horario_decolagem
            if decolado is not None and not status_voo.filter(status="DECOLADO").exists():
                StatusVoo.objects.create(
                    voo=voo,
                    status="DECOLADO",
                )
            if detalhe_horario_voo.previsao_pouso is not None:
                aproximando = detalhe_horario_voo.previsao_pouso - timedelta(seconds=10)
                if aproximando is not None and agora > aproximando and not status_voo.filter(status="APROXIMANDO").exists():
                    StatusVoo.objects.create(
                        voo=voo,
                        status="APROXIMANDO",
                    )
                pousado = detalhe_horario_voo.previsao_pouso - timedelta(seconds=5)
                if pousado is not None and agora > pousado and not status_voo.filter(status="POUSADO").exists():
                    StatusVoo.objects.create(
                        voo=voo,
                        status="POUSADO",
                    )
            desembarcando = detalhe_horario_voo.horario_pouso
            if desembarcando is not None and not status_voo.filter(status="DESEMBARCANDO").exists():
                StatusVoo.objects.create(
                    voo=voo,
                    status="DESEMBARCANDO",
                )
