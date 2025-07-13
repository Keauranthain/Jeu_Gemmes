import math
from functools import total_ordering

from Basique import aleatoire, True_ou_False, aleatoire_liste
from Capacite import Capacite_class, capacites_jeu
from Talent import Tous_talents
from Type import Type_class
import Variable_Global
from Ressource import fichier_config

class Rune_class():
    def __init__(self, niveau: int = 1,inconnu:bool=False):
        self.niveau = niveau
        self.inconnu:bool = inconnu
        self.atk_mag:int = 0
        self.def_mag:int = 0
        self.vit_mag:int = 0
        self.res_mag:int = 0
        self.atk_phy:int = 0
        self.def_phy:int = 0
        self.vit_phy:int = 0
        self.res_phy:int = 0

    def __str__(self):
        if fichier_config.getboolean("Rune", "CACHER_LE_NIVEAU_DES_RUNES_INCONNUES", fallback=False):
            return f"Rune inconnue"
        return f"Rune inconnue de niveau {self.niveau}"

    def reveler(self):
        self.inconnu = True

    def definir_mag(self,atk_mag:int,def_mag:int,vit_mag:int,res_mag:int):
        self.atk_mag = atk_mag
        self.def_mag = def_mag
        self.vit_mag = vit_mag
        self.res_mag = res_mag

    def definir_phy(self,atk_phy:int,def_phy:int,vit_phy:int,res_phy:int):
        self.atk_phy = atk_phy
        self.def_phy = def_phy
        self.vit_phy = vit_phy
        self.res_phy = res_phy

    def str_bonus_capacite(self)->str:
        result:str = f"||| Capacité |||\n"
        result += f"          | Physique |  Magique |\n"
        result += f"=================================\n"
        result += f"Attaque   |{(9-len(str(self.atk_phy)))*" "+str(self.atk_phy)} |{(9-len(str(self.atk_mag)))*" "+str(self.atk_mag)} |\n"
        result += f"Defence   |{(9-len(str(self.def_phy)))*" "+str(self.def_phy)} |{(9-len(str(self.def_mag)))*" "+str(self.def_mag)} |\n"
        result += f"Vitesse   |{(9-len(str(self.vit_phy)))*" "+str(self.vit_phy)} |{(9-len(str(self.vit_mag)))*" "+str(self.vit_mag)} |\n"
        result += f"Ressource |{(9-len(str(self.res_phy)))*" "+str(self.res_phy)} |{(9-len(str(self.res_mag)))*" "+str(self.res_mag)} |\n"
        return result
class Rune_rupture_class(Rune_class):
    def __init__(self, niveau: int = 1,inconnu:bool=False):
        super().__init__(niveau, inconnu)
    def __str__(self):
        if self.inconnu:
            return super().__str__()
        return str(f"Rune de rupture de niveau {self.niveau}")

class Rune_capacite_class(Rune_class):
    def __init__(self, niveau:int=1,magique:bool=False,physique:bool=False,type:Type_class=None,inconnu:bool=False):
        super().__init__(niveau, inconnu)
        point_competence = obtenir_point_competence(niveau)
        attaque,defense,vitesse,ressource = repartir_point(point_competence,4)
        self.type = trouve_type(type)

        if (magique and not physique) or (not physique and True_ou_False()):
            self.domaine = "magique"
            self.definir_mag(attaque,defense,vitesse,ressource)
        else:
            self.domaine = "physique"
            self.definir_phy(attaque, defense, vitesse, ressource)
        self.capacite = self.trouve_capacite()


    def __str__(self):
        if self.inconnu:
            return super().__str__()
        return (f"Rune academique {self.domaine} {self.type.adjectif_feminin}, niveau {self.niveau} \n{self.str_bonus_capacite()}|||Capacité|||\n"
                f"{self.capacite}")

    def trouve_capacite(self):
        toutes_capacite = []
        for p in range (3,8):
            for v in range (3,8):
                toutes_capacite.append(capacites_jeu[f"spe_{self.domaine[:3]}_p{p}_v{v}_capacite"])
        toutes_capacite_poids = [self.poids_capacite(capacite) for capacite in toutes_capacite]
        poids_total = sum(poids for poids in toutes_capacite_poids)
        result = aleatoire(1, poids_total)
        choix = 0
        while result > toutes_capacite_poids[choix]:
            result -= toutes_capacite_poids[choix]
            choix += 1
        return toutes_capacite[choix]

    def poids_capacite(self,capacite:Capacite_class, sigma: float = 1.5, facteur: float = 100.0) -> int:
        rang = capacite.vitesse+max(capacite.force,capacite.magie)-5
        mu = 1 + (8 / 19) * (min(self.niveau,20) - 1)
        exponent = -((rang - mu) ** 2) / (2 * sigma ** 2)
        return max(int(facteur * math.exp(exponent)),1)

