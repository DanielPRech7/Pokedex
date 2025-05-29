from django.urls import path
from .views import pesquisar_pokemon, catalogar_pokemon

urlpatterns = [
    path('', pesquisar_pokemon, name='pesquisar_pokemon'),
    path('catalogar/', catalogar_pokemon, name='catalogar_pokemon'),
]
