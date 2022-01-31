import pymongo
from pymongo import MongoClient
from flask import Flask, make_response, render_template, request
import matplotlib.pyplot as plt
import pandas as pd
import json
import plotly
import plotly.express as px
import math
import os 
import sys

if os.path.exists('data.json')==True:
    os.remove("data.json")
    os.system('scrapy crawl autoy -o data.json')
    # os.system('python3 app.py')
else:
    os.system('scrapy crawl autoy -o data.json')
    # os.system('python3 app.py')


#On  lit et crée une data frame
lire = pd.read_json("data.json") 
lire = pd.DataFrame(lire)
lire.rename(columns={'Kilométrage': 'Kilométrage (en km)', 
                    'Puissance fiscale': 'Puissance fiscale (en Ch)',
                     'Garantie':'Garantie (en mois)',
                     'Emission de CO2':'Emission de CO2 (en g/km)',
                    'Prix': 'Prix (en €)'}, inplace=True)

lire = lire.dropna(axis=0)

#On cree une colonne marque_id

marque_id_dic = dict()
for i in range(len(lire['Marque'].unique())):
    marque_id_dic.update({str(i) : lire['Marque'].unique()[i] })

marque_id = []
for val in lire['Marque'] :
    for key, value in marque_id_dic.items(): 
        if val == value :
            marque_id.append(int(key))

lire.insert(2,"marque_id",marque_id,True)


#On creé la colonne model_id

Modele_id_dic = dict()
for i in range(len(lire['Modèle'].unique())):
    Modele_id_dic.update({str(i) : lire['Modèle'].unique()[i] })

Modèle_id = []
for val in lire['Modèle'] :
    for key, value in Modele_id_dic.items(): 
        if val == value :
            Modèle_id.append(int(key))

lire.insert(4,"Modèle_id",Modèle_id,True)

#On cree energie_id

Énergie_id_dic = dict()
for i in range(len(lire['Énergie'].unique())):
    Énergie_id_dic.update({str(i) : lire['Énergie'].unique()[i] })

Énergie_id = []
for val in lire['Énergie'] :
    for key, value in Énergie_id_dic.items(): 
        if val == value :
            Énergie_id.append(int(key))

lire.insert(8,"Énergie_id",Énergie_id,True)

#On cree Boite de vitesse_id

Boite_de_vitesse_id_dic = dict()
for i in range(len(lire['Boite de vitesse'].unique())):
    Boite_de_vitesse_id_dic.update({str(i) : lire['Boite de vitesse'].unique()[i] })
Boite_de_vitesse_id = []
for val in lire['Boite de vitesse'] :
    for key, value in Boite_de_vitesse_id_dic.items(): 
        if val == value :
            Boite_de_vitesse_id.append(int(key))
lire.insert(10,"Boite_de_vitesse_id",Boite_de_vitesse_id,True)

#mise en circulation_année

lire = lire[lire["Mise en circulation"]!='N.C']

Mise_en_circulation_année = []
for val in lire['Mise en circulation'] :
    liste_val = val.split('/')
    Mise_en_circulation_année.append(liste_val[2])

lire.insert(6,"Mise_en_circulation_année",Mise_en_circulation_année,True)
lire['Mise_en_circulation_année'] = lire['Mise_en_circulation_année'].astype(int)

#MONGO

client = MongoClient("mongo")

# Base de données
db = client['auto']

#Création de la collection
col= db['info_car']#tables

f = lire.to_dict("records")
col.drop()

col= db['info_car']

col.insert_many(f)

cursor3 = col.find({"$and":[{"Prix (en €)":{"$lte": 60000}}, {"Kilométrage (en km)":{"$lte": 50000 }},{"Marque": "AIXAM"}]})
cursor3 = list(cursor3)
valeur=[]
for dic in cursor3:
    element = []
    for cle,val in dic.items():
         element.append(val)
    valeur.append(element)


cursor2 = col.find({})
cursor2 = list(cursor2)
valeur=[]
for dic in cursor2:
    element = []
    for cle,val in dic.items():
        element.append(val)
    valeur.append(element)


#Flask




#On commence par crée une instance de Flask
app = Flask(__name__)

client = MongoClient(host="localhost", port=27017)



#1er page de notre Web APP
@app.route('/',methods=['GET','POST'])

