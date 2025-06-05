import requests
from django.shortcuts import render
from .models import PokemonCatalogado

def pesquisar_pokemon(request):
    resultado = {}
    if request.method == 'GET' and 'nome' in request.GET:
        nome_parametro = request.GET['nome'].strip().capitalize()

        try:
            pokemon = PokemonCatalogado.objects.get(name=nome_parametro)
            resultado = {
                'nome': pokemon.name,
                'elemento': pokemon.types,
                'habilidades': pokemon.abilities
            }
        except PokemonCatalogado.DoesNotExist:
            resultado = {'erro': 'Pokémon não encontrado no banco de dados.'}

    return render(request, 'dados_pokemons/telapokedex.html', {'resultado': resultado})


def catalogar_pokemon(request):
    resultado = {}

    if request.method == 'GET' and 'nome' in request.GET:
        nome_parametro = request.GET['nome'].strip().lower()

        url = f'https://pokeapi.co/api/v2/pokemon/{nome_parametro}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            nome = data['name'].capitalize()
            tipos = ', '.join([t['type']['name'].capitalize() for t in data['types']])
            habilidades = ', '.join([h['ability']['name'].capitalize() for h in data['abilities']])

            if PokemonCatalogado.objects.filter(name=nome).exists():
                resultado = {'mensagem': 'Pokémon já está catalogado.'}
            else:
                PokemonCatalogado.objects.create(
                    name=nome,
                    types=tipos,
                    abilities=habilidades
                )
                resultado = {
                    'nome': nome,
                    'elemento': tipos,
                    'habilidades': habilidades
                }
        else:
            resultado = {'erro': 'Pokémon não encontrado na API.'}

    return render(request, 'dados_pokemons/telapokedex.html', {'resultado': resultado})