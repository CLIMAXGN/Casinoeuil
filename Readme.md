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
- [Validations](#validations)
- [Dépannage](#dépannage)
  - [Port Déjà Utilisé](#1--port-déjà-utilisé)
  - [Base de Données Corrompue](#2--base-de-données-corrompue)
  - [Erreur Flask Non Trouvée](#3--erreur-flask-non-trouvée)
  - [Argent Négatif](#4--argent-négatif)
  - [Améliorations Ne Fonctionnent Pas](#5--améliorations-ne-fonctionnent-pas)

---

## Description

Application web de casino complète construite avec **Flask** (backend Python) et **JavaScript vanilla** (frontend). L'application offre une expérience de jeu immersive avec plusieurs jeux de casino classiques, un système innovant de **Money Clicker** pour générer des revenus, et un suivi détaillé des statistiques.

### Caractéristiques Principales:

- 5 Jeux de Casino entièrement fonctionnels
- Système Multi-Utilisateurs avec authentification sécurisée
- Money Clicker avec 4 types d'améliorations progressives
- Statistiques Complètes globales et personnelles
- Classement des Joueurs en temps réel
- Panel Admin pour gestion des utilisateurs
- Base de Données SQLite avec relations complexes
- Interface Responsive avec animations fluides
- Architecture POO avec structures de données (PILE)
- Sécurité avec hachage de mots de passe

---

## Prérequis

Avant d'exécuter ce projet, assurez-vous d'avoir installé :

| Logiciel | Version Minimale | Description |
|----------|------------------|-------------|
| **Python** | 3.7+ | Langage de programmation principal |
| **Flask** | 3.0.0+ | Framework web |
| **Flask-SQLAlchemy** | 3.1.1+ | ORM pour base de données |
| **Flask-Login** | 0.6.3+ | Gestion des sessions utilisateur |
| **Werkzeug** | 3.0.1+ | Hashage sécurisé des mots de passe |
| **pip** | Dernière version | Gestionnaire de paquets Python |
| **SQLite** | 3.x | Inclus avec Python |
| **Navigateur Web** | Version récente | Chrome, Firefox, Safari ou Edge |

---

## Installation

### Étape 1 : Cloner le Dépôt
```bash
git clone https://github.com/CLIMAXGN/Casinoeuil.git
cd casinoeuil
```

### Étape 2 : Créer un Environnement Virtuel
```bash
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Étape 3 : Installer les Dépendances
```bash
pip install -r requirements.txt
```

### Étape 4 : Vérifier la Structure des Fichiers
```
Casinoeuil/
│
├── 📄 app.py                    
├── 📄 models.py                
├── 📂 instance/            
│   └── casinoeuil.db
│
├── 📂 static/
│   ├── favicon.ico         
│   ├── script.js            
│   └── styles.css            
│
└── 📂 templates/
    ├── index.html              
    ├── login.html              
    ├── register.html            
    ├── profile.html             
    └── admin_users.html         
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

### Premiers Pas

1. Créer un compte sur /register
  Pseudo (min. 3 caractères)
  Email valide
  Mot de passe sécurisé (min. 6 caractères)
  Bonus de bienvenue : 5,000$
  
2. Se connecter sur /login

3. Jouer !
  Utilisez le Money Clicker pour générer des revenus
  Placez des paris sur les jeux de casino
  Suivez vos statistiques et votre classement

---

### Fonctionnalités

#### Pour les Joueurs

- Inscription/Connexion sécurisée
- 5,000$ de départ pour tous les nouveaux joueurs
- 5 jeux de casino avec règles authentiques
- Statistiques détaillées par jeu
- Classement mondial des meilleurs joueurs
- Historique des 20 dernières parties
- Page de profil avec données personnelles
- Système d'achievements avec 5 succès débloquables :

| Nom | Description | Récompense | Condition |
|-----|-------------|------------|-----------|
| 🎮 **Premier pas** | Joue ta première partie | 100$ | Jouer 1 partie |
| 🏆 **Gagnant** | Gagne 10 parties | 500$ | Remporter 10 victoires |
| 💰 **Millionnaire** | Atteins 10,000$ | 2,000$ | Avoir un solde ≥ 10,000$ |
| 🔥 **Série de victoires** | Gagne 5 parties d'affilée | 1,500$ | 5 victoires consécutives |
| 🍀 **Chanceux** | Gagne avec multiplicateur ×50+ | 1,000$ | Gain avec multiplicateur ≥ 50 |

#### Pour les Administrateurs

- Panel admin sur /admin/users (archibogue88 uniquement)
- Liste complète des utilisateurs
- Donner de l'argent à un joueur
- Supprimer des comptes
- Statistiques globales (argent total, moyenne, etc.)
  
---

## Contrôles & Fonctionnement

### Menu Principal

- Cartes de jeu cliquables pour lancer un jeu
- Bouton "← Back" pour revenir au menu
- Affichage en temps réel du solde et revenu passif
- Classement des joueurs en bas de page
- Profil pour voir vos statistiques détaillées

### Money Clicker

<p align="center">
  <img src="https://github.com/user-attachments/assets/e6e8a0cb-283e-488f-895b-239481e9db26" width="55%" />
</p>

**Comment jouer:**

1. **Cliquez** sur le gros bouton pour gagner de l'argent
2. **Achetez des améliorations** dans le panneau de droite

> Les prix augmentent après chaque achat selon un multiplicateur unique par amélioration.

#### 📊 Détails des Améliorations

| Amélioration | Nom | Effet | Coût initial | Multiplicateur de coût |
|--------------|-----|-------|--------------|------------------------|
| **Click** | 💪 Archibogue Power | +1 $/clic | 25$ | ×1.8 |
| **Auto** | 🤖 'Pataphysique Autoclicker | +0.5 $/s passif | 150$ | ×2.2 |
| **Factory** | 🏭 Usine à ₿itcoin | +2 $/s passif | 800$ | ×2.5 |
| **Bank** | 🎨 NFT | +8 $/s passif | 5000$ | ×3.0 |

**Formule du coût progressif :**
- Après chaque achat, le coût augmente selon le multiplicateur
- Exemple : Click coûte 25$, puis 45$, puis 81$, etc.

### Blackjack

<p align="center">
  <img src="https://github.com/user-attachments/assets/7b155565-cee2-4cbb-bff8-fc6804ed6395" width="60%" />
</p>

**Règles :**

- **But :** Se rapprocher de 21 sans dépasser
- **Multi-decks :** 1 à 8 jeux de cartes (aléatoire)
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
- Formule : `Multiplicateur = 1 + (diamants trouvés × 0.3 × bombes/5)`

### Slot Machine

<p align="center">
  <img src="https://github.com/user-attachments/assets/5880931b-1faf-4b58-b374-122925c2d932" width="60%" />
</p>

**Table des Gains (3 symboles identiques) :**

| Symbole | Paiement | Rareté |
|---------|----------|--------|
| 💎 **Diamant** | 100x | Ultra Rare |
| 7️⃣ **Sept** | 50x | Très Rare |
| 🎰 **Casino** | 20x | Rare |
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
├── 📄 models.py                
├── 📂 instance/            
│   └── casinoeuil.db
│
├── 📂 static/
│   ├── favicon.ico         
│   ├── script.js            
│   └── styles.css            
│
└── 📂 templates/
    ├── index.html              
    ├── login.html              
    ├── register.html            
    ├── profile.html             
    └── admin_users.html            
```

### Fichiers Détaillés

| Fichier | Lignes | Responsabilité |
|---------|--------|----------------|
| `app.py` | ~1000 | Logique serveur, API REST, gestion sessions |
| `models.py` | ~400 | Modèles DB (User, ClickerData, GameHistory), POO, structures PILE |
| `script.js` | ~700 | Interactions client, appels asynchrones |
| `styles.css` | ~900 | Design responsive, animations, thème |
| `index.html` | ~600 | Structure HTML, interfaces jeux |
| `X.html` | ~ | Toutes les autres pages HTML |

---

## Base de Données

### Architecture SQLite avec SQLAlchemy

Notre application utilise **SQLite** avec **SQLAlchemy** comme ORM. Voici les **6 tables principales** :

#### Tables Principales

| Table | Description | Relations |
|-------|-------------|-----------|
| **User** | Utilisateurs de l'application | 1→1 ClickerData, 1→N GameHistory |
| **ClickerData** | Données du Money Clicker | N→1 User |
| **GameHistory** | Historique des parties | N→1 User |
| **Achievement** | Succès débloquables | N↔N User |
| **user_achievements** | Table d'association | Lie User et Achievement |
| **GlobalStats** | Statistiques globales | Indépendante |

---

### Détails des Tables

#### 1. **User** (Utilisateurs)
| Colonne | Clés | Description |
|---------|------|-------------|
| `id` | PK | Identifiant unique |
| `username` | | Nom d'utilisateur |
| `email` | | Email |
| `password_hash` | | Mot de passe haché |
| `money` | | Solde du joueur |
| `created_at` | | Date de création |
| `last_login` | | Dernière connexion |

**Relations :**
- Un User a **1 seul** ClickerData
- Un User a **plusieurs** GameHistory
- Un User peut débloquer **plusieurs** Achievements

#### 2. **ClickerData** (Money Clicker)
| Colonne | Clés | Description |
|---------|------|-------------|
| `id` | PK | Identifiant unique |
| `user_id` | FK | Propriétaire (→ User) |
| `click_power` | | Gain par clic |
| `click_level` | | Niveau amélioration |
| `auto_level` | | Niveau Autoclicker (+0.5$/s) |
| `factory_level` | | Niveau Usine (+2$/s) |
| `bank_level` | | Niveau NFT (+8$/s) |
| `click_cost` | | Coût prochain upgrade |
| `auto_cost` | | Coût prochain upgrade |
| `factory_cost` | | Coût prochain upgrade |
| `bank_cost` | | Coût prochain upgrade |

**Revenu passif (calculé) :**
```python
passive_income = (auto_level × 0.5) + (factory_level × 2) + (bank_level × 8)
```

#### 3. **GameHistory** (Historique des Parties)
| Colonne | Clés | Description |
|---------|------|-------------|
| `id` | PK | Identifiant unique |
| `user_id` | FK | Joueur (→ User) |
| `game_type` | | Type : blackjack, roulette, minebomb, slots |
| `bet_amount` | | Montant parié |
| `result` | | Résultat : win, lose, draw |
| `profit` | | Profit/Perte (peut être négatif) |
| `multiplier` | | Multiplicateur de gain |
| `details` | | Infos spécifiques (ex: cartes, numéro roulette) |
| `played_at` | | Date et heure de la partie |

#### 4. **Achievement** (Succès)
| Colonne | Clés | Description |
|---------|------|-------------|
| `id` | PK | Identifiant unique |
| `name` | | Nom du succès |
| `description` | | Description |
| `icon` | | Emoji (ex: 🏆) |
| `reward` | | Récompense en $ |

**Exemples de succès :**
- "Premier pas" - Jouer sa première partie → 100$
- "Gagnant" - Gagner 10 parties → 500$
- "Millionnaire" - Atteindre 10,000$ → 2000$

#### 5. **user_achievements** (Table d'Association)
| Colonne | Clés | Description |
|---------|------|-------------|
| `user_id` | FK | ID utilisateur |
| `achievement_id` | FK | ID succès |
| `unlocked_at` | | Date de déblocage |

**Clé primaire composite :** `(user_id, achievement_id)`

#### 6. **GlobalStats** (Statistiques Globales)
| Colonne | Clés | Description |
|---------|------|-------------|
| `id` | PK | Identifiant unique |
| `stat_key` | | Clé (ex: "total_games") |
| `stat_value` | | Valeur |
| `last_updated` | | Dernière mise à jour |

---

### Relations Résumées

- **User → ClickerData** : 1 à 1 (chaque joueur a ses données clicker)
- **User → GameHistory** : 1 à N (un joueur a plusieurs parties)
- **User ↔ Achievement** : N à N (via `user_achievements`)

---

### Exemples de Données

**User :**
```json
{
  "id": 1,
  "username": "archibogue88",
  "money": 25000
}
```

**GameHistory :**
```json
{
  "game_type": "blackjack",
  "bet_amount": 100,
  "result": "win",
  "profit": 100,
  "details": {"player_total": 21, "dealer_total": 19}
}
```

---

### Programmation Orientée Objet (POO) & Structure PILE

#### Classes POO Implémentées

**Classe `GameAction`** - Représente une action de jeu individuelle :
```python
action = GameAction(
    action_type='hit',
    card={'suit': '♥', 'value': 'K'},
    total=20,
    details={'bet': 100}
)
```

**Classe `ActionStack`** - Structure de données PILE (LIFO) pour l'historique :
```python
stack = ActionStack()
stack.push(action1)  # Empiler une action
stack.push(action2)  # Empiler une autre action
last = stack.pop()   # Dépiler (retourne action2 - LIFO)
peek = stack.peek()  # Voir le sommet sans dépiler
```

**Classe `GameManager`** - Gestionnaire principal utilisant la PILE :
```python
manager = GameManager()
manager.record_action('hit', card={'suit': '♥', 'value': 'K'}, total=20)
manager.record_action('stand')
history = manager.get_action_history()  # Récupère toute la PILE
```

---

## Panel Admin

Accès : **Uniquement** ```archibogue88```

Fonctionnalités :

| Action | Endpoint | Description |
|---------|----------|--------|
| **Liste utilisateurs** | GET /admin/users | Voir tous les comptes |
| **Donner argent** | POST /admin/user/add_money/<id> | Ajouter des $ à un joueur |
| **Supprimer compte** | POST /admin/user/delete/<id> | Supprimer définitivement |

---

## Validations

Le code inclut **plusieurs validations** pour garantir l'intégrité des données et la logique correcte. (nous avons voulu en mettre un maximum pour nous assurer de la fiabilîté du code, et surtout d'assurer une experience utilisateur agréable)

#### 1- **Gestion de l'Argent**
```python
# models.py - Classe User
def add_money(self, amount):
    if amount < 0:
        raise ValueError("Le montant ne peut pas être négatif")
    self.money += amount

def remove_money(self, amount):
    if amount < 0:
        raise ValueError("Le montant ne peut pas être négatif")
    if self.money < amount:
        raise ValueError("Fonds insuffisants")
    self.money -= amount
```

#### 2- **Validation des Mises**
```python
# Blackjack, Roulette, Slots
if bet < 10:
    return jsonify({'error': 'Mise minimum : 10$'}), 400
if bet > current_user.money:
    return jsonify({'error': 'Mise trop élevée'}), 400
```

#### 3- **Validation MineBomb**
```python
if bombs < 3 or bombs > 10:
    return jsonify({'error': 'Entre 3 et 10 bombes'}), 400
```

#### 4- **Validation Inscription**
```python
if len(username) < 3:
    return jsonify({'error': 'Min 3 caractères'}), 400
if len(password) < 6:
    return jsonify({'error': 'Min 6 caractères'}), 400
```

**Total : 15+ validations** garantissant l'intégrité et la sécurité de l'application.

---

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

#### 2- Base de Données Corrompue

**Erreur :**
```
DatabaseError: database disk image is malformed
```

**Solution :**
```bash
# Supprimer le fichier et redémarrer
rm instance/casinoeuil.db
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

>  Ceci ne devrait JAMAIS arriver grâce aux validations.

#### 5- Améliorations Ne Fonctionnent Pas

**Symptômes :**
- Acheter une amélioration ne change rien
- L'argent est déduit mais pas d'effet

**Solutions :**

1. Recharger la page (`F5`)
2. Vérifier les logs serveur Flask
3. Vérifier la console navigateur (F12)
4. Reset et réessayer

---

## Credits

<p align="center">
  <strong>Fait par TeamCipo & KAYOZZ</strong><br>
  <strong>Trust us with your Entertainment!</strong>
</p>

---
