from Combat import Combat
import Personnage as perso

if __name__ == '__main__':
    combattant_1 = perso.Personnage(joueur=True, nom="Titi")
    combattant_2 = perso.Personnage(joueur=False, nom="Goblin 1", race="goblin")
    combattant_3 = perso.Personnage(joueur=False, nom="Goblin 2", race="goblin")
    combattant_4 = perso.Personnage(joueur=False, nom="Goblin 3", race="goblin")
    c = Combat(combattant_1, combattant_2)
    c.debut()