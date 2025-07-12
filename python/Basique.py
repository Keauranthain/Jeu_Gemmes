import os
from math import floor
from random import random


def obtenir_texte(langue: str, tag: str) -> str:
    dossier_langue = os.path.join("../langue", langue)

    if not os.path.isdir(dossier_langue):
        return tag

    for nom_fichier in os.listdir(dossier_langue):
        chemin = os.path.join(dossier_langue, nom_fichier)
        if not os.path.isfile(chemin):
            continue

        with open(chemin, "r", encoding="utf-8") as fichier:
            for ligne in fichier:
                ligne = ligne.strip()
                if not ligne or ":" not in ligne:
                    continue

                cle, valeur = ligne.split(":", 1)
                cle = cle.strip().strip('"')
                valeur = valeur.strip().strip('"')

                if cle == tag:
                    return valeur

    return tag

def choix_nombre(max: int,question:str,min:int=0 ) -> int:
    result = -1
    while result < min or result > max:
        try:
            result = int(input(question))
        except:
            print(f"Merci de mettre un entier entre {min} et {max}")
    return result


def aleatoire(low, high):
    return floor((high - low + 1) * random()) + low

def  T_ou_F():
    return aleatoire(0,1) == 1