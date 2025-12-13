import datetime

from django.core.management.base import BaseCommand
from time import sleep

from api.integracao import integracao_voos_ativos, integracao_voos_finalizados
from api.models import Voo, Companhia, Aeroporto, StatusVoo


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando task voos...'))
        try:
            while True:
                try:
                    voos_ativos = integracao_voos_ativos()
                    self.atualiza_voos(voos=voos_ativos)
                    voos_finalizados = integracao_voos_finalizados()
                    self.finaliza_voos(voos=voos_finalizados)
                except Exception as e:
                    print("Ocorreu um erro inesperado: ", e)
                    self.stdout.write(self.style.ERROR('Falha ao realizar a integração: '))
                sleep(5)  # Aguarda 5 segundos para próxima chamada

        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('Task voos finalizada'))

    def atualiza_voos(self, voos):
        print(voos)
        for voo in voos:
            if Voo.objects.filter(id_api=voo['id'], ativo=True).exists():
                voo_recuperado = Voo.objects.filter(id_api=voo['id']).first()
                status_voo = StatusVoo.objects.create(
                    voo=voo_recuperado,
                    posicao=voo['posicao'],
                    data_hora=datetime.datetime.now()
                )
            else:
                voo_create = Voo.objects.create(
                    codigo=str(voo['codigo_voo']),
                    id_api=voo['id'],
                    companhia=Companhia.objects.filter(nome=voo['companhia']).first(),
                    origem=Aeroporto.objects.filter(nome=voo['origem']).first(),
                    destino=Aeroporto.objects.filter(nome=voo['destino']).first(),
                )
                status_voo = StatusVoo.objects.create(
                    voo=voo_create,
                    posicao=voo['posicao'],
                    data_hora=datetime.datetime.now()
                )
            print('Salvo: ', status_voo)

    def finaliza_voos(self, voos):
        for voo in voos:
            if Voo.objects.filter(id_api=voo['id'], ativo=True).exists():
                voo_recuperado = Voo.objects.filter(id_api=voo['id']).first()
                voo_recuperado.ativo = False
                voo_recuperado.save()
                StatusVoo.objects.create(
                    voo=voo_recuperado,
                    posicao=voo['posicao'],
                    data_hora=datetime.datetime.now()
                )