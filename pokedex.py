from flask import Flask, render_template
from flask.globals import request
from models.pokemon import Pokemon
import requests
import json

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    pokemon = Pokemon(request.form['pesquisa'],'','','','','','','','')
    try:
        json_pokemon = json.loads(requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon.pesquisa}').text)
        pokemon.numero = json_pokemon['id']
        pokemon.nome = json_pokemon['name'].capitalize()
        pokemon.foto = json_pokemon['sprites']['front_default']

        pokemon.tipo = []
        for i in range(0, len(json_pokemon['types'])):
            pokemon.tipo.append(json_pokemon['types'][i]['type']['name'].upper())

        pokemon.golpes = []
        for i in range(0, len(json_pokemon['moves'])):
            pokemon.golpes.append(json_pokemon['moves'][i]['move']['name'].capitalize())
        
        pokemon.nome_estatisticas = []
        for i in range(0, len(json_pokemon['stats'])):
            pokemon.nome_estatisticas.append(json_pokemon['stats'][i]['stat']['name'].upper())

        pokemon.estatisticas = []
        for i in range(0, len(json_pokemon['stats'])):
            pokemon.estatisticas.append(json_pokemon['stats'][i]['base_stat'])

        zipestatisticas = zip(pokemon.nome_estatisticas, pokemon.estatisticas)

        pokemon.habilidade = []
        for i in range(0, len(json_pokemon['abilities'])):
            pokemon.habilidade.append(json_pokemon['abilities'][i]['ability']['name'].capitalize())

    except:
        return "Pokemon não encontrado"
    return render_template('buscar.html',
    nome = pokemon.nome,
    foto = pokemon.foto,
    numero = pokemon.numero,
    tipo = pokemon.tipo,
    golpes = pokemon.golpes,
    zipestatisticas = zipestatisticas,
    habilidade = pokemon.habilidade,
    )
    
if __name__ == '__main__':
    app.run(debug=True)