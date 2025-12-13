from django.core.management.base import BaseCommand
from time import sleep

from api.integracao import integracao_voos_ativos, integracao_voos_finalizados
from api.models import Voo, Companhia, Aeroporto, PosicaoVoo, DetalheHorarioVoo


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
            self.stdout.write(self.style.WARNING('Task voos finalizada'))

    def atualiza_voos(self, voos):
        print(voos)
        for voo in voos:
            if Voo.objects.filter(id_api=voo['id'], ativo=True).exists():
                voo_recuperado = Voo.objects.filter(id_api=voo['id']).first()
                if not PosicaoVoo.objects.filter(voo=voo_recuperado, posicao=voo['posicao']).exists():
                    PosicaoVoo.objects.create(
                        voo=voo_recuperado,
                        posicao=voo['posicao'],
                    )
                    detalhe_horario_voo = DetalheHorarioVoo.objects.filter(voo=voo_recuperado).first()
                    if voo['posicao'] == "Em voo":
                        detalhe_horario_voo.horario_decolagem = voo['horario_decolagem']
                        detalhe_horario_voo.previsao_pouso = voo['previsao_pouso']
                        detalhe_horario_voo.save()
                    elif voo['posicao'] == "Destino":
                        detalhe_horario_voo.horario_pouso = voo['horario_pouso']
                        detalhe_horario_voo.save()
            else:
                voo_create = Voo.objects.create(
                    id_api=voo['id'],
                    codigo=str(voo['codigo_voo']),
                    companhia=Companhia.objects.filter(nome=voo['companhia']).first(),
                    origem=Aeroporto.objects.filter(nome=voo['origem']).first(),
                    destino=Aeroporto.objects.filter(nome=voo['destino']).first(),
                )
                PosicaoVoo.objects.create(
                    voo=voo_create,
                    posicao=voo['posicao'],
                )
                DetalheHorarioVoo.objects.create(
                    voo=voo_create,
                    previsao_decolagem=voo['previsao_decolagem'],
                )

    def finaliza_voos(self, voos):
        for voo in voos:
            if Voo.objects.filter(id_api=voo['id'], ativo=True).exists():
                voo_recuperado = Voo.objects.filter(id_api=voo['id']).first()
                voo_recuperado.ativo = False
                voo_recuperado.save()
                PosicaoVoo.objects.create(
                    voo=voo_recuperado,
                    posicao=voo['posicao'],
                )
