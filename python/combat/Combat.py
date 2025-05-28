from python import Capacite as capa
import random as rnd
from python.combat.Acteur import Acteur

from python.Basique import aleatoire, choix_nombre


class Action():
    def __init__(self,auteur:Acteur=None,cible:Acteur=None,capacite:capa.Capacite_class=None,temps:int=0,posture:bool=False,position:bool=False):
        self.auteur = auteur
        self.cible = cible
        self.capacite = capacite
        self.temps:int = temps
        self.posture = posture
        self.position = position

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

    def str_vie(self,personnage:Acteur):
        perso = personnage.personnage
        return f"{perso.nom},{personnage.posture} ({perso.vie} / {perso.vie_total})"

    def creation_print_liste(self,camps:list,nom_le_plus_long:int=0):
        result = []
        for personnage in camps:
            perso = self.str_vie(personnage)
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
            self.printer(f" et inflige {deg} à {defenseur.personnage.nom}")
        defenseur.personnage.vie = max(0, round(defenseur.personnage.vie - deg, 2))

    def debut(self):
        camp_1 = self.camp_1
        camp_2 = self.camp_2
        camp_1_mort = self.camp_1_mort
        camp_2_mort = self.camp_2_mort
        liste_actions = []
        self.ecran_combat()
        for personnage in camp_1+camp_2:
            nouvelle_action = self.choix_action(personnage)
            liste_actions.append(nouvelle_action)


        while(len(camp_1)>0 and len(camp_2)>0):
            #Trouve le premier à attaquer
            action_plus_rapide = liste_actions[0]
            for action in liste_actions:
                if action.temps < action_plus_rapide.temps:
                    action_plus_rapide = action
            liste_actions.remove(action_plus_rapide)

            #Avance dans le temps
            self.temps_combat = self.temps_combat + action_plus_rapide.temps
            for action in liste_actions:
                action.avance_temps(action_plus_rapide.temps)

            #Attaque
            self.ecran_combat()
            if action_plus_rapide.capacite != None:
                self.attaque(action_plus_rapide)

            #Traite la mort s'il y a
            cible = action_plus_rapide.cible
            if cible.personnage.vie <= 0:
                if cible in camp_1:
                    camp_1.remove(cible)
                    camp_1_mort.append(cible)
                elif cible in camp_2:
                    camp_2.remove(cible)
                    camp_2_mort.append(cible)
                self.printer(f"{cible.personnage.nom} est tombé{'e' if cible.personnage.genre == 'female' else ''} !")

            #Nouvelle action
            if len(camp_1)>0 and len(camp_2)>0:
                personnage = action_plus_rapide.auteur
                nouvelle_action = self.choix_action(personnage)
                liste_actions.append(nouvelle_action)

        if(len(camp_1)>0):
            self.printer("Le camps 1 l'emporte !")
            self.victoire = self.camp_1

        else:
            self.printer("Le camps 2 l'emporte !")
            self.victoire = self.camp_2

    def choix_action(self, acteur: Acteur):
        choix = 0
        if acteur.personnage.joueur:
            self.printer("\n0 : Attaque\n1 : Changement de posture")
            choix = choix_nombre(max = 1,question="Que voulez vous faire :")
            self.printer("\n")

        if choix == 0:
            nouvelle_action= self.choix_attaque(acteur)

        elif choix == 1:
            nouvelle_action = self.choix_posture(acteur)

        return nouvelle_action



    def choix_attaque(self, acteur: Acteur):
        nouvelle_capacite = acteur.personnage.capaciter_selecteur(acteur.personnage.magie,acteur.personnage.endurance)
        temps = nouvelle_capacite.temps
        if nouvelle_capacite.cible_sois:
            cible = acteur
        elif acteur in self.camp_1:
            cible = self.camp_2[aleatoire(0, len(self.camp_2)) - 1]
        else:
            cible = self.camp_1[aleatoire(0, len(self.camp_1)) - 1]
        nouvelle_action = Action(auteur=acteur, cible=cible, temps=temps, capacite=nouvelle_capacite)
        return nouvelle_action


    def choix_posture(self, acteur: Acteur):
        temps = 5
        acteur.changement_posture()
        nouvelle_action = Action(auteur=acteur,cible=acteur, temps=temps)
        return nouvelle_action