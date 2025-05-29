from django.db import models

class PokemonCatalogado(models.Model):
    Name = models.CharField(max_length=100, primary_key=True)
    Pokedex_Number = models.BigIntegerField(null=True)
    Types = models.TextField(null=True)
    Abilities = models.TextField(null=True)
    Generation = models.TextField(null=True)
