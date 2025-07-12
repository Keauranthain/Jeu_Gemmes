import configparser
import json
import os

json_dico = {}
tous_json = ["capacite","race","type"]
with open("../ressources/capacite.json", "r", encoding="utf-8") as fichier:
    capacites_global = json.load(fichier)
for nom_json in tous_json:
    with open(f"../ressources/{nom_json}.json", "r", encoding="utf-8") as fichier:
        json_dico[f"{nom_json}"] = json.load(fichier)

paramettre = {}

def definir_paramettre(nom:str,valeur):
    paramettre[nom] = valeur

def obtenir_paramettre(nom:str):
    return paramettre[nom]

def obtenir_json(nom:str):
    return json_dico[nom]


def charger_config(path: str) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    if not os.path.exists(path):
        raise FileNotFoundError(f"Fichier config introuvable : {path}")
    config.read(path, encoding="utf-8")
    return config

fichier_config = charger_config("../ressources/config.ini")