def home():
    cursor2 = col.find({})
    cursor2 = list(cursor2)
    valeur=[]
    for dic in cursor2:
        element = []
        for cle,val in dic.items():
            element.append(val)
        valeur.append(element)
#############################################################  marque    #########################################
    marque_cur = col.find({},{'Marque':1,'_id':0}).sort([("Marque", 1)])
    marque_cur = list(marque_cur)
    marque_tout = []
    marque=[]
    for dic in marque_cur:
        for marq in dic.values():
            marque_tout.append(marq)
    for mar in marque_tout:
        if mar in marque:
            next
        else:
            marque.append(mar)
############################################################ Kilometrage ###########################################

    kilometrage = [10000,50000,100000,150000,200000,300000]

############################################################ Prix en euro ###########################################
    prix = list(col.find({},{'Prix (en €)':1,'_id':0}).sort([("Prix (en €)", -1)]).limit(1))
    max_prix = list(prix[0].values())[0]
    prix_list = []
    for k in range(max_prix,0,-10000):
        multiplier = 10 ** (-4)
        val = math.ceil(k * multiplier) / multiplier
        prix_list.append(int(val))
    
    return render_template('index.html', liste=valeur,marque=marque, kilometrage= kilometrage, prix=prix_list)


@app.route('/recherche/<marque>/<kilometrage>/<prix>')

def recherche(marque,kilometrage,prix):
    cursor3 = col.find({"$and":[{"Prix (en €)":{"$lte": int(float(prix)) }}, {"Kilométrage (en km)":{"$lte": int(float(kilometrage)) }},{"Marque": marque}]})
    cursor3 = list(cursor3)
    valeur=[]
    for dic in cursor3:
        element = []
        for cle,val in dic.items():
            element.append(val)
        valeur.append(element)
    return render_template('index.html', liste=valeur) 


@app.route('/graph')

def courbe():
    cur = col.aggregate([{"$group" : {"_id" : "$Énergie", "Nombre" : {"$sum" : 1}}}])
    cur = list(cur)
    label = []
    valeur = []
    for dic in list(cur):
        label.append(dic["_id"])
        valeur.append(dic["Nombre"])
    cur = col.aggregate([{"$group" : {"_id" : "$Boite de vitesse", "Nombre" : {"$sum" : 1}}}])
    cur = list(cur)
    label2 = []
    valeur2 = []
    for dic in list(cur):
        label2.append(dic["_id"])
        valeur2.append(dic["Nombre"])
    cur = col.aggregate([{"$group" : {"_id" : "$Marque", "Nombre" : {"$sum" : 1}}}])
    cur = list(cur)
    label3 = []
    valeur3 = []
    for dic in list(cur):
        label3.append(dic["_id"])
        valeur3.append(dic["Nombre"])

        
    return render_template("graph.html", label=label, valeur=valeur,label2=label2,valeur2=valeur2,label3=label3,valeur3=valeur3)

@app.route('/prix')

def courbe_prix():
###############################   Prix moyenne en fonction des marques #####################################    
    cur = col.aggregate([{"$group" : {"_id" : "$Marque", "Moyenne" : {"$avg" : "$Prix (en €)"}}}])
    cur = list(cur)
    label4 = []
    valeur4 = []
    for dic in list(cur):
        label4.append(dic["_id"])
        valeur4.append(dic["Moyenne"])
###############################   Prix moyenne en fonction du Puissance fiscale #####################################  
    cur = col.aggregate([{"$group" : {"_id" : "$Puissance fiscale (en Ch)", "Moyenne" : {"$avg" : "$Prix (en €)"}}},{ "$sort": { "_id": 1 } }])
    label5 = []
    valeur5 = []
    for dic in list(cur):
        label5.append(dic["_id"])
        valeur5.append(dic["Moyenne"])
###############################   Prix moyenne en fonction de l'énergie #####################################  
    cur = col.aggregate([{"$group" : {"_id" : "$Énergie", "Moyenne" : {"$avg" : "$Prix (en €)"}}}])
    label6 = []
    valeur6 = []
    for dic in list(cur):
        label6.append(dic["_id"])
        valeur6.append(dic["Moyenne"])
###############################   Prix moyenne en fonction de la boite de vitesse #####################################    
    cur = col.aggregate([{"$group" : {"_id" : "$Boite de vitesse", "Moyenne" : {"$avg" : "$Prix (en €)"}}}])
    cur = list(cur)
    label7 = []
    valeur7 = []
    for dic in list(cur):
        label7.append(dic["_id"])
        valeur7.append(dic["Moyenne"])
