from Variable_Global import tous_types


from enum import Enum
from typing import NamedTuple

class Talent(NamedTuple):
    nom: str
    description: str

class Tous_talents(Enum):
    RRESISTANCE = Talent("Résistance élémentaire","Ajoute un cran de résistance à l'élément de la rune contenant le talent")
    RESILIENCE = Talent("Résilience", "Ajoute 10% à la santé max")
    RECUP_ENDURANCE = Talent("Récupération d'endurance", "Récupère 2% d'endurance à chaque action")
    RECUP_MANA = Talent("Récupération de mana", "Récupère 2% de mana à chaque action")
    CATALYSEUR = Talent("Catalyseur", "Gagne des points d'expérience supplémentaires après chaque combat")
    INTELLIGENCE = Talent("Intelligence", "+10% d'intelligence")
    CHARISME = Talent("Charisme", "+10% de charisme")
