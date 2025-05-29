import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
import re
from .models import PokemonCatalogado

def pesquisar_pokemon(request):
    resultado = {}
    if request.method == 'GET' and 'nome' in request.GET:
        nome_parametro = request.GET['nome'].strip()
        nome_lower = nome_parametro.lower()

        # Consulta no banco
        try:
            pokemon = PokemonCatalogado.objects.get(Name=nome_parametro)
            resultado = {
                'nome': pokemon.Name,
                'elemento': pokemon.Types,
                'habilidades': pokemon.Abilities
            }
        except PokemonCatalogado.DoesNotExist:

            # Consulta na API
            url = f'https://pokeapi.co/api/v2/pokemon/{nome_lower}'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                tipos = ', '.join([t['type']['name'].capitalize() for t in data['types']])
                habilidades = ', '.join([h['ability']['name'].capitalize() for h in data['abilities']])
                resultado = {
                    'nome': data['name'].capitalize(),
                    'elemento': tipos,
                    'habilidades': habilidades}

                # Salvar no banco após buscar na API
                PokemonCatalogado.objects.create(
                    Name=data['name'].capitalize(),
                    Types=tipos,
                    Abilities=habilidades
                )
            else:
                resultado = {'erro': 'Pokemon não encontrado na API nem no banco :('}
    return render(request, 'dados_pokemons/telapokedex.html', {'resultado': resultado})

def catalogar_pokemon(request):
    resultado = {}

    if request.method == 'GET' and 'nome' in request.GET:
        nome_parametro = request.GET['nome']
        nome = nome_parametro.capitalize()
        url = f"https://wiki.pokexgames.com/index.php/{nome}"

        response = requests.get(url)

        if response.status_code != 200:
            resultado = {'erro': 'Pokemon não encontrado no site.'}
            return render(request, 'dados_pokemons/telapokedex.html', {'resultado': resultado})

        try:
            # Verifica se já está catalogado
            if PokemonCatalogado.objects.filter(Name=nome).exists():
                resultado = {'mensagem': 'Pokemon já catalogado.'}
                return render(request, 'dados_pokemons/telapokedex.html', {'resultado': resultado})

            # Faz o scraping
            soup = BeautifulSoup(response.content, "html.parser")
            info_title = soup.find("span", id="Informações_Gerais")

            if info_title:
                container = info_title.find_parent("h2").find_next_sibling()
                if container:
                    raw_html = container.get_text(separator="\n", strip=True)
                    padrao = r"([A-Za-zÀ-ÿ\s]+):\s*([^:\n]+)"
                    matches = re.findall(padrao, raw_html)

                    campos_desejados = ['nome', 'elemento', 'habilidades']
                    dados_extraidos = {}

                    for chave, valor in matches:
                        chave_limpa = chave.strip().lower()
                        if chave_limpa in campos_desejados:
                            dados_extraidos[chave_limpa] = valor.strip()

                    dados_extraidos['nome'] = nome_parametro.capitalize()

                    # Salva no banco
                    PokemonCatalogado.objects.create(
                        Name=dados_extraidos.get('nome', ''),
                        Types=dados_extraidos.get('elemento', ''),
                        Abilities=dados_extraidos.get('habilidades', '')
                    )

                    resultado = {
                        'nome': dados_extraidos.get('nome', ''),
                        'elemento': dados_extraidos.get('elemento', ''),
                        'habilidades': dados_extraidos.get('habilidades', '')
                    }
                else:
                    resultado = {'erro': 'dados não encontrados.'}
            else:
                resultado = {'erro': 'Informações não encontradas.'}

        except Exception as e:
            resultado = {'erro': f'Erro ao processar os dados: {str(e)}'}

    return render(request, 'dados_pokemons/telapokedex.html', {'resultado': resultado})