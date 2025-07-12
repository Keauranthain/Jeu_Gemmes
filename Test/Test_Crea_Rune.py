from Rune.Rune import rune_aleatoire
from Type import Type_class

if __name__ == '__main__':
    for k in range (26):
        print(rune_aleatoire(niveau=k,inconnu=False),end="\n\n")