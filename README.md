# PokedexProject
Esse projeto é um pokedex

Onde temos 2 campos:
pesquisar_pokemon: Ele vai pesquisar no banco se já tem o pokemon catalogado e tras as suas informações. Caso não tenha ele faz uma consulta na api pokeapi e tras o pokemon e salva no banco.

catalogar_pokemon: Faz um scraping em um site e salva as informações no banco de dados, isso somente se o pokemon nao estiver catalogado.

# Como rodar o projeto
Antes de mais nada, é necessário ter instalado no seu computador o Docker: https://docs.docker.com/engine/install/ e o Docker-Compose: https://docs.docker.com/compose/install/

Após instalado, é necessário rodar o comando à seguir dentro do projeto: `docker-compose up --build`