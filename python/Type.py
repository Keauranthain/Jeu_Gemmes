from Ressource import obtenir_json

tous_types = []

class Type_class:
    def __init__(self,nom:str,adjectif:str,adjectif_feminin:str):
        self.nom = nom
        self.adjectif = adjectif
        self.adjectif_feminin = adjectif_feminin
        self.faiblesse = []
        self.resistance = []

    def __str__(self):
        return self.nom

    def nouvelle_faiblesse(self,faiblesse):
        self.faiblesse.append(faiblesse)

    def nouvelle_resistance(self,resistance):
        self.resistance.append(resistance)

    def variation(self,type):
        impact = 0.25
        mult_personnel = 2
        if type == self:
            return 1-mult_personnel*impact
        elif type in self.resistance:
            return 1-impact
        elif type in self.faiblesse:
            return 1+impact
        else:
            return 1

def setup():
    for clef, contenu in obtenir_json("type").items():
        tous_types.append(Type_class(
            nom=contenu.get("nom", clef),
            adjectif=contenu.get("adjectif", clef),
            adjectif_feminin=contenu.get("adjectif_feminin", clef),
        ))

setup()