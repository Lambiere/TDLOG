import os
from flask import Flask, render_template, request, redirect, url_for, abort, session, flash
import pandas as pd 
import random
import collections
import copy

import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.no_of_chance = 4

file = 'capitales.csv'

cap = pd.read_csv(file, sep = ",", encoding = "ISO-8859-1")

list_cap = cap['Capitale'].__array__()
list_pays = cap['Pays'].__array__()

list_pays_str = ['' for i in range(len(list_pays))]
list_articles_pays = ['' for i in range(len(list_pays))]

k = 0

for pays in list_pays:
    i = 0
    j = 0
    while i < len(pays):
        if (pays[i] == '('):
            j = i
            i += 3
            while (pays[i] != ')'):
                i+=1
            list_pays_str [k] = pays[:j-1]
            list_articles_pays[k] = pays[j+1:i]
        i += 1
    k += 1
    print(k)

longueur_questionnaire = 10

liste_pays_avec_articles = [list_articles_pays[i] + ' ' + list_pays_str[i] for i in range(len(list_pays_str))]

dict_capitale = { list_pays_str[i] : list_cap[i] for i in range(len(list_pays))}

##Génération des questions avec les réponses

questions = {}
for i in range(len(liste_pays_avec_articles)):
    pays = liste_pays_avec_articles[i]
    options = [random.choice(list_cap) for j in range(4)]
    options[random.randint(0,3)] = list_cap[i]
    questions[str(i)] = {"question" : "Quelle est la capitale de {}".format(pays), "options" : options, "answer" : list_cap[i]}



# Ici on vérifie si le fichier qui conserve les réponses existe ou pas




#### La page d'accueil #####
@app.route('/')
def home():
    return render_template('index.html')


#### s'inscrire #####

liste = [None] * (longueur_questionnaire + 2)

@app.route('/signup', methods=['POST'])
def signup():
    session['username'] = request.form['username']
    liste[0] = request.form['username']
    #df.iloc[-1]["user"] = request.form['username']
    return redirect(url_for('bienvenue'))


#### page de bienvenue une fois l'inscription faite #####

@app.route('/bienvenue')
def bienvenue():
    if not 'username' in session:
        return abort(403)        
    return render_template('message.html', username=session['username'])
    
#### le questionnaire #####
    
@app.route('/questionnaire/', methods=['GET', 'POST'])
def questionnaire():
    print(request.method)
    print(session.get("question", "a"))

    if request.method == "POST":
        if "question" in session:
            entered_answer = request.form.get('answer', '')
            liste[int(session["question"])] = entered_answer
            print(questions.get(session["question"],False))
            if questions.get(session["question"],False):
                if entered_answer != questions[session["question"]]["answer"]:
                    mark = 0
                else:
                    mark = 4
                session["mark"] += mark
                session["question"] = str(int(session["question"])+1)
        else:
            print("question missing")
  
    if "question" not in session:
        session["question"] = "1"
        session["mark"] = 0
    elif session["question"] not in questions: #cas où il n'y a plus de question
        df = pd.read_csv(file_csv)
        df.reset_index(drop = True,inplace = True)          
        liste[longueur_questionnaire+1]  =  session["mark"]
        df.loc[-1]  = liste
        df.to_csv(file_csv, index = False)       
        return render_template("score.html", score = session["mark"])
    return render_template("quiz.html", question=questions[session["question"]]["question"], question_number=session["question"],
                            nb_questions = len(questions), options=questions[session["question"]]["options"], score = session["mark"], score_total = len(questions)*4)


@app.route('/logout')
def logout():
    # réinitialiser la session
    session.pop('username', None)
    session.clear()
    return redirect(url_for('home'))    

if __name__ == '__main__':
    app.run(debug = True)
