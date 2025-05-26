from Basique import obtenir_texte
from Ressource import capacites_global

capacites_jeu = {}

def capacite(clef:str):
    return capacites_jeu[clef]

def trouve_clef_capacite(temps:int,puissance:int,magique:bool=False,physique:bool=False):
    if magique:
        clef = capacites_global["capacite_magique"][f"{temps},{puissance}"]
    else:
        clef = capacites_global["capacite_physique"][f"{temps},{puissance}"]
    return clef

def trouve_nom_capacite(temps:int,puissance:int,magique:bool=False,physique:bool=False):
    return obtenir_texte(trouve_clef_capacite(temps,puissance,magique,physique))


class Capacite_class():
    def __init__(self,nom,clef,force:int = 0,magie:int = 0,temps:int = 0,
                 cible_autre:bool = True,cible_sois:bool = False,soin:bool = False,
                 magique:bool = True,mana:int = 0,endurance:int=0):
        self.nom = nom
        self.clef = clef
        self.force = force
        self.magie = magie
        if mana == 0 :
            self.mana = magie*(temps-10)*-1
        else:
            self.mana = mana
        if endurance == 0 :
            self.endurance = force*(temps-10)*-1
        else:
            self.endurance = endurance
        self.temps = temps
        self.cible_autre = cible_autre
        self.cible_sois = cible_sois
        self.soin = soin
        self.magique = magique

def capacite_basique():
    capacite = Capacite_class("Coup de poing", "coup_de_poing_capacite", force=2, temps=7,magique=False,endurance=2)
    capacites_jeu["coup_de_poing_capacite"] =  capacite
    capacite = Capacite_class("Repos", "repos_capacite",mana  = -2, endurance = -2,
                              temps= 7,cible_sois = True,cible_autre = False)
    capacites_jeu["repos_capacite"] = capacite


def setup():
    for temps in range (3,8):
        for puissance in range (3,8):
            clef = trouve_clef_capacite(temps,puissance)
            nom = obtenir_texte("fr",clef)
            capacites_jeu[clef]=Capacite_class(nom,clef,force=puissance,temps=temps)
            clef = trouve_clef_capacite(temps, puissance,magique=True)
            nom = obtenir_texte("fr",clef)
            capacites_jeu[clef] = Capacite_class(nom, clef, magie=puissance, temps=temps)
    capacite_basique()

setup()