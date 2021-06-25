from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
app = Flask(__name__)

started = False
import requests
import random

player1 = []
player2 = []
player1ActiveIndex = -1
player2ActiveIndex = -1
turn = 1
def findEffectiveness(attacker, defender):
    with open("dict2.json") as f:
        file = json.load(f)
    return file[attacker][defender]


def getPokemon(rarity):
    allPokemon = []
    page = 1
    response = requests.get(
        f"https://api.pokemontcg.io/v2/cards?q=supertype:Pokémon rarity:{rarity} &page={page}",
        headers={
            "X-Api-Key": "28da6591-8223-4f95-b194-f094230bc576"
        }).json()
    print(response["data"][0])
    count = 0 #take count out in final game
    while (response and len(response["data"]) > 0 and count < 2):
        allPokemon.extend(response["data"])
        page += 1
        count+=1
        print(page)
        response = requests.get(
            f"https://api.pokemontcg.io/v2/cards?q=supertype:Pokémon rarity:{rarity} &page={page}",
            headers={
                "X-Api-Key": "28da6591-8223-4f95-b194-f094230bc576"
            }).json()
    return allPokemon

def checkEmpty(list1):
    flag = True
    for item in list1:
        if item:
            flag = False
    return flag

def insertPokemon(number, rarity):
    pokemon = getPokemon(rarity)
    for i in range(number):
        player1.append(pokemon[random.randint(0, len(pokemon) - 1)])
        player2.append(pokemon[random.randint(0, len(pokemon) - 1)])
    print("Done adding " + str(number) + " pokemon of " + rarity + " rarity.")

def flipCoin():
  if(random.randint(0,1)):
    return 1
  else:
    return 2

def dead(pokemon):
    if pokemon["hp"]<=0:
        pokemon["images"]["small"] = "https://i.ibb.co/4s12zWc/dead.png"
        pokemon.update({"dead":True})


def displayPokemon(pokemon):
  hp = pokemon["hp"]
  moves = []
  for move in pokemon["attacks"]:
    moves.append((move["name"],move["cost"][0]))
  return {"hp":hp,"attacks":moves}

@app.route('/', methods=['POST', 'GET'])

def index():
    global started
    global turn
    global player1ActiveIndex
    global player2ActiveIndex
    global player1
    global player2
    if request.method == 'POST':
        ...

    elif not started:
        player1 = []
        player2 = []
        player1ActiveIndex = -1
        player2ActiveIndex = -1
        turn = flipCoin()
        insertPokemon(4, "Rare")
        print(player1[0])
        return render_template('poke.html',player1 = player1, player2=player2,player1ActiveIndex= int(player1ActiveIndex)
        , player2ActiveIndex = int(player2ActiveIndex), message = f"Flipped coin, Player {turn} goes first.", status = None)

@app.route('/decision', methods=['POST', 'GET'])
def decision():
    global started
    global turn
    global player1ActiveIndex
    global player2ActiveIndex
    global player1
    global player2
    if request.method == 'POST':
        a = request.form['submit_button']
        #print(a)
        if(a == "Switch"):

            return render_template('poke.html',player1 = player1, player2=player2,player1ActiveIndex= player1ActiveIndex
        , player2ActiveIndex = player2ActiveIndex, message=f"Player {turn} turn now.\n Click a Pokemon to make Active",status = "switching" )
        if(a == "Attack"):
            return render_template('poke.html',player1 = player1, player2=player2,player1ActiveIndex= player1ActiveIndex
        , player2ActiveIndex = player2ActiveIndex, message=f"Player {turn} turn now.\n Enter how much damage you did",status = "attacking" )
    return render_template('poke.html',player1 = player1, player2=player2,player1ActiveIndex= player1ActiveIndex
        , player2ActiveIndex = player2ActiveIndex, message="Made decision",status = "None" )
@app.route('/enterDamage', methods=['POST', 'GET'])
def enterDamage():
    global started
    global turn
    global player1ActiveIndex
    global player2ActiveIndex
    global player1
    global player2
    
    if request.method == 'POST':
        a = request.form['submit_button']
        a = int(a)
        if turn == 1:
            damage = a* findEffectiveness(player1[player1ActiveIndex]["types"][0].lower(),player2[player2ActiveIndex]["types"][0].lower())
            player2[player2ActiveIndex]["hp"] = int(player2[player2ActiveIndex]["hp"]) - damage
            turn = 2
            message = f"Player {turn} hit with {damage} damage.<br> Player {turn} turn now."
            dead(player2[player2ActiveIndex])
        elif turn == 2:
            damage = a* findEffectiveness(player2[player2ActiveIndex]["types"][0].lower(),player1[player1ActiveIndex]["types"][0].lower())
            player1[player1ActiveIndex]["hp"] = int(player1[player1ActiveIndex]["hp"]) - damage
            turn = 1
            message = f"Player {turn} hit with {damage} damage.<br> Player {turn} turn now."
            dead(player1[player1ActiveIndex])
        if(checkEmpty(player1)):
            message = f"Player 1 hit with {damage} damage.\n Player 1 loses"
        if(checkEmpty(player2)):
            message = f"Player 2 hit with {damage} damage.\n Player 2 loses"
        return render_template('poke.html',player1 = player1, player2=player2,player1ActiveIndex= player1ActiveIndex
        , player2ActiveIndex = player2ActiveIndex, message=message,status = "None" )
@app.route('/pickActive/<index>', methods=['POST', 'GET'])
def pickActive(index):
    index = int(index)
    global started
    global turn
    global player1ActiveIndex
    global player2ActiveIndex
    global player1
    global player2
    for i in range(len(player1)):
        if player1[i]:
            if int(player1[i]["hp"]) < 0:
                player1[i] = None
    for i in range(len(player2)):
        if player2[i]:
            if int(player2[i]["hp"]) < 0:
                player2[i] = None

    if turn == 1:
        player1ActiveIndex = index
        #player1[int(index)] = None
        turn = 2
        return render_template('poke.html',player1 = player1, player2=player2,player1ActiveIndex= player1ActiveIndex
        , player2ActiveIndex = player2ActiveIndex, message=f"Changed active pokemon \n Player {turn} turn now.", status = "picked" )
    if turn == 2:
        player2ActiveIndex = index
        #player2[int(index)] = None
        turn = 1
        return render_template('poke.html',player1 = player1, player2=player2,player1ActiveIndex= player1ActiveIndex\
        , player2ActiveIndex = player2ActiveIndex, message=f"Changed active pokemon \n Player {turn} turn now.", status = "picked"  )



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
