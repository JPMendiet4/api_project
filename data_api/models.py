from django.db import models

class Character(models.Model):
    name = models.CharField(max_length=255)
    species = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    # Agrega otros campos según la estructura de los datos que vas a consumir

    def __str__(self):
        return self.name
