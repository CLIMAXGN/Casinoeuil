<p align="center">
  <img src="https://github.com/user-attachments/assets/d29729d4-da3d-4b22-a951-cbc7fc0d02ca" width="100%" />
</p>

<h1 align="center">The ONLY Casino Where You Can't Lose Money</h1>

<p align="center">
  <strong>Bienvenue dans le casino le plus injuste jamais créé — car les probabilités sont TOUJOURS de votre côté.</strong>
</p>

---

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Edition-CLIMAX-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Engine-Python-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Flask-2.0+-black?style=for-the-badge&logo=flask" />
</p>

---

## Table des Matières


- [Description](#description)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Lancement du Projet](#lancement-du-projet)
- [Contrôles & Fonctionnement](#contrôles--fonctionnement)
  - [Menu Principal](#menu-principal)
  - [Money Clicker](#money-clicker)
  - [Blackjack](#blackjack)
  - [Roulette](#roulette)
  - [MineBomb](#minebomb)
  - [Slot Machine](#slot-machine)
- [Structure du Projet](#structure-du-projet)
  - [Fichiers Détaillés](#fichiers-détaillés)
- [Base de Données](#base-de-données)
- [Assertions & Tests](#assertions--tests)
  - [Validation des Statistiques](#1-validation-des-statistiques)
  - [Gestion de l'Argent](#2-gestion-de-largent)
  - [Système Clicker](#3-système-clicker)
  - [Blackjack](#4-blackjack)
  - [Roulette](#5-roulette)
  - [MineBomb](#6-minebomb)
  - [Slot Machine](#7-slot-machine)
- [Dépannage](#dépannage)
  - [Port Déjà Utilisé](#1-port-déjà-utilisé)
  - [Fichier de Statistiques Corrompu](#2-fichier-de-statistiques-corrompu)
  - [Erreur Flask Non Trouvée](#3-erreur-flask-non-trouvée)
  - [Argent Négatif](#4-argent-négatif)
  - [Améliorations Ne Fonctionnent Pas](#5-améliorations-ne-fonctionnent-pas)

---

## Description

Application web de casino complète construite avec **Flask** (backend Python) et **JavaScript vanilla** (frontend). L'application offre une expérience de jeu immersive avec plusieurs jeux de casino classiques, un système innovant de **Money Clicker** pour générer des revenus, et un suivi détaillé des statistiques.

### Caractéristiques Principales:

- **5 Jeux de Casino** entièrement fonctionnels
- **Money Clicker** avec 4 types d'améliorations progressives
- **Statistiques Globales** et par jeu en temps réel
- **Persistance des Données** entre les sessions
- **Interface Responsive** avec animations fluides
- **Système d'Assertions** complet pour la fiabilité

---

## Prérequis

Avant d'exécuter ce projet, assurez-vous d'avoir installé :

| Logiciel | Version Minimale | Description |
|----------|------------------|-------------|
| **Python** | 3.7+ | Langage de programmation principal |
| **pip** | Dernière version | Gestionnaire de paquets Python |
| **Navigateur Web** | Version récente | Chrome, Firefox, Safari ou Edge |

---

## Installation

### Étape 1 : Cloner le Dépôt
```bash
git clone https://github.com/votre-nom/casino-web-app.git
cd casino-web-app
```

### Étape 2 : Installer les Dépendances
```bash
pip install flask
```

### Étape 3 : Vérifier la Structure des Fichiers
```
Casinoeuil/
│
├── 📄 app.py                     
│
├── 📊 casino_stats.json           
│
├── 📂 static/
│   ├── favicon.ico 
│   ├── script.js
│   └── styles.css
│
└── 📂 templates/
    └── index.html   
```

---

## Lancement du Projet

### Démarrer le Serveur Flask
```bash
python app.py
```

### Accéder à l'Application

Ouvrez votre navigateur et naviguez vers :
```
http://localhost:5000
```

### Commencer à Jouer

1. **Vous démarrez avec 0$**
2. **Utilisez le Money Clicker** pour générer des revenus
3. **Placez des paris** sur les différents jeux de casino
4. **Suivez votre progression** avec les statistiques complètes

> **Astuce :** Investissez d'abord dans le Money Clicker pour générer un revenu passif avant de jouer aux jeux de casino !

---

## Contrôles & Fonctionnement

### Menu Principal

- **Cliquez sur une carte de jeu** pour accéder au jeu
- **Bouton "Back to Menu"** pour revenir au menu principal (⬅️)
- **Bouton "Reset Game"** pour réinitialiser votre argent et améliorations (🔄)
- **Affichage du solde** et revenu passif en haut de l'écran

### Money Clicker

<p align="center">
  <img src="https://github.com/user-attachments/assets/e6e8a0cb-283e-488f-895b-239481e9db26" width="55%" />
</p>

**Comment jouer:**

1. **Cliquez** sur le gros bouton pour gagner de l'argent
2. **Achetez des améliorations** dans le panneau de droite

> Les prix augmentent après chaque achat selon un multiplicateur unique par amélioration.

### Blackjack

<p align="center">
  <img src="https://github.com/user-attachments/assets/7b155565-cee2-4cbb-bff8-fc6804ed6395" width="60%" />
</p>

**Règles :**

- **But :** Se rapprocher de 21 sans dépasser
- **Multi-decks :** 4 à 8 jeux de cartes (aléatoire)
- **Paiement :** 2x votre mise en cas de victoire
- **Mise minimale :** 10$

**Contrôles :**

1. Entrez votre mise
2. Cliquez sur **"Start Game"**
3. **"Hit"** pour tirer une carte
4. **"Stand"** pour arrêter et laisser le croupier jouer

### Roulette

<p align="center">
  <img src="https://github.com/user-attachments/assets/5e8038c3-76ec-4d77-b6f3-1c1eec3bd880" width="60%" />
</p>

**Modes de jeu :**

| Mode | Options | Paiement |
|------|---------|----------|
| 🎨 **Couleur** | Rouge ou Noir | 2x |
| 🔢 **Numéro** | 0 à 36 | 36x |

**Comment jouer :**

1. Choisissez le **mode** (Couleur ou Numéro)
2. Sélectionnez votre **choix**
3. Entrez votre **mise** (minimum 10$)
4. Cliquez sur **"Spin"** pour lancer la roulette

### MineBomb

<p align="center">
  <img src="https://github.com/user-attachments/assets/e5c6692e-15e3-4d4e-8a13-759c310b46f6" width="60%" />
</p>

**Principe :**

- Grille **5x5** (25 cases)
- Choisissez **3 à 10 bombes**
- Révélez des diamants pour augmenter le **multiplicateur**
- **Cashout** avant de toucher une bombe !

**Stratégie :**

- **Peu de bombes** = Gains faibles mais sûrs
- **Beaucoup de bombes** = Multiplicateur élevé mais risqué
- Formule : `Multiplicateur de base = 0.2 + (bombes × 0.05)`

### Slot Machine

<p align="center">
  <img src="https://github.com/user-attachments/assets/5880931b-1faf-4b58-b374-122925c2d932" width="60%" />
</p>

**Table des Gains (3 symboles identiques) :**

| Symbole | Paiement | Rareté |
|---------|----------|--------|
| 💎 **Diamant** | 100x | Ultra Rare |
| 7️⃣ **Sept** | 50x | Très Rare |
| 🍉 **Pastèque** | 20x | Rare |
| 🍋 **Citron** | 15x | Peu Commun |
| 🍊 **Orange** | 12x | Commun |
| 🍇 **Raisin** | 10x | Très Commun |

**Bonus :** 2 symboles identiques = **2x** votre mise

---

## Structure du Projet
```
Casinoeuil/
│
├── 📄 app.py                     
│
├── 📊 casino_stats.json           
│
├── 📂 static/
│   ├── favicon.ico 
│   ├── script.js
│   └── styles.css
│
└── 📂 templates/
    └── index.html           
```

### Fichiers Détaillés

| Fichier | Lignes | Responsabilité |
|---------|--------|----------------|
| `app.py` | ~800 | Logique serveur, API REST, gestion sessions |
| `script.js` | ~700 | Interactions client, appels asynchrones |
| `styles.css` | ~900 | Design responsive, animations, thème |
| `index.html` | ~400 | Structure HTML, interfaces jeux |

---

## Base de Données

### Stockage en Session (Flask Session)

**Données utilisateur (à titre d'exemple) :**
```python
session = {
    'money': 1250,                    # Solde actuel
    'clicker': {
        'clickPower': 5,              # Puissance par clic
        'clickLevel': 5,              # Niveau d'amélioration
        'autoLevel': 3,               # Niveau Auto-Clicker
        'factoryLevel': 2,            # Niveau Factory
        'bankLevel': 1,               # Niveau Bank
        'clickCost': 76,              # Coût prochaine amélioration
        'autoCost': 180,
        'factoryCost': 800,
        'bankCost': 2500
    },
    'bj_*': {...},                    # État actif Blackjack
    'mb_*': {...}                     # État actif MineBomb
}
```

### Statistiques Globales (Les statistiques présentées ci-dessous ne sont pas représentatives mais utilisées uniquement à titre d'exemple)

**Données persistantes partagées :**
```json
{
  "totalGames": 44,
  "totalWins": 8,
  "totalLosses": 35,
  "biggestWin": 100,
  "biggestLoss": 1000,
  "totalWagered": 4384,
  "totalWinnings": 420,
  "blackjack": {
    "games": 10,
    "wins": 4,
    "wagered": 500,
    "won": 200
  },
  "roulette": {
    "games": 7,
    "wins": 3,
    "wagered": 484,
    "won": 120
  },
  "minebomb": {
    "games": 11,
    "wins": 0,
    "wagered": 2600,
    "won": 0
  },
  "slots": {
    "games": 16,
    "wins": 1,
    "wagered": 800,
    "won": 100
  }
}
```

**Champs calculés automatiquement :**

- **Taux de victoire** : `(totalWins / totalGames) × 100`
- **Profit net** : `totalWinnings - totalWagered`
- **Taux par jeu** : Calculé individuellement

---

## Assertions & Tests

Le code inclut **+50 assertions** pour garantir l'intégrité des données et la logique correcte. (nous avons voulu en mettre un maximum pour nous assurer de la fiabilîté du code, et surtout d'assurer une experience utilisateur agréable)

#### 1- **Validation des Statistiques**
```python
assert isinstance(stats, dict), "Stats doit être un dictionnaire"
assert stats['totalGames'] >= 0, "totalGames ne peut pas être négatif"
assert stats['totalWins'] <= stats['totalGames'], "totalWins ≤ totalGames"
assert stats['biggestWin'] >= 0, "biggestWin ne peut pas être négatif"
```

#### 2- **Gestion de l'Argent**
```python
assert money >= 0, "L'argent ne peut pas être négatif"
assert bet > 0, "La mise doit être positive"
assert session['money'] == money_before - cost, "Transaction exacte"
```

#### 3- **Système Clicker**
```python
assert clickPower > 0, "clickPower doit être positif"
assert autoLevel >= 0, "autoLevel ne peut pas être négatif"
assert cost > 0, "Le coût doit être positif"
assert passive >= 0, "Le revenu passif ne peut pas être négatif"
```

#### 4- **Blackjack**
```python
assert len(deck) == 52 * num_decks, "Deck size correct"
assert len(player_hand) == 2, "Main initiale = 2 cartes"
assert card['value'] in card_values, "Valeur de carte valide"
assert total >= 0, "Total ne peut pas être négatif"
```

#### 5- **Roulette**
```python
assert 0 <= number <= 36, "Numéro entre 0 et 36"
assert color in ['Red', 'Black', 'Green'], "Couleur valide"
assert mode in ['color', 'number'], "Mode invalide"
```

#### 6- **MineBomb**
```python
assert len(grid) == 25, "Grille 5x5 = 25 cases"
assert 3 <= bombs <= 10, "Bombes entre 3 et 10"
assert grid.count('bomb') == bombs, "Nombre de bombes exact"
assert multiplier > 0, "Multiplicateur positif"
assert 0 <= pos < 25, "Position valide"
```

#### 7- **Slot Machine**
```python
assert len(reels) == 3, "3 rouleaux exactement"
assert len(weighted_symbols) == 80, "80 symboles pondérés"
assert multiplier > 0, "Multiplicateur positif pour gains"
```

## Dépannage

### Problèmes Courants:

#### 1- Port Déjà Utilisé

**Erreur :**
```
Address already in use: Port 5000
```

**Solution :**
```bash
# macOS/Linux
lsof -i :5000
kill -9 <PID>

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Ou changer le port dans app.py
app.run(port=5001)
```

#### 2- Fichier de Statistiques Corrompu

**Erreur :**
```
JSONDecodeError: Expecting value
```

**Solution :**
```bash
# Supprimer le fichier et redémarrer
rm casino_stats.json
python app.py
```

Le fichier sera recréé automatiquement avec les valeurs par défaut.

#### 3- Erreur Flask Non Trouvée

**Erreur :**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution :**
```bash
pip install flask

# Ou créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install flask
```

#### 4- Argent Négatif

**Symptômes :**
- Solde affiche -100$

**Solution :**

>  Ceci ne devrait JAMAIS arriver grâce aux assertions.

#### 5- Améliorations Ne Fonctionnent Pas

**Symptômes :**
- Acheter une amélioration ne change rien
- L'argent est déduit mais pas d'effet

**Solutions :**

1. Recharger la page (`F5`)
2. Vérifier les logs serveur Flask
3. Vérifier la console navigateur (F12)
4. Reset et réessayer


## Credits

<p align="center">
  <strong>Fait par TeamCipo & KAYOZZ</strong><br>
  <strong>Trust us with your Entertainement!</strong>
</p>

---
