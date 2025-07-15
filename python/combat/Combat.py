from python import Capacite as capa
import random as rnd

from python.Capacite import Capacite_class
from python.Ressource import definir_paramettre, obtenir_paramettre
from python.combat.Acteur import Acteur

from python.Basique import aleatoire, choix_nombre
from python.combat.Equipe import Equipe


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
    def __init__(self,camps_1:Equipe,camps_2:Equipe,affiche:bool=True):
        self.equipe_1:Equipe = camps_1
        self.equipe_2:Equipe = camps_2
        self.camp_1 = camps_1.liste_combat()
        self.camp_2 = camps_2.liste_combat()
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
        return f"{perso.nom} ({perso.vie} / {perso.get_vie_tt()})"

    def str_titre(self,personnage:Acteur):
        equipe = self.trouve_equipe(personnage)
        role = ""
        if equipe.est_chef(personnage):
            role = "Chef, "
        elif equipe.est_second(personnage):
            role = "Second, "
        perso = personnage.personnage
        return f"{role}{personnage.posture}"

    def creation_print_liste(self,camps:list,nom_le_plus_long:int=0,liste_la_plus_long:int=0):
        result = []
        n = 0
        for personnage in camps:
            perso = self.str_vie(personnage)
            result.append(perso)
            n += 1
            if len(perso)>nom_le_plus_long:
                nom_le_plus_long = len(perso)
        if n > liste_la_plus_long:
            liste_la_plus_long = n
        return result, nom_le_plus_long,liste_la_plus_long

    def creation_print_liste_titre(self,camps:list,nom_le_plus_long:int=0):
        result = []
        for personnage in camps:
            perso = self.str_titre(personnage)
            result.append(perso)
            if len(perso)>nom_le_plus_long:
                nom_le_plus_long = len(perso)
        return result, nom_le_plus_long

    def clean_des_liste_str(self,liste:list,taille_str:int,nombre_str:int):
        for k in range(0,nombre_str):
            if k<len(liste):
                liste[k] = self.centre_str(liste[k],taille_str)
            else:
                liste.append(" "*taille_str)

    def centre_str(self,string:str,taille_str:int):
        return " "*((taille_str-len(string))//2+(taille_str-len(string))%2)+string+" "*((taille_str-len(string))//2)


    def ecran_combat(self):
        listes_acteurs = []
        listes_nom = []
        listes_titre = []
        nom_le_plus_long, liste_la_plus_longue = 7, 0
        self.equipe_1.liste_casser(listes_acteurs)
        self.equipe_2.liste_casser(listes_acteurs)
        for liste in listes_acteurs:
            str_nom_liste, nom_le_plus_long, liste_la_plus_longue = self.creation_print_liste(liste,nom_le_plus_long,liste_la_plus_longue)
            str_titre_liste, nom_le_plus_long =self.creation_print_liste_titre(liste, nom_le_plus_long)
            listes_nom.append(str_nom_liste)
            listes_titre.append(str_titre_liste)
        n = 2
        nom_le_plus_long += n * 2
        for liste in listes_nom:
            self.clean_des_liste_str(liste,nom_le_plus_long,liste_la_plus_longue)
        for liste in listes_titre:
            self.clean_des_liste_str(liste,nom_le_plus_long,liste_la_plus_longue)

        premier_string = (f"{self.centre_str("Ligne 3",nom_le_plus_long)}|"
                          f"{self.centre_str("Ligne 2",nom_le_plus_long)}|"
                          f"{self.centre_str("Ligne 1",nom_le_plus_long)}| X |"
                          f"{self.centre_str("Ligne 1",nom_le_plus_long)}|"
                          f"{self.centre_str("Ligne 2",nom_le_plus_long)}|"
                          f"{self.centre_str("Ligne 3",nom_le_plus_long)}")
        char_ligne = "="
        deuxieme_string = (f"{nom_le_plus_long*char_ligne}|"
                           f"{nom_le_plus_long*char_ligne}|"
                           f"{nom_le_plus_long*char_ligne}| X |"
                           f"{nom_le_plus_long*char_ligne}|"
                           f"{nom_le_plus_long*char_ligne}|"
                           f"{nom_le_plus_long*char_ligne}")
        self.printer(f"\n\n{len(premier_string)*'#'}\n")
        self.printer(premier_string)
        self.printer(deuxieme_string)

        for k in range(len(listes_nom[0])):
            string_nom = (f"{listes_nom[2][k]}|{listes_nom[1][k]}|{listes_nom[0][k]}| X |"
                      f"{listes_nom[3][k]}|{listes_nom[4][k]}|{listes_nom[5][k]}")
            string_titre = (f"{listes_titre[2][k]}|{listes_titre[1][k]}|{listes_titre[0][k]}| X |"
                          f"{listes_titre[3][k]}|{listes_titre[4][k]}|{listes_titre[5][k]}")
            string_vide = (f"{nom_le_plus_long * " "}|"
                           f"{nom_le_plus_long * " "}|"
                           f"{nom_le_plus_long * " "}| X |"
                           f"{nom_le_plus_long * " "}|"
                           f"{nom_le_plus_long * " "}|"
                           f"{nom_le_plus_long * " "}")
            self.printer(string_vide)
            self.printer(string_nom)
            self.printer(string_titre)

        self.printer(f"\n     {(len(premier_string)-10)*"-"}     \n")

    def temps_execution(self,temps:int,rapidite:int,acteur:Acteur):
        return (temps**2)/(rapidite*self.trouve_equipe(acteur).bonus_commandement())

    def temps(self,capacite,auteur):
        if capacite.atk_mag > 0:
            t = self.temps_execution(capacite.temps, auteur.personnage.vit_mag, auteur)
        else:
            t = self.temps_execution(capacite.temps,auteur.personnage.agilite,auteur)
        return t

    def trouve_equipe(self,acteur:Acteur)->Equipe:
        if acteur in self.equipe_1:
            return self.equipe_1
        return self.equipe_2

    def degat(self,capacite:Capacite_class,cible:Acteur,auteur:Acteur):
        equipe_atk = self.trouve_equipe(auteur)
        equipe_def = self.trouve_equipe(cible)
        if capacite.magie > 0:
            resistance = equipe_def.defense_magique(cible,equipe_atk.obtenir_ligne(auteur))
            puissance = capacite.magie*equipe_atk.attaque_magique(auteur)
            degat = (puissance**1.5)/(resistance**1.5)  * round(rnd.uniform(0.9, 1.1), 2)
        else:
            resistance = equipe_def.defense(cible, equipe_atk.obtenir_ligne(auteur))
            puissance = capacite.force*equipe_atk.attaque(auteur)
            degat = (puissance**1.5)/(resistance**1.5)  * round(rnd.uniform(0.9, 1.1), 2)
        return round(degat,2)

    def obtenir_camps(self,acteur:Acteur):
        if acteur in self.camp_1:
            return self.camp_1
        return self.camp_2

    def attaque(self,action:Action):
        attaquant,defenseur,capacite=action.auteur,action.cible,action.capacite
        deg = self.degat(capacite, defenseur, attaquant)
        attaquant.personnage.res_mag = min(attaquant.personnage.res_mag - capacite.mana, attaquant.personnage.res_tt_mag)
        attaquant.personnage.res_phy = min(attaquant.personnage.res_phy - capacite.endurance, attaquant.personnage.res_tt_phy)
        self.printer(f"{attaquant.personnage.nom} utilise {capacite.nom}", end="")
        if capacite.cible_sois:
            self.printer(f" et recupère {-capacite.mana} de mana et {-capacite.endurance} d'endurance")
        else:
            self.printer(f" et inflige {deg} à {defenseur.personnage.nom}")
        defenseur.degat(deg)

    def choix_cible(self,action:Action,confirmation:bool=False):
        camps_cible = self.obtenir_camps(action.cible)
        if action.capacite.cible_sois or not obtenir_paramettre("action_mouvante"):
            return

        if confirmation and action.auteur.personnage.joueur and action.cible != action.auteur:
            choix = choix_nombre(1, f"Confirmer vous l'attaque sur {action.cible.personnage.nom} (0 = Non, 1 = Oui) ? : ")
            if choix == 1:
                return

        elif confirmation and action.cible.vivant and action.cible != action.auteur:
            return

        if action.auteur.personnage.joueur and action.cible != action.auteur:
            for k in range (len(camps_cible)):
                self.printer(f"{k} : {camps_cible[k]}")
            choix = choix_nombre(len(camps_cible)-1, "Quel ennemie cibler ? :")
            action.cible = camps_cible[choix]
            return
        elif not action.auteur.personnage.joueur:
            cible = action.cible
            equipe_cible = self.trouve_equipe(cible)
            proportion_vie = 0
            for test_cible in camps_cible:
                deg = self.degat(action.capacite, test_cible, action.auteur)
                prop = deg/test_cible.personnage.vie
                if equipe_cible.est_chef(test_cible):
                    prop *= 1.15
                if equipe_cible.est_second(test_cible):
                    prop *= 1.05
                if proportion_vie < prop:
                    proportion_vie = prop
                    cible = test_cible
            action.cible = cible

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
                if action.temps < action_plus_rapide.temps and action.auteur.vivant:
                    action_plus_rapide = action
            liste_actions.remove(action_plus_rapide)

            #Avance dans le temps
            self.temps_combat = self.temps_combat + action_plus_rapide.temps
            for action in liste_actions:
                action.avance_temps(action_plus_rapide.temps)

            #Confirmation cible
            ancienne_cible = action_plus_rapide.cible
            self.choix_cible(action_plus_rapide, True)
            nouvelle_cible = not (ancienne_cible == action_plus_rapide.cible)


            #Attaque
            self.ecran_combat()
            if action_plus_rapide.capacite_basique != None and not nouvelle_cible:
                self.attaque(action_plus_rapide)
            elif action_plus_rapide.position and not nouvelle_cible:
                acteur = action_plus_rapide.auteur
                equipe = self.trouve_equipe(acteur)
                equipe.changement_ligne(acteur)
                self.printer(f"{acteur.personnage.nom} passe en {equipe.ligne_str(acteur)}")
            elif action_plus_rapide.posture and not nouvelle_cible:
                acteur = action_plus_rapide.auteur
                action_plus_rapide.auteur.changement_posture()
                self.printer(f"{acteur.personnage.nom} passe en posture {action_plus_rapide.auteur.posture}")

            #Traite la mort s'il y a
            cible = action_plus_rapide.cible
            if not cible.vivant:
                action_mort:Action
                for action in liste_actions:
                    if action.auteur == cible:
                        action_mort = action
                liste_actions.remove(action_mort)

                if cible in camp_1:
                    camp_1.remove(cible)
                    camp_1_mort.append(cible)
                    self.equipe_1.chute(cible)
                elif cible in camp_2:
                    camp_2.remove(cible)
                    camp_2_mort.append(cible)
                    self.equipe_2.chute(cible)
                self.printer(f"{cible.personnage.nom} est tombé{'e' if cible.personnage.genre == 'female' else ''} !")

            #Nouvelle action
            if len(camp_1)>0 and len(camp_2)>0 and not nouvelle_cible:
                personnage = action_plus_rapide.auteur
                nouvelle_action = self.choix_action(personnage)
                liste_actions.append(nouvelle_action)
            elif len(camp_1)>0 and len(camp_2)>0:
                action_plus_rapide.temps = self.temps(action_plus_rapide.capacite_basique, action_plus_rapide.auteur) / 2
                liste_actions.append(action_plus_rapide)



        if(len(camp_1)>0):
            self.printer("Le camps 1 l'emporte !")
            self.victoire = self.camp_1

        else:
            self.printer("Le camps 2 l'emporte !")
            self.victoire = self.camp_2

    def choix_action(self, acteur: Acteur):
        choix = 0
        if acteur.personnage.joueur:
            self.printer("\n0 : Attaque\n1 : Changement de posture\n2 : Changement de ligne")
            choix = choix_nombre(max = 2,question="Que voulez vous faire :")
            self.printer("\n")

        if choix == 0:
            nouvelle_action= self.choix_attaque(acteur)

        elif choix == 1:
            nouvelle_action = self.choix_posture(acteur)

        elif choix == 2:
            nouvelle_action = self.choix_deplacement(acteur)

        return nouvelle_action



    def choix_attaque(self, acteur: Acteur):
        nouvelle_capacite = acteur.personnage.capaciter_selecteur(acteur.personnage.atk_mag, acteur.personnage.res_phy)
        temps = self.temps(nouvelle_capacite,acteur)
        nouvelle_action = Action(auteur=acteur, cible=None, temps=temps, capacite=nouvelle_capacite)
        if nouvelle_capacite.cible_sois:
            cible = acteur
        elif acteur in self.camp_1:
            self.choix_cible(nouvelle_action)
            cible = self.camp_2[aleatoire(0, len(self.camp_2)) - 1]
        else:
            cible = self.camp_1[aleatoire(0, len(self.camp_1)) - 1]
        nouvelle_action.cible = cible
        return nouvelle_action


    def choix_posture(self, acteur: Acteur):
        temps = self.temps_execution(5,acteur.personnage.agilite,acteur)
        nouvelle_action = Action(auteur=acteur,cible=acteur, temps=temps,posture=True)
        return nouvelle_action

    def choix_deplacement(self, acteur: Acteur):
        temps = self.temps_execution(7, acteur.personnage.agilite,acteur)
        nouvelle_action = Action(auteur=acteur, cible=acteur, temps=temps, position=True)
        self.printer(f"{acteur.personnage.nom} ce prépare a changer de position !")
        return nouvelle_action