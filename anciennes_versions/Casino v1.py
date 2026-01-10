import random

def BlackJack(Money):
    print("\n=== BLACKJACK ===")

    valeurs = {
        "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9,
        "10":10, "J":10, "Q":10, "K":10, "A":11
    }
    cartes = list(valeurs.keys())

    def tirer_carte(main):
        carte = random.choice(cartes)
        main.append(carte)

    def total(main):
        t = sum(valeurs[c] for c in main)
        as_count = main.count("A")
        while t > 21 and as_count > 0:
            t -= 10
            as_count -= 1
        return t

    mise = int(input("Combien veux-tu miser ?\n"))
    if mise > Money:
        print("Tu n'as pas assez d'argent !")
        return Money

    joueur = []
    croupier = []

    tirer_carte(joueur)
    tirer_carte(joueur)
    tirer_carte(croupier)
    tirer_carte(croupier)

    print("Ta main :", joueur, "- total :", total(joueur))
    print("Carte du croupier :", croupier[0])

    while total(joueur) < 21:
        choix = input("Tirer ou Rester ? (T/R)\n").upper()
        if choix == "T":
            tirer_carte(joueur)
            print("Tu tires :", joueur[-1])
            print("Total :", total(joueur))
        else:
            break

    if total(joueur) > 21:
        print("Tu dépasses 21 ! Perdu.")
        return Money - mise

    print("\nTour du croupier...")
    print("Main du croupier :", croupier, "- total :", total(croupier))

    while total(croupier) < 17:
        tirer_carte(croupier)
        print("Le croupier tire :", croupier[-1])

    print("Total final du croupier :", total(croupier))

    if total(croupier) > 21 or total(joueur) > total(croupier):
        print("Tu as gagné ! +", mise, "$")
        return Money + mise
    elif total(joueur) == total(croupier):
        print("Égalité, tu récupères ta mise.")
        return Money
    else:
        print("Perdu ! -", mise, "$")
        return Money - mise



def Roulette(Money):
    print("\n=== ROULETTE ===")

    Cases = ['Vert'] + ['Rouge','Noir'] * 18 
    Cases[1::2] = ['Rouge']*18
    Cases[2::2] = ['Noir']*18

    print("Modes disponibles :")
    print("- Couleur")
    print("- 1 case")
    print("- 2 cases")
    print("- 4 cases")

    mode = input("Que choisis-tu ?\n")

    if mode == "Couleur":
        couleur = input("Rouge ou Noir ?\n")
        mise = int(input("Montant misé :\n"))

        tirage = random.randint(0, 36)

        print(f"Case tirée : {tirage} ({Cases[tirage]})")

        if Cases[tirage] == couleur:
            print("Gagné ! +", mise)
            return Money + mise
        else:
            print("Perdu ! -", mise)
            return Money - mise


    if mode == "1 case":
        case = int(input("Choisis un chiffre entre 0 et 36 :\n"))
        mise = int(input("Montant misé :\n"))

        tirage = random.randint(0, 36)
        print("Case tirée :", tirage)

        if tirage == case:
            print("Jackpot ! +", mise * 35)
            return Money + mise * 35
        else:
            print("Perdu ! -", mise)
            return Money - mise


    if mode == "2 cases":
        cases = []
        mises = []
        for i in range(2):
            cases.append(int(input(f"Case {i+1} (0-36) :\n")))
            mises.append(int(input(f"Mise {i+1} :\n")))

        total_mise = sum(mises)
        tirage = random.randint(0, 36)

        print("Case tirée :", tirage)

        for i in range(2):
            if tirage == cases[i]:
                print("Gagné ! +", mises[i] * 17)
                return Money + mises[i] * 17

        print("Perdu ! -", total_mise)
        return Money - total_mise

    if mode == "4 cases":
        cases = []
        mises = []
        for i in range(4):
            cases.append(int(input(f"Case {i+1} (0-36) :\n")))
            mises.append(int(input(f"Mise {i+1} :\n")))

        total_mise = sum(mises)
        tirage = random.randint(0, 36)

        print("Case tirée :", tirage)

        for i in range(4):
            if tirage == cases[i]:
                print("Gagné ! +", mises[i] * 8)
                return Money + mises[i] * 8

        print("Perdu ! -", total_mise)
        return Money - total_mise

    print("Mode inconnu.")
    return Money


def Join_Casino():
    Money = 1000

    print("= CASINOEUIL =")

    while True:
        print("\nTu as", Money, "$")
        print("Choisis un jeu :")
        print("- BlackJack")
        print("- Roulette")
        print("- Quitter")

        choix = input("Ton choix :\n")

        if choix == "BlackJack":
            Money = BlackJack(Money)

        elif choix == "Roulette":
            Money = Roulette(Money)

        elif choix == "Quitter":
            print("Merci d'avoir joué !")
            break

        else:
            print("Choix invalide.")


Join_Casino()
