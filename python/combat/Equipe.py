from python.Personnage import Personnage
from python.combat.Acteur import Acteur


class Equipe:
    def __init__(self, premiere_ligne: list[Personnage]=[], deuxieme_ligne: list[Personnage]=[], troisieme_ligne: list[Personnage]=[]):
        self.premiere_ligne: list[Acteur] = []
        self.premiere_ligne_combat: list[Acteur] = []
        for personnage in premiere_ligne:
            perso = Acteur(personnage)
            perso.ligne = 1
            self.premiere_ligne.append(perso)
            self.premiere_ligne_combat.append(perso)


        self.deuxieme_ligne: list[Acteur] = []
        self.deuxieme_ligne_combat: list[Acteur] = []
        for personnage in deuxieme_ligne:
            perso = Acteur(personnage)
            perso.ligne = 2
            self.deuxieme_ligne.append(perso)
            self.deuxieme_ligne_combat.append(perso)

        self.troisieme_ligne: list[Acteur] = []
        self.troisieme_ligne_combat: list[Acteur] = []
        for personnage in troisieme_ligne:
            perso = Acteur(personnage)
            perso.ligne = 3
            self.troisieme_ligne.append(perso)
            self.troisieme_ligne_combat.append(perso)

        self.bonus_defense_ligne_occupe = 1.5
        self.bonus_defense_distance = 0.1
        self.distance_sans_malus = 2

    def reset_ligne(self):
        self.premiere_ligne_combat.clear()
        self.deuxieme_ligne_combat.clear()
        self.troisieme_ligne_combat.clear()
        self.premiere_ligne_combat = self.premiere_ligne.copy()
        self.deuxieme_ligne_combat = self.deuxieme_ligne.copy()
        self.deuxieme_ligne_combat = self.troisieme_ligne.copy()

    def obtenir_ligne(self,perso: Acteur):
        if perso in self.premiere_ligne_combat:
            return 1
        if perso in self.deuxieme_ligne_combat:
            return 2
        if perso in self.troisieme_ligne_combat:
            return 3
        return 0

    def malus_occupation(self,ligne:int):
        result = 1.0
        if ligne == 2:
            if len(self.premiere_ligne_combat) != 0:
                result = result*self.bonus_defense_ligne_occupe
        elif ligne == 3:
            if len(self.deuxieme_ligne_combat) != 0:
                result = result * self.bonus_defense_ligne_occupe
            if len(self.premiere_ligne_combat) != 0:
                result = result * self.bonus_defense_ligne_occupe
        return result

    def malus_distance(self,ligne_attaque:int,ligne_defence:int):
        distance = ligne_attaque + ligne_defence - 1
        if distance > self.distance_sans_malus:
            return (distance - self.distance_sans_malus)*self.bonus_defense_distance
        return 1.0


    def defense(self, perso: Acteur,ligne_attaque: int):
        ligne = self.obtenir_ligne(perso)
        return perso.def_phy()*self.malus_occupation(ligne)*self.malus_distance(ligne_attaque, ligne)

    def defense_magique(self, perso: Acteur,ligne_attaque: int):
        ligne = self.obtenir_ligne(perso)
        return perso.def_mag()*self.malus_occupation(ligne)*self.malus_distance(ligne_attaque, ligne)

    def avance(self, perso: Acteur):
        if perso in self.deuxieme_ligne_combat:
            self.deuxieme_ligne_combat.remove(perso)
            self.premiere_ligne_combat.append(perso)
        elif perso in self.troisieme_ligne_combat:
            self.troisieme_ligne_combat.remove(perso)
            self.deuxieme_ligne_combat.append(perso)

    def reculer(self, perso: Acteur):
        if perso in self.premiere_ligne_combat:
            self.premiere_ligne_combat.remove(perso)
            self.deuxieme_ligne_combat.append(perso)
        elif perso in self.deuxieme_ligne_combat:
            self.deuxieme_ligne_combat.remove(perso)
            self.troisieme_ligne_combat.append(perso)