from flask import Flask, render_template
import requests
from flask.globals import request
from models.PokemonList import Pokemon
import json
import os


app = Flask(__name__)

imgFolder = os.path.join('static','img')

app.config['UPLOAD_FOLDER'] = imgFolder

@app.route("/")
def index():
    img1 = os.path.join(app.config['UPLOAD_FOLDER'], 'fundopokemon.png')
    return render_template("index.html", user_image = img1)

@app.route("/buscar", methods = ["GET", "POST"])
def buscar():
    pokemon = Pokemon(request.form["nome"].lower(),"","","","")
    try:
        res = json.loads(requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon.nome}").text)
        result = res['sprites']
        result = result['front_default']
        pokemon.foto = result
        pokemon.golpes = []
        for i in range(0, len(res["moves"])):
            pokemon.golpes.append(res["moves"][i]["move"]["name"])

        if len(res["types"])==2:
            pokemon.tipo1 = res["types"][0]["type"]["name"]
            pokemon.tipo2 = res["types"][1]["type"]["name"]
        else:
            pokemon.tipo1 = res["types"][0]["type"]["name"]
    except:
        return "Pokemon não encontrado"    
    return render_template("index.html",
    nome = pokemon.nome,
    foto = pokemon.foto,
    tipo1 = pokemon.tipo1.upper(),
    tipo2 = pokemon.tipo2.upper(),
    golpes = pokemon.golpes
    )



if __name__ == "__main__":
    app.run(debug=True)