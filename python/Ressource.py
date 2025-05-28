import json

with open("./ressources/capacite.json", "r", encoding="utf-8") as fichier:
    capacites_global = json.load(fichier)
with open("./ressources/race.json", "r", encoding="utf-8") as fichier:
    races_global = json.load(fichier)