class Rune_talent_class(Rune_class):
    def __init__(self, niveau: int = 1, theme: str = "", talent:Tous_talents=None,type:Type_class=None,inconnu:bool=False):
        super().__init__(niveau, inconnu)
        point_competence = obtenir_point_competence(niveau)
        mag, phy = repartir_point(point_competence,2)
        themes_disponibles = ["atk", "def", "vit", "res"]
        if theme not in themes_disponibles:
            theme = themes_disponibles[aleatoire(0,len(themes_disponibles)-1)]
        match theme:
            case "atk":
                theme = "attaque"
                self.atk_phy = phy
                self.atk_mag = mag
            case "def":
                theme = "défense"
                self.def_mag = mag
                self.def_phy = phy
            case "vit":
                theme = "vitesse"
                self.vit_mag = mag
                self.vit_phy = phy
            case "res":
                theme = "résistance"
                self.res_phy = phy
                self.res_mag = mag
        self.theme = theme
        self.type = trouve_type(type)
        if talent == None:
            self.talent = aleatoire_liste(list(Tous_talents))
        else:
            self.talent = talent

    def __str__(self):
        if self.inconnu:
            return super().__str__()
        if self.talent == Tous_talents.RRESISTANCE:
            talent_nom = f"{self.talent.value.nom} : {self.type.nom}"
            talent_desc = f"Ajoute un cran de résistance à l'élément {self.type.nom}"
        else:
            talent_nom = self.talent.value.nom
            talent_desc =self.talent.value.description
        return (f"Rune talentueuse {self.theme} {self.type.adjectif_feminin}, niveau {self.niveau} \n"
                f"{self.str_bonus_capacite()}|||Talent|||\n"
                f"{talent_nom}\n{talent_desc}")


def obtenir_point_competence(niveau):
    niv:int = niveau
    result:int = 0
    multiplicateur:int = 1
    step_par_mult:int = 10
    while niv > 0:
        result += multiplicateur * min(step_par_mult, niv)
        niv -= step_par_mult
        multiplicateur += 1
    return result

def rune_aleatoire(niveau:int=1,inconnu:bool=True):
    alea = aleatoire(1,100)
    if alea < 50 :
        return Rune_capacite_class(niveau, inconnu=inconnu)
    elif alea > 51 :
        return Rune_talent_class(niveau,inconnu=inconnu)
    else :
        return Rune_rupture_class(niveau,inconnu=inconnu)

def trouve_type(type):
    if type == None:
        types = Variable_Global.tous_types
        return types[aleatoire(0, len(types) - 1)]
    else:
        return type

def repartir_point(nombre_point:int,nombre_caracteristique:int) -> tuple[int, ...]:
    total = 0
    liste_caracteristiques = []

    for k in range (0,nombre_caracteristique):
        alea = aleatoire(1,100)
        liste_caracteristiques.append(alea)
        total += alea

    attendu = [caracteristique/total*nombre_point for caracteristique in liste_caracteristiques]
    result = [int(caracteristique) for caracteristique in attendu]

    while sum(result) < nombre_point:
        ecart = [attendu[k] - result[k] for k in range(nombre_caracteristique)]
        result[ecart.index(max(ecart))]+=1
    return *result,
