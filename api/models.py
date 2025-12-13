import uuid

from django.db import models

from api.choices import STATUS, POSICAO


class Cidade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(max_length=4)
    nome = models.CharField(max_length=64)

    def __str__(self):
        return self.nome


class Aeroporto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(max_length=4)
    nome = models.CharField(max_length=64)
    cidade = models.ForeignKey(to=Cidade, on_delete=models.PROTECT)

    def __str__(self):
        return self.codigo


class Companhia(models.Model):
    nome = models.CharField(max_length=64)

    def __str__(self):
        return self.nome


class Voo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_api = models.UUIDField()
    codigo = models.CharField(max_length=8)
    companhia = models.ForeignKey(to=Companhia, on_delete=models.PROTECT)
    origem = models.ForeignKey(to=Aeroporto, on_delete=models.PROTECT, related_name='aeroporto_origem')
    destino = models.ForeignKey(to=Aeroporto, on_delete=models.PROTECT, related_name='aeroporto_destino')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.codigo


class DetalheHorarioVoo(models.Model):
    voo = models.ForeignKey(to=Voo, on_delete=models.PROTECT)
    previsao_decolagem = models.DateTimeField()
    horario_decolagem = models.DateTimeField(null=True)
    previsao_pouso = models.DateTimeField(null=True)
    horario_pouso = models.DateTimeField(null=True)

    def __str__(self):
        return self.voo.codigo


class PosicaoVoo(models.Model):  # Surte efeito many to one, para cada voo tem o histórico de cada atualização de status
    voo = models.ForeignKey(to=Voo, on_delete=models.PROTECT)
    posicao = models.CharField(choices=POSICAO, max_length=16)  # Origem, EmVoo, Destino

    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    # Criar lógica no gerador e na modelagem para embarque e desembarque detalhados...
    # status = models.CharField(choices=STATUS, max_length=16)
    # portao = models.CharField(max_length=2, null=True, blank=True)

    # history = django_history

    def __str__(self):
        return self.voo.codigo + self.posicao


class StatusVoo(models.Model):
    voo = models.ForeignKey(to=Voo, on_delete=models.PROTECT)
    status = models.CharField(choices=STATUS, max_length=16)

    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.voo.codigo + self.status

# class Aeronave(models.Model):
#     modelo
#     capacidade
#     status
