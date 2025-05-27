from time import sleep

import Personnage as perso
import Capacite as capa
import random as rnd
from Acteur import Acteur

from Basique import aleatoire, choix_nombre


class Action():
    def __init__(self,auteur:Acteur=None,cible:Acteur=None,capacite:capa.Capacite_class=None,temps:int=0):
        self.auteur = auteur
        self.cible = cible
        self.capacite = capacite
        self.temps:int = temps

    def __str__(self):
        return f"auteur : {self.auteur}, cible : {self.cible}, capacite : ({self.capacite}), temps : {self.temps}"

    def avance_temps(self,avance:int):
        self.temps = self.temps-avance


class Combat():
    def __init__(self,camps_1:list,camps_2:list,affiche:bool=True):
        self.camp_1 = []
        for personnage in camps_1:
            self.camp_1.append(Acteur(personnage))
        self.camp_2 = []
        for personnage in camps_2:
            self.camp_2.append(Acteur(personnage))
        self.camp_1_mort = []
        self.camp_2_mort = []
        self.temps_combat = 0
        self.affiche = affiche
        self.victoire = []

    def printer(self, txt, end="\n"):
        if self.affiche:
            print(txt, end=end)

    def str_vie(self,personnage:perso.Personnage):
        return f"{personnage.nom} ({personnage.vie} / {personnage.vie_total})"

    def creation_print_liste(self,camps:list,nom_le_plus_long:int=0):
        result = []
        for personnage in camps:
            perso = self.str_vie(personnage.personnage)
            result.append(perso)
            if len(perso)>nom_le_plus_long:
                nom_le_plus_long = len(perso)
        return result, nom_le_plus_long

    def ecran_combat(self):
        n = 20

        camp_1_str,nom_le_plus_long =self.creation_print_liste(self.camp_1)
        camp_2_str, nom_le_plus_long = self.creation_print_liste(self.camp_2, nom_le_plus_long)
        premier_string = (f"{camp_1_str[0]}"
                    f" {n*' '}{(nom_le_plus_long-len(camp_1_str[0]))*' '} VS {(nom_le_plus_long-len(camp_2_str[0]))*' '}{n*' '} "
                    f"{camp_2_str[0]}")
        self.printer(f"\n\n{len(premier_string)*'#'}\n")
        self.printer(premier_string)

        for k in range(1,max(len(camp_1_str), len(camp_2_str))):
            if len(camp_1_str) > k:
                self.printer(f"{camp_1_str[k]}{(nom_le_plus_long-len(camp_1_str[k]))*' '}",end="")
            else:
                self.printer(f"{' '*nom_le_plus_long}",end="")
            self.printer(f"{(2*n+6) * ' '}",end="")
            if len(camp_2_str) > k:
                self.printer(f"{(nom_le_plus_long-len(camp_2_str[k]))*' '}{camp_2_str[k]}")
            else:
                self.printer(f"{' '*nom_le_plus_long}")
        self.printer(f"\n     {(len(premier_string)-10)*"-"}     \n")

    def temps(self,capacite,auteur):
        if capacite.magie > 0:
            t = (capacite.temps**2)/auteur.incantation
        else:
            t = (capacite.temps**2)/auteur.agilite
        return t

    def degat(self,capacite,cible:Acteur,auteur:Acteur):
        if capacite.magie > 0:
            d = (capacite.magie*auteur.atk_mag()**1.5)/(cible.def_mag()**1.5)  * round(rnd.uniform(0.9, 1.1), 2)
        else:
            d = (capacite.force*auteur.atk_phy()**1.5)/(cible.def_phy()**1.5)  * round(rnd.uniform(0.9, 1.1), 2)
        return round(d,2)

    def attaque(self,action:Action):
        attaquant,defenseur,capacite=action.auteur,action.cible,action.capacite
        deg = self.degat(capacite, defenseur, attaquant)
        attaquant.personnage.mana = min(attaquant.personnage.mana - capacite.mana, attaquant.personnage.mana_total)
        attaquant.personnage.endurance = min(attaquant.personnage.endurance - capacite.endurance, attaquant.personnage.endurance_total)
        self.printer(f"{attaquant.personnage.nom} utilise {capacite.nom}", end="")
        if capacite.cible_sois:
            self.printer(f" et recupère {-capacite.mana} de mana et {-capacite.endurance} d'endurance")
        else:
            self.printer(f" et inflige {deg}")
        defenseur.personnage.vie = max(0, round(defenseur.personnage.vie - deg, 2))

    def debut(self):
        camp_1 = self.camp_1
        camp_2 = self.camp_2
        camp_1_mort = self.camp_1_mort
        camp_2_mort = self.camp_2_mort
        liste_actions = []
        self.ecran_combat()
        for personnage in camp_1+camp_2:
            perso = personnage.personnage
            capacite = perso.capaciter_selecteur(perso.magie,perso.endurance)
            if capacite.cible_sois:
                cible = personnage
            elif perso in camp_1:
                cible = camp_2[aleatoire(0,len(camp_2)-1)]
            else:
                cible = camp_1[aleatoire(0,len(camp_1)-1)]

            liste_actions.append(Action(auteur=personnage,cible=cible,temps=capacite.temps,capacite=capacite))

        self.ecran_combat()


        while(len(camp_1)>0 and len(camp_2)>0):
            action_plus_rapide = liste_actions[0]
            for action in liste_actions:
                if action.temps < action_plus_rapide.temps:
                    action_plus_rapide = action
            liste_actions.remove(action_plus_rapide)

            self.temps_combat = self.temps_combat + action_plus_rapide.temps

            for action in liste_actions:
                action.avance_temps(action_plus_rapide.temps)

            personnage = action_plus_rapide.auteur
            cible = action_plus_rapide.cible


            self.attaque(action_plus_rapide)

            if cible.personnage.vie <= 0:
                if cible in camp_1:
                    camp_1.remove(cible)
                    camp_1_mort.append(cible)
                elif cible in camp_2:
                    camp_2.remove(cible)
                    camp_2_mort.append(cible)
                self.printer(f"{cible.personnage.nom} est tombé{'e' if cible.personnage.genre == 'female' else ''} !")

            if len(camp_1)>0 and len(camp_2)>0:
                self.ecran_combat()
                nouvelle_capacite = personnage.personnage.capaciter_selecteur(personnage.personnage.magie,personnage.personnage.endurance)
                temps = nouvelle_capacite.temps

                if nouvelle_capacite.cible_sois:
                    cible = personnage
                elif personnage in camp_1:
                    cible = camp_2[aleatoire(0,len(camp_2))-1]
                else:
                    cible = camp_1[aleatoire(0,len(camp_1))-1]
                nouvelle_action = Action(auteur=personnage, cible=cible, temps=temps, capacite=nouvelle_capacite)
                liste_actions.append(nouvelle_action)
        if(len(camp_1)>0):
            self.printer("Le camps 1 l'emporte !")
            self.victoire = self.camp_1

        else:
            self.printer("Le camps 2 l'emporte !")
            self.victoire = self.camp_2