###############################   Prix moyenne en fonction de l'annee de la mise a circulation #############################
    cur = col.aggregate([{"$match":{"Mise_en_circulation_année":{"$gte":1908}}},{"$group" : {"_id" : "$Mise_en_circulation_année", "Moyenne" : {"$avg" : "$Prix (en €)"}}},{ "$sort": { "_id": 1 } }])
    cur = list(cur)
    label8 = []
    valeur8 = []
    for dic in list(cur):
        label8.append(dic["_id"])
        valeur8.append(dic["Moyenne"])
###########################################################

    cur = col.aggregate([{"$group" : {"_id" : {"kilometrage":"$Kilométrage (en km)","marque":"$Marque"}, "Moyenne" : {"$avg" : "$Prix (en €)"}}},{ "$sort": { "_id": 1 } }])
    kilometrage = []
    marque = []
    dic_id = []
    prix = []
    for dic in list(cur):
        dic_id.append(dic["_id"])
        prix.append(dic["Moyenne"])
    for val in dic_id:
        kilometrage.append(val["kilometrage"])
        marque.append(val["marque"])


    df = pd.DataFrame({'kilometrage': kilometrage, 'marque': marque, 'prix_moyenne': prix})
    fig = px.scatter(df, x="kilometrage", y="prix_moyenne", color="marque", symbol="marque")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template("prix3.html", label4=label4, valeur4=valeur4, label5=label5, valeur5=valeur5, label6=label6, valeur6=valeur6 , label7=label7 , valeur7=valeur7,label8=label8, valeur8=valeur8,graphJSON=graphJSON)

@app.route('/pollution')
def courbe_polution():
###############################   Polution moyenne en fonction des marques #####################################    
    cur = col.aggregate([{"$group" : {"_id" : "$Marque", "Moyenne" : {"$avg" : "$Emission de CO2 (en g/km)"}}}])
    cur = list(cur)
    label4 = []
    valeur4 = []
    for dic in list(cur):
        label4.append(dic["_id"])
        valeur4.append(dic["Moyenne"])
###############################   Polution moyenne en fonction du Puissance fiscale #####################################  
    cur = col.aggregate([{"$group" : {"_id" : "$Puissance fiscale (en Ch)", "Moyenne" : {"$avg" : "$Emission de CO2 (en g/km)"}}},{ "$sort": { "_id": 1 } }])
    label5 = []
    valeur5 = []
    for dic in list(cur):
        label5.append(dic["_id"])
        valeur5.append(dic["Moyenne"])
###############################   Polution moyenne en fonction de l'énergie #####################################  
    cur = col.aggregate([{"$group" : {"_id" : "$Énergie", "Moyenne" : {"$avg" : "$Emission de CO2 (en g/km)"}}}])
    label6 = []
    valeur6 = []
    for dic in list(cur):
        label6.append(dic["_id"])
        valeur6.append(dic["Moyenne"])
###############################   Polution moyenne en fonction de la boite de vitesse #####################################    
    cur = col.aggregate([{"$group" : {"_id" : "$Boite de vitesse", "Moyenne" : {"$avg" : "$Emission de CO2 (en g/km)"}}}])
    cur = list(cur)
    label7 = []
    valeur7 = []
    for dic in list(cur):
        label7.append(dic["_id"])
        valeur7.append(dic["Moyenne"])
###############################   Polution moyenne en fonction de l'annee de la mise a circulation #############################
    cur = col.aggregate([{"$match":{"Mise_en_circulation_année":{"$gte":1908}}},{"$group" : {"_id" : "$Mise_en_circulation_année", "Moyenne" : {"$avg" : "$Emission de CO2 (en g/km)"}}},{ "$sort": { "_id": 1 } }])
    cur = list(cur)
    label8 = []
    valeur8 = []
    for dic in list(cur):
        label8.append(dic["_id"])
        valeur8.append(dic["Moyenne"])

    return render_template("pollution2.html", label4=label4, valeur4=valeur4, label5=label5, valeur5=valeur5, label6=label6, valeur6=valeur6 , label7=label7 , valeur7=valeur7,label8=label8, valeur8=valeur8)

