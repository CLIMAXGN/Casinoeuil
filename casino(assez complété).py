import random
from collections import deque #permet de faire des listes plus optimisées

class Blackjack:
    def __init__(self):
        self.valeurs = {
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, 
            "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11
        } #attribution d'une valeur à chacun des numéros d'un paquet de carte
        signes = ["♠", "♥", "♦", "♣"] #tout les signes d'un jeu de cartes
        cartes = [v + s for v in self.valeurs for s in signes] #on combine la valeur + le signe
        random.shuffle(cartes) #mélanger toutes les cartes aléatoirement
        self.paquet = deque(cartes) #paquet optimisé
        self.defausse = deque() #ici on met les cartes usées pour les remélanger plus tard

    def tirer(self, main):
        if len(self.paquet) < 10: #si le paquet est presque vide on remélange
            self.paquet = deque(list(self.defausse))
            self.defausse.clear()
            random.shuffle(self.paquet)
        carte = self.paquet.pop() #on prend la dernière carte du paquet
        main.append(carte) #on la met dans la main du joueur/croupier

    def total(self, main):
        t, as_count = 0, 0 #t = total, as_count = nombre d'as
        for c in main:
            v = c[:-1]
            t += self.valeurs[v] #ajoute la valeur de la carte
            if v == "A":
                as_count += 1 #on compte les as
        while t > 21 and as_count: #un as peut valoir 1 au lieu de 11
            t -= 10
            as_count -= 1
        return t

    def play(self, money):
        print("\n=== BLACKJACK ===")
        mise = int(input("Mise :\n")) #demande la mise
        if mise > money: #si t'as pas assez
            return money

        joueur, croupier = [], [] #les deux mains
        self.tirer(joueur); self.tirer(joueur) #2 cartes joueur
        self.tirer(croupier); self.tirer(croupier) #2 cartes croupier

        while self.total(joueur) < 21: #tant qu'il n'a pas dépassé
            print("Ta main", joueur, "-", self.total(joueur))
            print("Carte visible du croupier :", croupier[0])
            if input("(T/R)\n").upper() == "T": #tirer
                self.tirer(joueur)
            else: #rester
                break

        if self.total(joueur) > 21: #si t'exploses
            for c in joueur + croupier: self.defausse.append(c) #on met tout dans la défausse
            return money - mise

        while self.total(croupier) < 17: #croupier continue jusqu'à 17
            self.tirer(croupier)

        for c in joueur + croupier: self.defausse.append(c) #met les cartes usées dans la défausse

        tj, tc = self.total(joueur), self.total(croupier)
        if tc > 21 or tj > tc: #conditions de victoire
            return money + mise
        elif tj == tc: #égalité
            return money
        else: #défaite
            return money - mise

class SlotMachine:
    def __init__(self):
        self.symbols = ["🍒", "⭐", "🔔", "🍋", "💎"] #symboles de la slot

    def play(self, money):
        print("\n=== SLOT MACHINE ===")
        mise = int(input("Mise :\n"))
        if mise > money:
            return money

        r = [random.choice(self.symbols) for _ in range(3)] #3 symboles aléatoires
        print(f"[ {r[0]} | {r[1]} | {r[2]} ]") #affichage

        if r[0] == r[1] == r[2]: #3 identiques
            return money + mise * 10
        elif r[0] == r[1] or r[1] == r[2] or r[0] == r[2]: #2 identiques
            return money + mise * 2
        else: #aucun win
            return money - mise

class MineBomb:
    def __init__(self):
        self.size = 5 #grille 5x5

    def play(self, money):
        print("\n=== MINEBOMB ===")
        mise = int(input("Mise :\n"))
        if mise > money:
            return money

        mines = random.sample(range(self.size * self.size), random.randint(5, 10)) #places aléatoires des bombes
        revealed = set() #cases déjà cliquées
        mult = 1.0 #multiplicateur initial

        while True:
            idx = 0
            for _ in range(self.size): #affichage de la grille
                row = []
                for _ in range(self.size):
                    row.append("💎" if idx in revealed else "■") #diamant si déjà reveal
                    idx += 1
                print(" ".join(row))

            c = input("Case (0-24) ou C:\n").upper() #choix case ou cashout
            if c == "C":
                return money + int(mise * mult) #gagner avec multiplicateur

            c = int(c)
            if c in revealed: #ignore si déjà cliqué
                continue
            if c in mines: #boom = perdu
                return money - mise

            revealed.add(c) #révéler la case
            mult += 0.25 #plus tu cliques plus le multiplicateur augmente

class Clicker:
    def __init__(self):
        self.argent = 0 #argent du clicker
        self.gain = 1 #gain par clic

    def play(self):
        print("\n=== CLICKER ===")
        while True:
            print(f"Argent actuel : {self.argent}")
            action = input("Tape 'C' pour cliquer, 'B' pour acheter multiplicateur (10€), 'Q' pour quitter : ").upper()
            if action == "C":
                self.argent += self.gain #ajoute le gain à l'argent du clicker
                print(f"Tu gagnes {self.gain}€ !")
            elif action == "B":
                if self.argent >= 10: #si assez d'argent
                    self.argent -= 10 #déduit 10€
                    self.gain += 1 #augmente le gain par clic
                    print(f"Multiplicateur acheté ! Chaque clic rapporte maintenant {self.gain}€")
                else:
                    print("Pas assez d'argent pour acheter le multiplicateur.")
            elif action == "Q": #quitter le clicker
                print(f"Tu quittes le clicker avec {self.argent}€")
                return self.argent #retourne les gains au casino
            else:
                print("Commande inconnue.")

class Casino:
    def __init__(self):
        self.money = 1000 #argent de base
        self.blackjack = Blackjack() #initialiser les jeux
        self.slot = SlotMachine()
        self.mine = MineBomb()
        self.clicker = Clicker() #initialiser le clicker

    def run(self):
        print("= CASINO =")
        while True:
            print("\nArgent :", self.money)
            print("- BlackJack")
            print("- Slot")
            print("- MineBomb")
            print("- Clicker") #option clicker
            print("- Quitter")
            c = input().lower() #choix du jeu

            if c == "blackjack":
                self.money = self.blackjack.play(self.money)
            elif c == "slot":
                self.money = self.slot.play(self.money)
            elif c == "minebomb":
                self.money = self.mine.play(self.money)
            elif c == "clicker":
                self.money += self.clicker.play() #ajoute les gains du clicker à l'argent principal
            elif c == "quitter":
                break #sortir

