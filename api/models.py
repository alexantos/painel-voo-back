import uuid

from django.db import models

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

class Voo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(max_length=8)
    origem = models.ForeignKey(to=Aeroporto, on_delete=models.PROTECT, related_name='aeroporto_origem')
    destino = models.ForeignKey(to=Aeroporto, on_delete=models.PROTECT, related_name='aeroporto_destino')
    status = models.CharField(choices=[], max_length=8)

    def __str__(self):
        return self.codigo
