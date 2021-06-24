from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

started = False
import requests
import random

player1 = []
player2 = []


def getPokemon(rarity):
    allPokemon = []
    page = 1
    response = requests.get(
        f"https://api.pokemontcg.io/v2/cards?q=supertype:Pokémon rarity:{rarity} &page={page}",
        headers={
            "X-Api-Key": "28da6591-8223-4f95-b194-f094230bc576"
        }).json()
    print(response["data"][0])
    while (response and len(response["data"]) > 0):
        allPokemon.extend(response["data"])
        page += 1
        print(page)
        response = requests.get(
            f"https://api.pokemontcg.io/v2/cards?q=supertype:Pokémon rarity:{rarity} &page={page}",
            headers={
                "X-Api-Key": "28da6591-8223-4f95-b194-f094230bc576"
            }).json()
    return allPokemon


def insertPokemon(number, rarity):
    pokemon = getPokemon(rarity)
    for i in range(number):
        player1.append(pokemon[random.randint(0, len(pokemon) - 1)])
        player2.append(pokemon[random.randint(0, len(pokemon) - 1)])
    print("Done adding " + str(number) + " pokemon of " + rarity + " rarity.")

def flipCoin():
  if(random.randint(0,1)):
    return "Heads"
  else:
    return "Tails"

def displayPokemon(pokemon):
  hp = pokemon["hp"]
  moves = []
  for move in pokemon["attacks"]:
    moves.append((move["name"],move["cost"][0]))
  return {"hp":hp,"attacks":moves}

@app.route('/', methods=['POST', 'GET'])

def index():
    global started
    if request.method == 'POST':
        ...

    elif not started:
        started  = True
        insertPokemon(4, "Common")
        return render_template('poke.html',player1 = player1)

"""
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)

"""

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = '0'
    response.headers["Pragma"] = "no-cache"
    return response


if __name__ == "__main__":
    app.run(debug=True)
