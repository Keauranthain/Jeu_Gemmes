from Combat import Combat
import Personnage as perso

if __name__ == '__main__':
    humain_1 = perso.Personnage(joueur=True, nom="Titi")
    humain_2 = perso.Personnage(joueur=False, nom="Toto")
    goblin_1 = perso.Personnage(joueur=False, nom="Goblin 1", race="goblin")
    goblin_2 = perso.Personnage(joueur=False, nom="Goblin 2", race="goblin")
    goblin_3 = perso.Personnage(joueur=False, nom="Goblin 3", race="goblin")
    humains = [humain_1, humain_2]
    goblins = [goblin_1, goblin_2, goblin_3]
    c = Combat(humains, goblins)
    c.debut()
    if not c.affiche:
        victorieux = c.victoire
        for v in victorieux:
            print(f"{v}, ",end="")