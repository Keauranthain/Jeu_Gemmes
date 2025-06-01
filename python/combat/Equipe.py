from python.Basique import choix_nombre, aleatoire
from python.Personnage import Personnage
from python.combat.Acteur import Acteur


class Equipe:
    def __init__(self, premiere_ligne: list[Personnage or Acteur]=[], deuxieme_ligne: list[Personnage or Acteur]=[], troisieme_ligne: list[Personnage or Acteur]=[],
                 chef:Personnage or Acteur = None,second:Personnage or Acteur = None):
        self.premiere_ligne: list[Acteur] = []
        self.premiere_ligne_combat: list[Acteur] = []
        self.preparation_liste_acteur(premiere_ligne, self.premiere_ligne)

        self.deuxieme_ligne: list[Acteur] = []
        self.deuxieme_ligne_combat: list[Acteur] = []
        self.preparation_liste_acteur(deuxieme_ligne, self.deuxieme_ligne)

        self.troisieme_ligne: list[Acteur] = []
        self.troisieme_ligne_combat: list[Acteur] = []
        self.preparation_liste_acteur(troisieme_ligne, self.troisieme_ligne)

        liste_tempo = self.liste()

        if chef is not None and isinstance(chef, Personnage):
            chef = self.trouve_acteur_avec_personnage(chef)
        if second is not None and isinstance(second, Personnage):
            second = self.trouve_acteur_avec_personnage(second)

        if chef == None or chef not in liste_tempo:
            if second == liste_tempo[0] and len(liste_tempo)>1:
                chef = liste_tempo[1]
            else:
                chef = liste_tempo[0]
        self.chef = chef
        if (second == None or second == chef) and len(liste_tempo)>1:
            if chef == liste_tempo[0]:
                second = liste_tempo[1]
            else:
                second = liste_tempo[0]
        elif len(liste_tempo)==1:
            second = None
        self.second = second

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

    def preparation_liste_acteur(self,liste:list[Personnage or Acteur],result:list[Acteur]=[]):
        for objet in liste:
            if isinstance(objet, Personnage):
                perso = Acteur(objet)
            else:
                perso = objet
            perso.ligne = 2
            result.append(perso)
        return result

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
        return perso.def_phy()*self.malus_occupation(ligne)*self.malus_distance(ligne_attaque, ligne)*self.bonus_commandement()

    def defense_magique(self, perso: Acteur,ligne_attaque: int)->float:
        ligne = self.obtenir_ligne(perso)
        return perso.def_mag()*self.malus_occupation(ligne)*self.malus_distance(ligne_attaque, ligne)*self.bonus_commandement()

    def attaque(self, perso: Acteur)->float:
        return perso.atk_phy()*self.bonus_commandement()

    def attaque_magique(self, perso: Acteur)->float:
        return perso.atk_mag()*self.bonus_commandement()

    def vitesse(self, perso: Acteur)->float:
        return perso.personnage.agilite**self.bonus_commandement()

    def vitesse_magique(self, perso: Acteur)->float:
        return perso.personnage.incantation*self.bonus_commandement()

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

    def liste_casser(self,liste:list=None):
        if liste != None:
            liste.append(self.premiere_ligne_combat)
            liste.append(self.deuxieme_ligne_combat)
            liste.append(self.troisieme_ligne_combat)
        return self.premiere_ligne_combat,self.deuxieme_ligne_combat,self.troisieme_ligne_combat

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

    def ligne_str(self, perso: Acteur,combat:bool=True)->str:
        if perso in self.premiere_ligne_combat and combat:
            return "première ligne"
        elif perso in self.deuxieme_ligne_combat and combat:
            return "deuxieme ligne"
        elif perso in self.troisieme_ligne_combat and combat:
            return "troisieme ligne"
        elif perso in self.premiere_ligne:
            return "premiere ligne"
        elif perso in self.deuxieme_ligne:
            return "deuxieme ligne"
        elif perso in self.troisieme_ligne:
            return "troisieme ligne"

    def est_chef(self,acteur:Acteur)->bool:
        return acteur == self.chef

    def est_second(self,acteur:Acteur)->bool:
        return acteur == self.second

    def est_tomber(self,acteur:Acteur)->bool:
        return acteur in self.liste_tomber()

    def est_debout(self,acteur:Acteur)->bool:
        return acteur in self.liste_combat()

    def bonus_commandement(self)->float:
        if self.est_debout(self.chef):
            return self.chef.personnage.charisme ** 0.1
        elif self.est_debout(self.second):
            return self.chef.personnage.charisme ** 0.05
        else:
            return 0.75
    def trouve_acteur_avec_personnage(self,perso:Personnage)->Acteur:
        for acteur in self.liste():
            if acteur.personnage == perso:
                return acteur
        return None

    def changement_ligne(self,acteur: Acteur)->bool:
        possibilite = ["avance", "recule", "immobile"]
        fait = False
        if acteur in self.premiere_ligne_combat:
            print("Changement de ligne")
            possibilite.remove("avance")
        elif acteur in self.troisieme_ligne_combat:
            possibilite.remove("recule")
        if acteur.personnage.joueur:
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