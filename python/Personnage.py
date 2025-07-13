from Rune.Rune import Rune_capacite_class, Rune_class, Rune_talent_class
from Talent import Tous_talents
from Type import Type_class
from python.Capacite import capacite
from python.Ressource import obtenir_json
from python.Basique import choix_nombre

class Personnage():
    def __init__(self, nom:str, race:str = "humain", joueur = False,male:bool = False,female:bool = False):

        if male or not(female):
            self.genre = "male"
        else:
            self.genre = "female"
        self.nom = nom
        self.race = race

        base = obtenir_json("race").get(race, {})

        self.atk_mag:int = base.get("magie", 0) + base.get(f"magie_{self.genre}", 0)
        self.def_mag:int = base.get("resistance_magique", 0) + base.get(f"resistance_magique_{self.genre}", 0)
        self.vit_mag:int = base.get("incantation", 0) + base.get(f"incantation_{self.genre}", 0)
        self.res_tt_mag:int = base.get("mana", 0) + base.get(f"mana_{self.genre}", 0)
        self.res_mag:int = self.res_tt_mag
        self.atk_phy:int = base.get("force", 0) + base.get(f"force_{self.genre}", 0)
        self.def_phy:int = base.get("resistance", 0) + base.get(f"resistance_{self.genre}", 0)
        self.agilite:int = base.get("agilite", 0) + base.get(f"agilite_{self.genre}", 0)
        self.res_tt_phy:int = base.get("endurance", 0) + base.get(f"endurance_{self.genre}", 0)
        self.res_phy:int = self.res_tt_phy
        self.vie_total:int = base.get("vie", 0) + base.get(f"vie_{self.genre}", 0)
        self.vie:int = self.vie_total

        self.capacite_basique = []
        for capacite_clef in base.get("capacite_base", []):
            self.capacite_basique.append(capacite(capacite_clef))

        self.charisme = base.get("charisme", 0) + base.get(f"charisme_{self.genre}", 0)
        self.intelligence = base.get("intelligence", 0) + base.get(f"intelligence_{self.genre}", 0)

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
        return f"{self.nom}, {self.race}, {self.genre}, - Vie: {self.vie}/{self.vie_total}, Mana: {self.res_mag}/{self.res_tt_mag}, Endurance: {self.res_phy}/{self.res_tt_phy}"

    def capaciter_selecteur(self,mana,endurance):
        liste_temporaire = []
        for k in self.capacite_basique:
            if k.res_mag<=mana and k.res_phy<=endurance:
                liste_temporaire.append(k)
        if self.joueur:
            print(f"Endurance: {endurance}/{self.res_tt_phy}\nMana: {mana}/{self.res_tt_mag}\n")
            for k in range (len(liste_temporaire)):
                print(f"{k} : {liste_temporaire[k].nom}, mana : {liste_temporaire[k].res_mag},"
                      f" endurance : {liste_temporaire[k].res_phy}")
            result = choix_nombre(max = len(liste_temporaire)-1, question = "Capacité : ")
            return liste_temporaire[result]
        return self.capacite_basique[0]

    def get_atk_mag(self)->int:
        return self.atk_mag + self.atk_mag_rune

    def get_def_mag(self)->int:
        return self.def_mag + self.def_mag_rune

    def get_vit_mag(self)->int:
        return self.vit_mag + self.vit_mag_rune

    def get_res_mag(self)->int:
        return self.res_tt_mag + self.res_mag_rune

    def get_atk_phy(self)->int:
        return self.atk_phy + self.atk_phy_rune

    def get_def_phy(self)->int:
        return self.def_phy + self.def_phy_rune

    def get_vit_phy(self)->int:
        return self.agilite + self.vit_phy_rune

    def get_res_phy(self)->int:
        return self.res_tt_phy + self.res_phy_rune

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