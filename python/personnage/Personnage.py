from Rune.Rune import Rune_capacite_class, Rune_class, Rune_talent_class
from Talent import Tous_talents
from Type import Type_class
from python.Capacite import capacite
from python.Ressource import obtenir_json
from python.Basique import choix_nombre
from python.personnage.Race import Race_class

class Personnage():
    def __init__(self, nom:str, race:str = "humain", joueur = False,male:bool = False,female:bool = False):

        if male or not(female):
            self.genre = "male"
        else:
            self.genre = "female"
        self.nom:str = nom
        self.race = Race_class(race)


        self.res_mag:int = self.race.get_res_mag(self.genre)
        self.res_phy:int = self.race.get_res_phy(self.genre)
        self.vie:int = self.race.get_vie(self.genre)

        self.eveiller = False

        self.runes = []
        self.capacites_runes = []
        self.atk_mag_rune:int = 0 #magie
        self.def_mag_rune:int = 0 #resistance magique
        self.vit_mag_rune:int = 0 #incantation
        self.res_mag_rune:int = 0 #mana
        self.atk_phy_rune:int = 0 #force
        self.def_phy_rune:int = 0 #resistance
        self.vit_phy_rune:int = 0 #agilité
        self.res_phy_rune:int = 0 #endurance

        self.talents = {}
        self.cran_element = {}
        self.cran_element_defense_sup = []

        self.niveau:int = 1
        self.exp:int = 0

        self.joueur = joueur

    def __str__(self):
        return f"{self.nom}, {self.race}, {self.genre}, - Vie: {self.vie}/{self.get_vie_tt()}, Mana: {self.res_mag}/{self.get_res_mag()}, Endurance: {self.res_phy}/{self.get_res_phy()}"

    def capaciter_selecteur(self,mana,endurance):
        liste_temporaire = []
        for k in self.race.capacite:
            if k.res_mag<=mana and k.res_phy<=endurance:
                liste_temporaire.append(k)
        if self.joueur:
            print(f"Endurance: {endurance}/{self.race.get_res_phy(self.genre)}\nMana: {mana}/{self.race.get_res_mag(self.genre)}\n")
            for k in range (len(liste_temporaire)):
                print(f"{k} : {liste_temporaire[k].nom}, mana : {liste_temporaire[k].res_mag},"
                      f" endurance : {liste_temporaire[k].res_phy}")
            result = choix_nombre(max = len(liste_temporaire)-1, question = "Capacité : ")
            return liste_temporaire[result]
        return self.race.capacite[0]

    def get_atk_mag(self)->int:
        return self.race.get_atk_mag(self.genre) + self.atk_mag_rune

    def get_def_mag(self)->int:
        return self.race.get_def_mag(self.genre) + self.def_mag_rune

    def get_vit_mag(self)->int:
        return self.race.get_vit_mag(self.genre) + self.vit_mag_rune

    def get_res_mag(self)->int:
        return self.race.get_res_mag(self.genre) + self.res_mag_rune

    def get_pas_mag(self)->int:
        mult_talent = (1+self.talents.get(Tous_talents.INTELLIGENCE,0)/10)
        bonus_rune = self.moyenne_mag()
        return int((self.race.get_pas_mag(self.genre)+bonus_rune)*mult_talent)

    def get_atk_phy(self)->int:
        return self.race.get_atk_phy(self.genre) + self.atk_phy_rune

    def get_def_phy(self)->int:
        return self.race.get_def_phy(self.genre) + self.def_phy_rune

    def get_vit_phy(self)->int:
        return self.race.get_vit_phy(self.genre) + self.vit_phy_rune

    def get_res_phy(self)->int:
        return self.race.get_res_phy(self.genre) + self.res_phy_rune

    def get_pas_phy(self)->int:
        mult_talent = (1+self.talents.get(Tous_talents.CHARISME,0)/10)
        bonus_rune = self.moyenne_phy()
        return int((self.race.get_pas_phy(self.genre)+bonus_rune)*mult_talent)

    def get_vie_tt (self)->int:
        mult_talent = (1 + self.talents.get(Tous_talents.RESILIENCE, 0) / 10)
        return int((self.race.get_vie(self.genre)+(self.moyenne_mag()+self.moyenne_phy())/2)*mult_talent)

    def moyenne_phy(self)->int:
        return int((self.atk_phy_rune+self.def_phy_rune+self.vit_phy_rune+self.res_phy_rune)/4)

    def moyenne_mag(self)->int:
        return int((self.atk_mag_rune+self.def_mag_rune+self.vit_mag_rune+self.res_mag_rune)/4)

    def equipe_rune(self,rune:Rune_class)->str:
        if len(self.runes)>= self.niveau:
            return "Pas d'emplacement de Rune disponible"
        if rune.niveau >= self.niveau:
            return "Rune trop puissante"
        self.runes.append(rune)
        self.amelioration_competence_rune(rune)
        match rune:
            case Rune_capacite_class():
                self.capacites_runes.append(rune.capacite)
            case Rune_talent_class():
                self.ajout_talent(rune)

        return "Rune absorbée"

    def amelioration_competence_rune(self,rune:Rune_class):
        self.atk_mag_rune:int = rune.atk_mag
        self.def_mag_rune:int = rune.def_mag
        self.vit_mag_rune:int = rune.vit_mag
        self.res_mag_rune:int = rune.res_mag
        self.atk_phy_rune:int = rune.atk_phy
        self.def_phy_rune:int = rune.def_phy
        self.vit_phy_rune:int = rune.vit_phy
        self.res_phy_rune:int = rune.res_phy

    def ajout_talent(self,rune:Rune_talent_class):
        if rune.talent is Tous_talents.RRESISTANCE:
            self.cran_element_defense_sup[rune.element] = self.cran_element_defense_sup.get(rune.element, 0) + 1
        else:
            self.talents[rune.talent] = self.talents.get(rune.talent, 0) + 1

    def eveille(self):
        if not self.race.magique and not self.eveiller:
            self.eveiller = True
            return f"{self.nom} s'éveille"
        elif self.eveiller:
            return f"{self.nom} est déjà éveillé"
        return f"{self.nom} est d'une race qui n'a pas d'éveille"