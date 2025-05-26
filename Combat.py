import Personnage as perso
import Capacite as capa
import random as rnd

class Combat():
    def __init__(self,combattant_1:perso.Personnage,combattant_2:perso.Personnage,combattant_3:perso.Personnage):
        self.combattant_1 = combattant_1
        self.camp_1 = [combattant_1]
        self.camp_2 = [combattant_2,combattant_3]
        self.combattant_2 = combattant_2

    def str_vie(self,personnage:perso.Personnage):
        return f"{personnage.nom} {personnage.vie} / {personnage.vie_total}"


    def ecrant_combat(self,camp_1,camp_2):
        """
        TODO
        Calculer tous les vie str stoquer en liste
        determiner le plus long
        printe le toups
        trouver le joueur
        print stat+
        """
        n = 10
        nom_le_plus_long = 0
        for perso in camp_1:
            if len(self.str_vie(perso)) > nom_le_plus_long:
                nom_le_plus_long = perso.nom
        for perso in camp_2:
            if perso.nom > nom_le_plus_long:
                nom_le_plus_long = perso.nom
        perso_1_c1 = self.str_vie(camp_1[0])
        perso_1_c2 = self.str_vie(camp_2[0])
        print(
            f"{self.str_vie(camp_1[0])}"
            f" {n*'-'} VS {n*'-'} "
            f"{self.str_vie(camp_2[0])}")

        for k in range(max(len(camp_1), len(camp_2))-1):
            print(
                f"{self.str_vie(camp_1[k])}"
                f"{2*n+6 * ' '}"
                f"{self.str_vie(camp_2[k])}")
        #print(
        #    f"\n\nEndurance : {combat_1.endurance}/{combat_1.endurance_total}"
        #    f"\nMana : {combat_1.mana}/{combat_1.mana_total}\n")

    def temps(self,capacite,auteur):
        if capacite.magie > 0:
            t = (capacite.temps**2)/auteur.incantation
        else:
            t = (capacite.temps**2)/auteur.agilite
        return t

    def degat(self,capacite,cible,auteur):
        if capacite.magie > 0:
            d = (capacite.magie*auteur.magie**1.5)/(cible.resistance_magique**1.5)  * round(rnd.uniform(0.9, 1.1), 2)
        else:
            d = (capacite.force*auteur.force**1.5)/(cible.resistance**1.5)  * round(rnd.uniform(0.9, 1.1), 2)
        return round(d,2)

    def attaque(self,attaquant:perso.Personnage,defenseur:perso.Personnage,capacite):
        deg = self.degat(capacite, defenseur, attaquant)
        attaquant.mana = min(attaquant.mana - capacite.mana, attaquant.mana_total)
        attaquant.endurance = min(attaquant.endurance - capacite.endurance, attaquant.endurance_total)
        print(f"{attaquant.nom} utilise {capacite.nom}", end="")
        if capacite.cible_sois:
            print(f" et recupère {-capacite.mana} de mana et {-capacite.endurance} d'endurance")
        else:
            print(f" et inflige {deg}")
        defenseur.vie = max(0, round(defenseur.vie - deg, 2))
        self.ecrant_combat(attaquant, defenseur)
        if defenseur.vie > 0:
            nouvelle_capacite = attaquant.capaciter_selecteur(attaquant.magie, attaquant.endurance)
            temps = self.temps(nouvelle_capacite, attaquant)
            return nouvelle_capacite, temps
        return 0,0

    def debut(self):
        camp_1 = self.camp_1
        camp_2 = self.camp_2

        self.ecrant_combat(combat_1,combat_2)

        cap_1 = combat_1.capaciter_selecteur(combat_1.magie,combat_1.endurance)
        cap_2 = combat_2.capaciter_selecteur(combat_2.magie,combat_2.endurance)
        temps_1 = self.temps(cap_1,combat_1)
        temps_2 = self.temps(cap_2,combat_2)

        while(self.combattant_1.vie>0 and self.combattant_2.vie>0):
            if temps_1 < temps_2:
                temps_2 = temps_2 - temps_1
                cap_1,temps_1 = self.attaque(combat_1,combat_2,cap_1)
            else :
                temps_1 = temps_1 - temps_2
                cap_2,temps_2 = self.attaque(combat_2,combat_1,cap_2)
            print()
        if combat_1.vie==0:
            print(f"{combat_1.nom} mort")
        else:
            print(f"{combat_2.nom} mort")

class Action():
    def __init__(self,auteur:perso.Personnage,cible:perso.Personnage,capacite:capa.Capacite_class,temps:int):
        self.auteur = auteur
        self.cible = cible
        self.capacite = capacite
        self.temps = temps

    def temps(self,avance:int):
        self.temps = self.temps-avance