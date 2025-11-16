import datetime

from django.core.management.base import BaseCommand
from time import sleep

from api.integracao import integracao_aeroporto
from api.models import Cidade, Voo, Companhia, Aeroporto, StatusVoo


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando task voos...'))
        try:
            while True:
                response = integracao_aeroporto()
                self.atualiza_voos(voos=response)
                sleep(10)  # Aguarda 5 segundos para próxima chamada
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('Task voos finalizada'))

    def atualiza_voos(self, voos):
        print(voos)
        for voo in voos:
            voo_create = Voo.objects.create(
                codigo=str(voo['codigo_voo']),
                companhia=Companhia.objects.filter(nome=voo['companhia']).first(),
                origem=Aeroporto.objects.filter(nome=voo['origem']).first(),
                destino=Aeroporto.objects.filter(nome=voo['destino']).first(),
            )
            status_voo = StatusVoo.objects.create(
                voo=voo_create,
                posicao=voo['posicao'],
                data_hora=datetime.datetime.now()
            )
            print('Salvo: ', voo_create, status_voo)
