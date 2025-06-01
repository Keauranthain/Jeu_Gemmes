from python.Basique import choix_nombre,aleatoire
from python import Personnage as perso


class Acteur():
    def __init__(self,personnage:perso.Personnage=None):
        self.personnage:perso.Personnage = personnage
        self.posture:str = "neutre"
        self.variation_posture:float = 1.25

    def __str__(self):
        return f"{self.personnage.nom}"

    def changement_posture(self):
        postures = ["neutre","offensive","defensive"]
        for posture in postures:
            if posture == self.posture:
                postures.remove(self.posture)
        if self.personnage.joueur:
            print("Changement de posture")
            for k in range (2):
                print(f"{k}: {postures[k]}")
            choix = choix_nombre(max = 1, question="Nouvelle posture : ")
        else:
            choix = aleatoire(0,1)
        self.posture = postures[choix]

    def def_phy(self):
        coef = 1
        if self.posture == "offensive":
            coef = coef/self.variation_posture
        elif self.posture == "defensive":
            coef = coef*self.variation_posture
        return self.personnage.resistance*coef

    def def_mag(self):
        coef = 1
        if self.posture == "offensive":
            coef = coef / self.variation_posture
        elif self.posture == "defensive":
            coef = coef * self.variation_posture
        return self.personnage.resistance_magique * coef

    def atk_phy(self):
        coef = 1
        if self.posture == "offensive":
            coef = coef * self.variation_posture
        elif self.posture == "defensive":
            coef = coef / self.variation_posture
        return self.personnage.force * coef

    def atk_mag(self):
        coef = 1
        if self.posture == "offensive":
            coef = coef * self.variation_posture
        elif self.posture == "defensive":
            coef = coef / self.variation_posture
        return self.personnage.magie * coef