from python.Basique import choix_nombre, aleatoire
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

        self.deuxieme_ligne: list[Acteur] = []
        self.deuxieme_ligne_combat: list[Acteur] = []
        for personnage in deuxieme_ligne:
            perso = Acteur(personnage)
            perso.ligne = 2
            self.deuxieme_ligne.append(perso)

        self.troisieme_ligne: list[Acteur] = []
        self.troisieme_ligne_combat: list[Acteur] = []
        for personnage in troisieme_ligne:
            perso = Acteur(personnage)
            perso.ligne = 3
            self.troisieme_ligne.append(perso)

        self.reset_ligne()
        self.bonus_defense_ligne_occupe = 1.5
        self.bonus_defense_distance = 0.1
        self.distance_sans_malus = 2

    def __str__(self):
        return (f"Première ligne : {self.premiere_ligne}\nDeuxième ligne : {self.deuxieme_ligne}\nTroisieme ligne : {self.troisieme_ligne}\n\n"
                f"Première ligne combat : {self.premiere_ligne_combat}\nDeuxième ligne combat : {self.deuxieme_ligne_combat}"
                f"\nTroisieme ligne combat : {self.troisieme_ligne_combat}")

    def __contains__(self, acteur: Acteur) -> bool:
        if acteur in self.premiere_ligne:
            return True
        if acteur in self.deuxieme_ligne:
            return True
        if acteur in self.troisieme_ligne:
            return True
        return False

    def reset_ligne(self):
        self.premiere_ligne_combat.clear()
        self.deuxieme_ligne_combat.clear()
        self.troisieme_ligne_combat.clear()
        self.premiere_ligne_combat = self.premiere_ligne.copy()
        self.deuxieme_ligne_combat = self.deuxieme_ligne.copy()
        self.troisieme_ligne_combat = self.troisieme_ligne.copy()

    def obtenir_ligne(self,perso: Acteur)->int:
        if perso in self.premiere_ligne_combat:
            return 1
        if perso in self.deuxieme_ligne_combat:
            return 2
        if perso in self.troisieme_ligne_combat:
            return 3
        return 0

    def malus_occupation(self,ligne:int)->float:
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

    def malus_distance(self,ligne_attaque:int,ligne_defence:int)->float:
        distance = ligne_attaque + ligne_defence - 1
        if distance > self.distance_sans_malus:
            return 1+(distance - self.distance_sans_malus)*self.bonus_defense_distance
        return 1.0


    def defense(self, perso: Acteur,ligne_attaque: int)->float:
        ligne = self.obtenir_ligne(perso)
        return perso.def_phy()*self.malus_occupation(ligne)*self.malus_distance(ligne_attaque, ligne)

    def defense_magique(self, perso: Acteur,ligne_attaque: int)->float:
        ligne = self.obtenir_ligne(perso)
        return perso.def_mag()*self.malus_occupation(ligne)*self.malus_distance(ligne_attaque, ligne)

    def avance(self, perso: Acteur)->None:
        if perso in self.deuxieme_ligne_combat:
            self.deuxieme_ligne_combat.remove(perso)
            self.premiere_ligne_combat.append(perso)
        elif perso in self.troisieme_ligne_combat:
            self.troisieme_ligne_combat.remove(perso)
            self.deuxieme_ligne_combat.append(perso)

    def reculer(self, perso: Acteur)->None:
        if perso in self.premiere_ligne_combat:
            self.premiere_ligne_combat.remove(perso)
            self.deuxieme_ligne_combat.append(perso)
        elif perso in self.deuxieme_ligne_combat:
            self.deuxieme_ligne_combat.remove(perso)
            self.troisieme_ligne_combat.append(perso)

    def decime(self)-> bool:
        if len(self.premiere_ligne_combat) == 0 and len(self.deuxieme_ligne_combat) == 0 and len(self.troisieme_ligne_combat) == 0:
            return True
        return False

    def liste_combat(self)-> list[Acteur]:
        result = []
        for perso in self.premiere_ligne_combat:
            result.append(perso)
        for perso in self.deuxieme_ligne_combat:
            result.append(perso)
        for perso in self.troisieme_ligne_combat:
            result.append(perso)
        return result

    def liste(self) -> list[Acteur]:
        result = []
        for perso in self.premiere_ligne:
            result.append(perso)
        for perso in self.deuxieme_ligne:
            result.append(perso)
        for perso in self.troisieme_ligne:
            result.append(perso)
        return result

    def chute(self, perso: Acteur)->None:
        if perso in self.premiere_ligne_combat:
            self.premiere_ligne_combat.remove(perso)
        elif perso in self.deuxieme_ligne_combat:
            self.deuxieme_ligne_combat.remove(perso)
        else:
            self.troisieme_ligne_combat.remove(perso)

    def liste_tomber(self)-> list[Acteur]:
        result = []
        for perso in self.liste():
            if self.obtenir_ligne(perso) == 0:
                result.append(perso)
        return result

    def changement_ligne(self,acteur: Acteur)->bool:
        possibilite = ["avance", "recule", "immobile"]
        fait = False
        if acteur in self.premiere_ligne_combat:
            possibilite.remove("avance")
        elif acteur in self.troisieme_ligne_combat:
            possibilite.remove("recule")
        if acteur.personnage.joueur:
            print(f"Ligne actuel : {self.obtenir_ligne(acteur)}")
            for k in range (len(possibilite)):
                print(f"{k}: {possibilite[k]}")
            choix = possibilite[choix_nombre(max = len(possibilite)-1, question="Déplacement : ")]
        else:
            choix = possibilite[aleatoire(0,len(possibilite)-1)]
        if choix == "avance":
            self.avance(acteur)
            fait = True
        if choix == "recule":
            self.reculer(acteur)
            fait = True
        return fait