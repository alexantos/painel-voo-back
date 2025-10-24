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
    codigo = models.CharField(max_length=8)
    cidade = models.ForeignKey(to=Cidade, on_delete=models.PROTECT)

    def __str__(self):
        return self.codigo


class Companhia(models.Model):
    nome = models.CharField(max_length=64)

    def __str__(self):
        return self.nome


class Voo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(max_length=8)
    companhia = models.ForeignKey(to=Companhia, on_delete=models.PROTECT)
    origem = models.ForeignKey(to=Aeroporto, on_delete=models.PROTECT, related_name='aeroporto_origem')
    destino = models.ForeignKey(to=Aeroporto, on_delete=models.PROTECT, related_name='aeroporto_destino')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.codigo


class StatusVoo(models.Model):
    voo = models.ForeignKey(to=Voo, on_delete=models.PROTECT)
    status = models.CharField(choices=STATUS, max_length=16)
    posicao = models.CharField(choices=POSICAO, max_length=16)  # Origem, EmVoo, Destino
    portao = models.CharField(max_length=2, null=True, blank=True)
    data_hora = models.DateTimeField()

    # history = django_history

    def __str__(self):
        return self.voo.codigo

# class Aeronave(models.Model):
#     modelo
#     capacidade
#     status
