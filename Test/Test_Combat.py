import time

from python.Ressource import definir_paramettre
from python.combat.Combat import Combat
from personnage import Personnage as perso
from python.combat.Equipe import Equipe

if __name__ == '__main__':
    definir_paramettre("action_mouvante",True)
    humain_1 = perso.Personnage(joueur=True, nom="Joueur")
    humain_2 = perso.Personnage(joueur=False, nom="Allier")
    goblin_1 = perso.Personnage(joueur=False, nom="Goblin 1", race="goblin")
    goblin_2 = perso.Personnage(joueur=False, nom="Goblin 2", race="goblin")
    goblin_3 = perso.Personnage(joueur=False, nom="Goblin 3", race="goblin")
    goblin_4 = perso.Personnage(joueur=False, nom="Goblin 4", race="goblin")
    equipe_humain = Equipe([humain_1,humain_2],second=humain_1)
    equipe_goblin = Equipe([goblin_1, goblin_2, goblin_3],chef=goblin_3)

    print(humain_1.eveille())

    c = Combat(equipe_humain, equipe_goblin,True)
    start = time.time()
    c.debut()
    end = time.time()

    print(f"Durée d'exécution : {round(end - start, 8)} secondes")
    """
    if not c.affiche:
        victorieux = c.victoire
        for v in victorieux:
            print(f"{v}, ",end="")"""

