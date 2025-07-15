from Capacite import capacite
from Ressource import obtenir_json


class Race_class():
    def __init__(self,nom):
        base = obtenir_json("race").get(nom, {})

        self.nom: str = nom

        self.magique: bool = base.get("magique", False)

        self.atk_mag: int = base.get("magie", 0)  # magie
        self.def_mag: int = base.get("resistance_magique", 0)  # resistance magique
        self.vit_mag: int = base.get("incantation", 0)  # incantation
        self.res_mag: int = base.get("mana", 0)  # mana
        self.pas_mag: int = base.get("intelligence", 0) #intelligence
        self.atk_phy: int = base.get("force", 0)  # force
        self.def_phy: int = base.get("resistance", 0)  # resistance
        self.vit_phy: int = base.get("agilite", 0)  # agilité
        self.res_phy: int = base.get("endurance", 0)  # endurance
        self.pas_phy: int = base.get("charisme", 0)  # charisme

        self.atk_mag_m: int = base.get("magie_male", 0)
        self.def_mag_m: int = base.get("resistance_magique_male", 0)
        self.vit_mag_m: int = base.get("incantation_male", 0)
        self.res_mag_m: int = base.get("mana_male", 0)
        self.pas_mag_m: int = base.get("intelligence_male", 0)
        self.atk_phy_m: int = base.get("force_male", 0)
        self.def_phy_m: int = base.get("resistance_male", 0)
        self.vit_phy_m: int = base.get("agilite_male", 0)
        self.res_phy_m: int = base.get("endurance_male", 0)
        self.pas_phy_m: int = base.get("charisme_male", 0)

        self.atk_mag_f: int = base.get("magie_female", 0)
        self.def_mag_f: int = base.get("resistance_magique_female", 0)
        self.vit_mag_f: int = base.get("incantation_female", 0)
        self.res_mag_f: int = base.get("mana_female", 0)
        self.pas_mag_f: int = base.get("intelligence_female", 0)
        self.atk_phy_f: int = base.get("force_female", 0)
        self.def_phy_f: int = base.get("resistance_female", 0)
        self.vit_phy_f: int = base.get("agilite_female", 0)
        self.res_phy_f: int = base.get("endurance_female", 0)
        self.pas_phy_f: int = base.get("charisme_female", 0)

        self.vie: int = base.get("vie", 0)
        self.vie_m: int = base.get("vie_male", 0)
        self.vie_f: int = base.get("vie_female", 0)

        self.enfance: int = base.get("enfance", 0)
        self.adolescence: int = base.get("adolescence", 0)
        self.adulte: int = base.get("adulte", 0)
        self.vieillesse: int = base.get("vieillesse", 0)
        self.esperance_de_vie: int = base.get("esperance_de_vie", 0)

        self.capacite: list = [capacite(clef) for clef in base.get("capacite_base", [])]

    def get_atk_mag(self,genre:str):
        if genre == "female":
            return self.atk_mag+self.atk_mag_f
        return self.atk_mag+self.atk_mag_m

    def get_def_mag(self,genre:str):
        if genre == "female":
            return self.def_mag+self.def_mag_f
        return self.def_mag+self.def_mag_m

    def get_vit_mag(self,genre:str):
        if genre == "female":
            return self.vit_mag+self.vit_mag_f
        return self.vit_mag+self.vit_mag_m

    def get_res_mag(self,genre:str):
        if genre == "female":
            return self.res_mag+self.res_mag_f
        return self.res_mag+self.res_mag_m

    def get_pas_mag(self,genre:str):
        if genre == "female":
            return self.pas_mag+self.pas_mag_f
        return self.pas_mag+self.pas_mag_m

    def get_atk_phy(self,genre:str):
        if genre == "female":
            return self.atk_phy+self.atk_phy_f
        return self.atk_phy+self.atk_phy_m

    def get_def_phy(self,genre:str):
        if genre == "female":
            return self.def_phy+self.def_phy_f
        return self.def_phy+self.def_phy_m

    def get_vit_phy(self,genre:str):
        if genre == "female":
            return self.vit_phy+self.vit_phy_f
        return self.vit_phy+self.vit_phy_m

    def get_res_phy(self,genre:str):
        if genre == "female":
            return self.res_phy+self.res_phy_f
        return self.res_phy+self.res_phy_m

    def get_pas_phy(self,genre:str):
        if genre == "female":
            return self.pas_phy+self.pas_phy_f
        return self.pas_phy+self.pas_phy_m

    def get_vie(self,genre:str):
        if genre == "female":
            return self.vie+self.vie_f
        return self.vie+self.vie_m