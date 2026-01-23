from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, ClickerData, GameHistory, Achievement, GameManager, Clan, clan_members
from datetime import datetime, timedelta
import random
import os
import json

# Créer l'app Flask AVANT d'importer les modèles
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fortnite_en_2020_ct_quelque_chose')

# Configuration de la base de données
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Production (Render avec Neon PostgreSQL)
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql+psycopg2://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
else:
    # Local (SQLite)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///casinoeuil.db'

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db, User, ClickerData, GameHistory, Achievement, GameManager

# Instance globale du gestionnaire (POO + PILE)
game_manager = GameManager()

# Initialisation
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ============================================
# GESTIONNAIRE D'ERREURS GLOBAL
# ============================================

@app.errorhandler(AssertionError)
def handle_assertion_error(error):
    """Gestionnaire global pour les AssertionError"""
    return jsonify({'error': str(error)}), 400

@app.errorhandler(403)
def handle_forbidden(error):
    """Gestionnaire pour les erreurs 403"""
    return jsonify({'error': 'Accès refusé'}), 403

@app.errorhandler(404)
def handle_not_found(error):
    """Gestionnaire pour les erreurs 404"""
    return jsonify({'error': 'Ressource non trouvée'}), 404

# ============================================
# ROUTES D'AUTHENTIFICATION
# ============================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Inscription"""
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # ASSERTIONS
        assert username and email and password, "Tous les champs sont requis"
        assert len(username) >= 3, "Le nom d'utilisateur doit avoir au moins 3 caractères"
        assert len(password) >= 6, "Le mot de passe doit avoir au moins 6 caractères"
        assert not User.query.filter_by(username=username).first(), "Nom d'utilisateur déjà pris"
        assert not User.query.filter_by(email=email).first(), "Email déjà utilisé"
        
        user = User(username=username, email=email, money=5000)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        clicker_data = ClickerData(user_id=user.id)
        db.session.add(clicker_data)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Compte créé avec succès!'})
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Connexion"""
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        # ASSERTIONS
        assert user, "Utilisateur non trouvé"
        assert user.check_password(password), "Mot de passe incorrect"
        
        login_user(user)
        user.last_login = datetime.utcnow()
        user.last_ip = request.remote_addr
        db.session.commit()
        return jsonify({'success': True})
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Déconnexion"""
    logout_user()
    return redirect(url_for('login'))

# ============================================
# ROUTES PRINCIPALES
# ============================================

@app.route('/')
@login_required
def index():
    """Page principale"""
    return render_template('index.html', money=current_user.money)

@app.route('/profile')
@login_required
def profile():
    """Page de profil utilisateur"""
    return render_template('profile.html')

@app.route('/admin/users')
@login_required
def admin_users():
    """Page admin pour voir tous les utilisateurs"""
    
    # ASSERTION
    assert current_user.username == 'archibogue88', "Accès refusé - Vous n'êtes pas admin"
    
    all_users = User.query.order_by(User.money.desc()).all()
    
    users_data = []
    for user in all_users:
        users_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'money': user.money,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M'),
            'last_login': user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else 'Jamais',
            'last_ip': user.last_ip,
            'is_banned': user.is_banned,
            'ban_reason': user.ban_reason,
        })
    
    return render_template('admin_users.html', users=users_data)

# Routes admin
@app.route('/admin/user/delete/<int:user_id>', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    # ASSERTIONS
    assert current_user.username == 'archibogue88', "Accès refusé"
    assert user_id != current_user.id, "Tu ne peux pas te supprimer toi-même !"
    
    user = User.query.get(user_id)
    assert user, "Utilisateur non trouvé"
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'Utilisateur {username} supprimé'})

@app.route('/admin/user/add_money/<int:user_id>', methods=['POST'])
@login_required
def admin_add_money(user_id):
    # ASSERTIONS
    assert current_user.username == 'archibogue88', "Accès refusé"
    
    data = request.json
    amount = data.get('amount', 0)
    
    assert amount > 0, "Montant invalide"
    
    user = User.query.get(user_id)
    assert user, "Utilisateur non trouvé"
    
    user.money += int(amount)
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': f'{amount}$ ajoutés à {user.username}',
        'new_money': user.money
    })

@app.route('/admin/user/ban/<int:user_id>', methods=['POST'])
@login_required
def admin_ban_user(user_id):
    assert current_user.username == 'archibogue88', "Accès refusé"
    
    data = request.json
    reason = data.get('reason', 'Aucune raison')
    
    user = User.query.get(user_id)
    assert user, "Utilisateur non trouvé"
    assert user.username != 'archibogue88', "Tu ne peux pas te bannir"
    
    user.is_banned = True
    user.ban_reason = reason
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'{user.username} banni'})

@app.route('/admin/user/unban/<int:user_id>', methods=['POST'])
@login_required
def admin_unban_user(user_id):
    assert current_user.username == 'archibogue88', "Accès refusé"
    
    user = User.query.get(user_id)
    assert user, "Utilisateur non trouvé"
    
    user.is_banned = False
    user.ban_reason = ''
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'{user.username} débanni'})

@app.route('/admin/user/set_money/<int:user_id>', methods=['POST'])
@login_required
def admin_set_money(user_id):
    assert current_user.username == 'archibogue88', "Accès refusé"
    
    data = request.json
    amount = int(data.get('amount', 0))
    
    assert amount >= 0, "Montant invalide"
    
    user = User.query.get(user_id)
    assert user, "Utilisateur non trouvé"
    
    user.money = amount
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'Argent de {user.username} défini à {amount}$', 'new_money': user.money})

# ============================================
# STATISTIQUES ET LEADERBOARD
# ============================================

@app.route('/api/get_stats')
@login_required
def get_stats():
    """Récupère les statistiques globales"""
    stats = get_global_stats()
    return jsonify(stats)

@app.route('/api/user_stats')
@login_required
def user_stats():
    """Statistiques personnelles du joueur"""
    return jsonify(current_user.get_stats())

@app.route('/api/user_achievements')
@login_required
def user_achievements():
    """Récupère les achievements du joueur"""
    # Tous les achievements disponibles
    all_achievements = Achievement.query.all()
    
    # Achievements débloqués par l'utilisateur
    unlocked_ids = [ach.id for ach in current_user.achievements]
    
    achievements_data = []
    for ach in all_achievements:
        achievements_data.append({
            'id': ach.id,
            'name': ach.name,
            'description': ach.description,
            'icon': ach.icon,
            'reward': ach.reward,
            'unlocked': ach.id in unlocked_ids
        })
    
    return jsonify(achievements_data)

@app.route('/api/leaderboard')
@login_required
def leaderboard():
    """Classement des joueurs par argent"""
    top_players = User.query.order_by(User.money.desc()).limit(100).all()
    
    leaderboard_data = []
    for rank, player in enumerate(top_players, start=1):
        games = GameHistory.query.filter_by(user_id=player.id).all()
        total_games = len(games)
        total_wins = sum(1 for g in games if g.result == 'win')
        win_rate = round((total_wins / total_games * 100), 1) if total_games > 0 else 0
        
        leaderboard_data.append({
            'rank': rank,
            'username': player.username,
            'money': player.money,
            'total_games': total_games,
            'total_wins': total_wins,
            'win_rate': win_rate,
            'is_current_user': player.id == current_user.id
        })
    
    return jsonify(leaderboard_data)

def get_global_stats():
    """Calcule les stats globales depuis la DB"""
    all_games = GameHistory.query.all()
    
    total_games = len(all_games)
    total_wins = sum(1 for g in all_games if g.result == 'win')
    total_losses = sum(1 for g in all_games if g.result == 'lose')
    total_wagered = sum(g.bet_amount for g in all_games)
    total_winnings = sum(g.profit for g in all_games if g.profit > 0)
    
    biggest_win_game = GameHistory.query.filter(GameHistory.profit > 0).order_by(GameHistory.profit.desc()).first()
    biggest_loss_game = GameHistory.query.filter(GameHistory.profit < 0).order_by(GameHistory.profit.asc()).first()
    
    def get_game_stats(game_type):
        games = GameHistory.query.filter_by(game_type=game_type).all()
        wins = sum(1 for g in games if g.result == 'win')
        wagered = sum(g.bet_amount for g in games)
        won = sum(g.profit for g in games if g.profit > 0)
        return {
            'games': len(games),
            'wins': wins,
            'wagered': wagered,
            'won': won
        }
    
    return {
        'totalGames': total_games,
        'totalWins': total_wins,
        'totalLosses': total_losses,
        'biggestWin': biggest_win_game.profit if biggest_win_game else 0,
        'biggestLoss': abs(biggest_loss_game.profit) if biggest_loss_game else 0,
        'totalWagered': total_wagered,
        'totalWinnings': total_winnings,
        'blackjack': get_game_stats('blackjack'),
        'roulette': get_game_stats('roulette'),
        'minebomb': get_game_stats('minebomb'),
        'slots': get_game_stats('slots'),
        'plinko': get_game_stats('plinko')  # PLINKO
    }

def check_and_unlock_achievements(user):
    """Vérifie et débloque les achievements du joueur"""
    stats = user.get_stats()
    unlocked_ids = [ach.id for ach in user.achievements]
    newly_unlocked = []
    
    # Premier pas - Jouer sa première partie
    ach1 = Achievement.query.filter_by(name='Premier pas').first()
    if ach1 and ach1.id not in unlocked_ids and stats['total_games'] >= 1:
        user.achievements.append(ach1)
        user.add_money(ach1.reward)
        newly_unlocked.append({'name': ach1.name, 'reward': ach1.reward})
    
    # Gagnant - Gagner 10 parties
    ach2 = Achievement.query.filter_by(name='Gagnant').first()
    if ach2 and ach2.id not in unlocked_ids and stats['total_wins'] >= 10:
        user.achievements.append(ach2)
        user.add_money(ach2.reward)
        newly_unlocked.append({'name': ach2.name, 'reward': ach2.reward})
    
    # Millionnaire - Atteindre 10,000$
    ach3 = Achievement.query.filter_by(name='Millionnaire').first()
    if ach3 and ach3.id not in unlocked_ids and user.money >= 10000:
        user.achievements.append(ach3)
        user.add_money(ach3.reward)
        newly_unlocked.append({'name': ach3.name, 'reward': ach3.reward})
    
    # Série de victoires - 5 victoires d'affilée (vérifie les 5 dernières parties)
    recent_games = GameHistory.query.filter_by(user_id=user.id)\
        .order_by(GameHistory.played_at.desc()).limit(5).all()
    if len(recent_games) == 5 and all(g.result == 'win' for g in recent_games):
        ach4 = Achievement.query.filter_by(name='Série de victoires').first()
        if ach4 and ach4.id not in unlocked_ids:
            user.achievements.append(ach4)
            user.add_money(ach4.reward)
            newly_unlocked.append({'name': ach4.name, 'reward': ach4.reward})
    
    # Chanceux - Gagner avec multiplicateur x50+
    big_win = GameHistory.query.filter_by(user_id=user.id)\
        .filter(GameHistory.multiplier >= 50).first()
    if big_win:
        ach5 = Achievement.query.filter_by(name='Chanceux').first()
        if ach5 and ach5.id not in unlocked_ids:
            user.achievements.append(ach5)
            user.add_money(ach5.reward)
            newly_unlocked.append({'name': ach5.name, 'reward': ach5.reward})
    
    if newly_unlocked:
        db.session.commit()
    
    return newly_unlocked

# ============================================
# MONEY CLICKER
# ============================================

@app.route('/api/clicker/get_data')
@login_required
def clicker_get_data():
    """Récupère les données du clicker"""
    clicker = current_user.clicker_data
    
    if not clicker:
        clicker = ClickerData(user_id=current_user.id)
        db.session.add(clicker)
        db.session.commit()
    
    return jsonify({
        'clickPower': clicker.click_power,
        'clickLevel': clicker.click_level,
        'autoLevel': clicker.auto_level,
        'factoryLevel': clicker.factory_level,
        'bankLevel': clicker.bank_level,
        'clickCost': clicker.click_cost,
        'autoCost': clicker.auto_cost,
        'factoryCost': clicker.factory_cost,
        'bankCost': clicker.bank_cost,
        'passiveIncome': clicker.passive_income
    })

@app.route('/api/clicker/click', methods=['POST'])
@login_required
def clicker_click():
    """Gère le clic"""
    clicker = current_user.clicker_data
    current_user.add_money(clicker.click_power)
    
    clicker.total_clicks += 1
    clicker.total_earned += clicker.click_power
    db.session.commit()
    
    return jsonify({'money': current_user.money})

@app.route('/api/clicker/upgrade', methods=['POST'])
@login_required
def clicker_upgrade():
    """Achète une amélioration"""
    data = request.json
    upgrade_type = data.get('type')
    
    clicker = current_user.clicker_data
    
    if upgrade_type == 'click':
        cost = clicker.click_cost
        assert current_user.money >= cost, "Pas assez d'argent"
        
        current_user.remove_money(cost)
        clicker.click_power += 1
        clicker.click_level += 1
        clicker.click_cost = int(cost * 1.8)
    
    elif upgrade_type == 'auto':
        cost = clicker.auto_cost
        assert current_user.money >= cost, "Pas assez d'argent"
        
        current_user.remove_money(cost)
        clicker.auto_level += 1
        clicker.auto_cost = int(cost * 2.2)
    
    elif upgrade_type == 'factory':
        cost = clicker.factory_cost
        assert current_user.money >= cost, "Pas assez d'argent"
        
        current_user.remove_money(cost)
        clicker.factory_level += 1
        clicker.factory_cost = int(cost * 2.5)
    
    elif upgrade_type == 'bank':
        cost = clicker.bank_cost
        assert current_user.money >= cost, "Pas assez d'argent"
        
        current_user.remove_money(cost)
        clicker.bank_level += 1
        clicker.bank_cost = int(cost * 3.0)
    
    db.session.commit()
    
    return jsonify({
        'money': current_user.money,
        'clickPower': clicker.click_power,
        'clickLevel': clicker.click_level,
        'autoLevel': clicker.auto_level,
        'factoryLevel': clicker.factory_level,
        'bankLevel': clicker.bank_level,
        'clickCost': clicker.click_cost,
        'autoCost': clicker.auto_cost,
        'factoryCost': clicker.factory_cost,
        'bankCost': clicker.bank_cost,
        'passiveIncome': clicker.passive_income
    })

@app.route('/api/clicker/passive', methods=['POST'])
@login_required
def clicker_passive():
    """Revenu passif"""
    clicker = current_user.clicker_data
    passive = clicker.passive_income
    
    if passive > 0:
        current_user.add_money(passive)
        clicker.total_earned += passive
        db.session.commit()
    
    return jsonify({'money': current_user.money})

# ============================================
# BLACKJACK
# ============================================

def create_deck():
    """Crée un jeu de 52 cartes"""
    suits = ['♥', '♦', '♣', '♠']
    values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    return [{'suit': suit, 'value': value} for suit in suits for value in values]

def card_value(card):
    """Retourne la valeur d'une carte"""
    assert 'value' in card, "La carte doit avoir une valeur"
    
    if card['value'] in ['J', 'Q', 'K']:
        return 10
    elif card['value'] == 'A':
        return 11
    else:
        return int(card['value'])

def hand_total(hand):
    """Calcule le total d'une main"""
    assert isinstance(hand, list), "La main doit être une liste"
    assert len(hand) > 0, "La main ne peut pas être vide"
    
    total = sum(card_value(card) for card in hand)
    aces = sum(1 for card in hand if card['value'] == 'A')
    
    while total > 21 and aces:
        total -= 10
        aces -= 1
    
    return total

@app.route('/api/blackjack/start', methods=['POST'])
@login_required
def blackjack_start():
    """Démarre une partie de Blackjack avec deck persistant"""
    data = request.json
    bet = int(data.get('bet', 50))
    
    # ASSERTIONS
    assert bet >= 10, "Mise minimum : 10$"
    assert bet <= current_user.money, "Mise trop élevée"
    
    # Retirer l'argent
    current_user.remove_money(bet)
    
    # AMÉLIORATION : Gestion persistante du deck
    blackjack_session = session.get('blackjack_session', {})
    
    # Si pas de session active OU moins de 20% du deck restant, créer nouveau deck
    if not blackjack_session or len(blackjack_session.get('deck', [])) < (blackjack_session.get('total_cards', 0) * 0.2):
        num_decks = 6  # Standard casino (peut être 4, 6 ou 8)
        deck = create_deck() * num_decks
        random.shuffle(deck)
        
        blackjack_session = {
            'deck': deck,
            'num_decks': num_decks,
            'total_cards': len(deck),
            'cards_dealt': 0
        }
    else:
        # Utiliser le deck existant
        deck = blackjack_session['deck']
        num_decks = blackjack_session['num_decks']
    
    # Distribuer 2 cartes au joueur et au croupier
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]
    
    # Mettre à jour le nombre de cartes distribuées
    blackjack_session['cards_dealt'] += 4
    blackjack_session['deck'] = deck
    
    # Calculer les totaux
    player_total = hand_total(player_hand)
    dealer_total = hand_total(dealer_hand)
    
    # Stocker la partie en cours
    session['blackjack'] = {
        'bet': bet,
        'player_hand': player_hand,
        'dealer_hand': dealer_hand
    }
    
    # Stocker la session de deck
    session['blackjack_session'] = blackjack_session
    
    # Calculer combien de cartes restent
    cards_remaining = len(deck)
    deck_percentage = (cards_remaining / blackjack_session['total_cards']) * 100
    
    # ENREGISTRER DANS LA PILE (POO)
    game_manager.start_game(current_user.id, 'blackjack', bet)
    game_manager.record_action('start', details={
        'bet': bet, 
        'num_decks': num_decks,
        'cards_remaining': cards_remaining
    })
    game_manager.record_action('deal_player', card=player_hand[0], total=card_value(player_hand[0]))
    game_manager.record_action('deal_player', card=player_hand[1], total=player_total)
    game_manager.record_action('deal_dealer', card=dealer_hand[0], total=card_value(dealer_hand[0]))
    
    return jsonify({
        'money': current_user.money,
        'player_hand': player_hand,
        'dealer_hand': dealer_hand,
        'player_total': player_total,
        'dealer_total': dealer_total,
        'num_decks': num_decks,
        'cards_remaining': cards_remaining,
        'deck_percentage': round(deck_percentage, 1)
    })


# Modifie aussi hit() et stand() pour utiliser le deck de session :

@app.route('/api/blackjack/hit', methods=['POST'])
@login_required
def blackjack_hit():
    """Tire une carte supplémentaire"""
    game = session.get('blackjack')
    assert game, "Pas de partie en cours"
    
    blackjack_session = session.get('blackjack_session', {})
    deck = blackjack_session.get('deck', [])
    
    assert len(deck) > 0, "Plus de cartes dans le deck"
    
    # Tirer une carte
    card = deck.pop()
    game['player_hand'].append(card)
    player_total = hand_total(game['player_hand'])
    
    # Mettre à jour
    blackjack_session['deck'] = deck
    blackjack_session['cards_dealt'] += 1
    session['blackjack'] = game
    session['blackjack_session'] = blackjack_session
    
    # ENREGISTRER DANS LA PILE
    game_manager.record_action('hit', card=card, total=player_total)
    
    # Vérifier si bust
    busted = player_total > 21
    
    return jsonify({
        'player_hand': game['player_hand'],
        'player_total': player_total,
        'busted': busted,
        'cards_remaining': len(deck)
    })


@app.route('/api/blackjack/stand', methods=['POST'])
@login_required
def blackjack_stand():
    game = session.get('blackjack')
    assert game, "Pas de partie en cours"
    
    blackjack_session = session.get('blackjack_session', {})
    deck = blackjack_session.get('deck', [])
    
    #ENREGISTRER L'ACTION STAND
    player_total = hand_total(game['player_hand'])
    game_manager.record_action('stand', total=player_total)
    
    #Dealer tire jusqu'à 17
    while hand_total(game['dealer_hand']) < 17:
        card = deck.pop()
        game['dealer_hand'].append(card)
        blackjack_session['cards_dealt'] += 1
        # ENREGISTRER CHAQUE CARTE DU DEALER
        game_manager.record_action('dealer_hit', card=card, total=hand_total(game['dealer_hand']))
    
    #Mettre à jour le deck
    blackjack_session['deck'] = deck
    session['blackjack_session'] = blackjack_session
    
    player_total = hand_total(game['player_hand'])
    dealer_total = hand_total(game['dealer_hand'])
    bet = game['bet']
    
    #Déterminer le résultat
    if player_total > 21:
        result = 'lose'
        profit = -bet
        result_message = 'Vous avez perdu ! (Bust)'
    elif dealer_total > 21 or player_total > dealer_total:
        result = 'win'
        profit = bet
        result_message = 'Vous avez gagné !'
    elif player_total < dealer_total:
        result = 'lose'
        profit = -bet
        result_message = 'Vous avez perdu !'
    else:
        result = 'draw'
        profit = 0
        result_message = 'Égalité !'
    
    #Mettre à jour l'argent
    if result == 'win':
        current_user.add_money(bet * 2)
    elif result == 'draw':
        current_user.add_money(bet)
    
    #Sauvegarder l'historique
    history = GameHistory(
        user_id=current_user.id,
        game_type='blackjack',
        bet_amount=bet,
        result=result,
        profit=profit,
        multiplier=1.0 if result == 'win' else 0,
        details={'player_total': player_total, 'dealer_total': dealer_total}
    )
    db.session.add(history)
    db.session.commit()
    
    # TERMINER LA PARTIE
    game_manager.end_game(current_user.id)
    
    # Nettoyer la partie (mais PAS la session de deck)
    session.pop('blackjack', None)

    new_achievements = check_and_unlock_achievements(current_user)
    
    # Info sur le deck pour affichage
    cards_remaining = len(deck)
    deck_percentage = (cards_remaining / blackjack_session['total_cards']) * 100
    will_shuffle = deck_percentage < 20  # Si moins de 20%, on mélangera au prochain coup
    
    return jsonify({
        'result': result,
        'result_message': result_message,
        'profit': profit,
        'money': current_user.money,
        'dealer_hand': game['dealer_hand'],
        'dealer_total': dealer_total,
        'player_total': player_total,
        'stats': get_global_stats(),
        'new_achievements': new_achievements,
        'cards_remaining': cards_remaining,
        'deck_percentage': round(deck_percentage, 1),
        'will_shuffle': will_shuffle
    })

# ============================================
# ROULETTE
# ============================================

@app.route('/api/roulette/spin', methods=['POST'])
@login_required
def roulette_spin():
    """Faire tourner la roulette"""
    data = request.json
    bet = int(data.get('bet', 50))
    mode = data.get('mode', 'color')
    choice = data.get('choice')
    
    # ASSERTIONS
    assert bet >= 10, "Mise minimum : 10$"
    assert bet <= current_user.money, "Mise trop élevée"
    
    current_user.remove_money(bet)
    
    # Générer le numéro
    number = random.randint(0, 36)
    
    # Déterminer la couleur
    red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    if number == 0:
        color = 'Green' 
    elif number in red_numbers:
        color = 'Red'  
    else:
        color = 'Black'  
    
    # Déterminer le résultat
    if mode == 'color':
        won = (choice == color)
        multiplier = 2 if won else 0
    else:
        won = (int(choice) == number)
        multiplier = 36 if won else 0
    
    result = 'win' if won else 'lose'
    profit = (bet * multiplier) - bet if won else -bet
    
    if won:
        current_user.add_money(bet * multiplier)
    
    # Sauvegarder l'historique
    history = GameHistory(
        user_id=current_user.id,
        game_type='roulette',
        bet_amount=bet,
        result=result,
        profit=profit,
        multiplier=multiplier,
        details={'number': number, 'color': color, 'choice': choice}
    )
    db.session.add(history)
    db.session.commit()

    new_achievements = check_and_unlock_achievements(current_user)
    
    return jsonify({
        'result': result,
        'number': number,
        'color': color,
        'profit': profit,
        'money': current_user.money,
        'stats': get_global_stats(),
        'new_achievements': new_achievements
    })

# ============================================
# MINEBOMB
# ============================================

@app.route('/api/minebomb/start', methods=['POST'])
@login_required
def minebomb_start():
    """Démarrer MineBomb"""
    data = request.json
    bet = int(data.get('bet', 50))
    bombs = int(data.get('bombs', 5))
    
    # ASSERTIONS
    assert bet >= 10, "Mise minimum : 10$"
    assert bet <= current_user.money, "Mise trop élevée"
    assert 3 <= bombs <= 10, "Entre 3 et 10 bombes"
    
    current_user.remove_money(bet)
    
    # Créer la grille
    grid = ['safe'] * (25 - bombs) + ['bomb'] * bombs
    random.shuffle(grid)
    
    session['minebomb'] = {
        'bet': bet,
        'bombs': bombs,
        'grid': grid,
        'revealed': [],
        'diamonds_found': 0
    }
    
    return jsonify({'money': current_user.money})

@app.route('/api/minebomb/reveal', methods=['POST'])
@login_required
def minebomb_reveal():
    """Révéler une case"""
    data = request.json
    index = int(data.get('index'))
    
    game = session.get('minebomb')
    assert game, "Pas de partie en cours"
    
    cell_type = game['grid'][index]
    game['revealed'].append(index)
    
    if cell_type == 'bomb':
        # Perdu
        history = GameHistory(
            user_id=current_user.id,
            game_type='minebomb',
            bet_amount=game['bet'],
            result='lose',
            profit=-game['bet'],
            multiplier=0,
            details={'bombs': game['bombs'], 'diamonds': game['diamonds_found']}
        )
        db.session.add(history)
        db.session.commit()
        
        session.pop('minebomb', None)
        
        return jsonify({
            'type': 'bomb',
            'money': current_user.money,
            'grid': game['grid'],
            'stats': get_global_stats()
        })
    
    else:
        # Diamant trouvé
        game['diamonds_found'] += 1
        
        # Calculer le multiplicateur
        safe_cells = 25 - game['bombs']
        diamonds = game['diamonds_found']
        multiplier = 1 + (diamonds * 0.3 * (game['bombs'] / 5))
        potential_win = int(game['bet'] * multiplier)
        
        session['minebomb'] = game
        
        return jsonify({
            'type': 'diamond',
            'multiplier': multiplier,
            'potential_win': potential_win,
            'diamonds_found': diamonds
        })

@app.route('/api/minebomb/cashout', methods=['POST'])
@login_required
def minebomb_cashout():
    """Encaisser les gains"""
    game = session.get('minebomb')
    assert game, "Pas de partie en cours. La session a peut-être expiré. Veuillez recommencer."
    
    diamonds = game['diamonds_found']
    multiplier = 1 + (diamonds * 0.3 * (game['bombs'] / 5))
    winnings = int(game['bet'] * multiplier)
    profit = winnings - game['bet']
    
    current_user.add_money(winnings)
    
    history = GameHistory(
        user_id=current_user.id,
        game_type='minebomb',
        bet_amount=game['bet'],
        result='win',
        profit=profit,
        multiplier=multiplier,
        details={'bombs': game['bombs'], 'diamonds': diamonds}
    )
    db.session.add(history)
    db.session.commit()
    
    session.pop('minebomb', None)
    
    new_achievements = check_and_unlock_achievements(current_user)

    return jsonify({
        'profit': profit,
        'multiplier': multiplier,
        'money': current_user.money,
        'stats': get_global_stats(),
        'new_achievements': new_achievements
    })

# ============================================
# SLOTS 
# ============================================

@app.route('/api/slots/spin', methods=['POST'])
@login_required
def slots_spin():
    """Faire tourner les slots"""
    data = request.json
    bet = int(data.get('bet', 50))
    
    # ASSERTIONS
    assert bet >= 10, "Mise minimum : 10$"
    assert bet <= current_user.money, "Mise trop élevée"
    
    current_user.remove_money(bet)
    
    symbols = ['🎰', '🍋', '🍊', '🍇', '7️⃣', '💎']
    reels = [random.choice(symbols) for _ in range(3)]
    
    # Déterminer le résultat
    if reels[0] == reels[1] == reels[2]:
        # 3 identiques
        multipliers = {
            '💎': 100,
            '7️⃣': 50,
            '🎰': 20,
            '🍋': 15,
            '🍊': 12,
            '🍇': 10
        }
        multiplier = multipliers.get(reels[0], 10)
        result = 'win'
    elif reels[0] == reels[1] or reels[1] == reels[2] or reels[0] == reels[2]:
        # 2 identiques
        multiplier = 2
        result = 'win'
    else:
        # Perdu
        multiplier = 0
        result = 'lose'
    
    profit = (bet * multiplier) - bet if result == 'win' else -bet
    
    if result == 'win':
        current_user.add_money(bet * multiplier)
    
    history = GameHistory(
        user_id=current_user.id,
        game_type='slots',
        bet_amount=bet,
        result=result,
        profit=profit,
        multiplier=multiplier,
        details={'reels': reels}
    )
    db.session.add(history)
    db.session.commit()

    new_achievements = check_and_unlock_achievements(current_user)
    
    return jsonify({
        'result': result,
        'reels': reels,
        'multiplier': multiplier,
        'profit': profit,
        'money': current_user.money,
        'stats': get_global_stats(),
        'new_achievements': new_achievements
    })

# ============================================
# HISTORIQUE
# ============================================

@app.route('/api/history')
@login_required
def get_history():
    """Récupère l'historique des 20 dernières parties"""
    games = GameHistory.query.filter_by(user_id=current_user.id)\
        .order_by(GameHistory.played_at.desc())\
        .limit(20)\
        .all()
    
    return jsonify([{
        'id': g.id,
        'game_type': g.game_type,
        'bet': g.bet_amount,
        'result': g.result,
        'profit': g.profit,
        'multiplier': g.multiplier,
        'date': g.played_at.isoformat()
    } for g in games])

# ============================================
# INITIALISATION
# ============================================

def init_db():
    """Initialise la base de données"""
    with app.app_context():
        db.create_all()
        
        if Achievement.query.count() == 0:
            achievements = [
                Achievement(name='Premier pas', description='Joue ta première partie', icon='🎮', reward=100),
                Achievement(name='Gagnant', description='Gagne 10 parties', icon='🏆', reward=500),
                Achievement(name='Chanceux', description='Gagne avec un multiplicateur x50+', icon='🍀', reward=1000),
                Achievement(name='Millionnaire', description='Atteins 10,000$', icon='💰', reward=2000),
                Achievement(name='Série de victoires', description='Gagne 5 parties d\'affilée', icon='🔥', reward=1500),
            ]
            db.session.add_all(achievements)
            db.session.commit()
            print("Achievements créés")


# Ajoute cet endpoint dans app.py

@app.route('/api/user_money_history')
@login_required
def user_money_history():
    """Récupère l'évolution de l'argent sur les 10 dernières parties"""
    
    # Récupérer les 10 dernières parties
    games = GameHistory.query.filter_by(user_id=current_user.id)\
        .order_by(GameHistory.played_at.asc())\
        .limit(10)\
        .all()
    
    if not games:
        return jsonify([])
    
    # Calculer l'argent après chaque partie
    # On part de l'argent actuel et on remonte
    current_balance = current_user.money
    history_points = []
    
    # On inverse pour partir de la fin
    for i, game in enumerate(reversed(games)):
        history_points.insert(0, {
            'game_number': len(games) - i,
            'money': current_balance,
            'game_type': game.game_type,
            'profit': game.profit,
            'date': game.played_at.strftime('%H:%M')
        })
        # On retire le profit pour avoir l'argent d'avant
        current_balance -= game.profit
    
    return jsonify(history_points)


    # ============================================
# ROUTES SYSTÈME SOCIAL - À AJOUTER À app.py
# ============================================

# PROFILS PUBLICS
# ============================================

@app.route('/profile/<string:username>')
@login_required
def public_profile(username):
    """Page de profil public d'un utilisateur"""
    user = User.query.filter_by(username=username).first()
    assert user, "Utilisateur non trouvé"
    
    return render_template('public_profile.html', profile_user=user)

@app.route('/api/profile/<int:user_id>')
@login_required
def get_public_profile(user_id):
    """API pour récupérer un profil public"""
    user = User.query.get(user_id)
    assert user, "Utilisateur non trouvé"
    
    profile = user.get_public_profile()
    
    # Ajouter le statut d'amitié
    profile['is_friend'] = current_user.is_friends_with(user)
    profile['request_sent'] = current_user.has_sent_request_to(user)
    profile['request_received'] = current_user.has_received_request_from(user)
    profile['is_self'] = current_user.id == user.id
    
    return jsonify(profile)

@app.route('/api/update_profile', methods=['POST'])
@login_required
def update_profile():
    """Mettre à jour son profil"""
    data = request.json
    
    if 'bio' in data:
        bio = data['bio'][:500]  # Limiter à 500 caractères
        current_user.bio = bio
    
    if 'favorite_game' in data:
        favorite_game = data['favorite_game']
        assert favorite_game in ['', 'blackjack', 'roulette', 'minebomb', 'slots', 'clicker'], "Jeu invalide"
        current_user.favorite_game = favorite_game
    
    if 'is_public' in data:
        current_user.is_public = bool(data['is_public'])
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Profil mis à jour'})




# SYSTÈME D'AMIS
# ============================================

@app.route('/api/friends/list')
@login_required
def get_friends():
    """Liste des amis"""
    friends = current_user.friends.all()
    
    friends_data = []
    for friend in friends:
        stats = friend.get_stats()
        friends_data.append({
            'id': friend.id,
            'username': friend.username,
            'money': friend.money,
            'favorite_game': friend.favorite_game,
            'total_games': stats['total_games'],
            'win_rate': stats['win_rate'],
            'is_online': (datetime.utcnow() - friend.last_login).seconds < 300  # En ligne si < 5 min
        })
    
    return jsonify(friends_data)

@app.route('/api/friends/requests')
@login_required
def get_friend_requests():
    """Liste des demandes d'amis reçues"""
    requests = current_user.received_requests.all()
    
    requests_data = []
    for user in requests:
        requests_data.append({
            'id': user.id,
            'username': user.username,
            'money': user.money,
            'avatar_url': user.avatar_url
        })
    
    return jsonify(requests_data)

@app.route('/api/friends/send/<int:user_id>', methods=['POST'])
@login_required
def send_friend_request(user_id):
    """Envoyer une demande d'ami"""
    user = User.query.get(user_id)
    assert user, "Utilisateur non trouvé"
    
    current_user.send_friend_request(user)
    
    return jsonify({'success': True, 'message': f'Demande envoyée à {user.username}'})

@app.route('/api/friends/accept/<int:user_id>', methods=['POST'])
@login_required
def accept_friend_request(user_id):
    """Accepter une demande d'ami"""
    user = User.query.get(user_id)
    assert user, "Utilisateur non trouvé"
    
    current_user.accept_friend_request(user)
    
    return jsonify({'success': True, 'message': f'Vous êtes maintenant ami avec {user.username}'})

@app.route('/api/friends/reject/<int:user_id>', methods=['POST'])
@login_required
def reject_friend_request(user_id):
    """Rejeter une demande d'ami"""
    user = User.query.get(user_id)
    assert user, "Utilisateur non trouvé"
    
    current_user.reject_friend_request(user)
    
    return jsonify({'success': True, 'message': 'Demande rejetée'})

@app.route('/api/friends/remove/<int:user_id>', methods=['POST'])
@login_required
def remove_friend(user_id):
    """Retirer un ami"""
    user = User.query.get(user_id)
    assert user, "Utilisateur non trouvé"
    
    current_user.remove_friend(user)
    
    return jsonify({'success': True, 'message': f'{user.username} retiré de vos amis'})


# SYSTÈME DE CLANS
# ============================================

@app.route('/clans')
@login_required
def clans_page():
    """Page des clans"""
    return render_template('clans.html')

@app.route('/api/clans/list')
@login_required
def get_clans():
    """Liste de tous les clans"""
    clans = Clan.query.order_by(Clan.money.desc()).all()
    
    clans_data = []
    for clan in clans:
        clans_data.append({
            'id': clan.id,
            'name': clan.name,
            'tag': clan.tag,
            'description': clan.description,
            'leader': clan.leader.username,
            'members_count': clan.get_member_count(),
            'max_members': clan.max_members,
            'total_money': clan.get_total_money(),
            'bank_money': clan.money,
            'is_public': clan.is_public,
            'created_at': clan.created_at.strftime('%Y-%m-%d')
        })
    
    return jsonify(clans_data)

@app.route('/api/clans/create', methods=['POST'])
@login_required
def create_clan():
    """Créer un clan (coûte 100M)"""
    data = request.json
    name = data.get('name')
    tag = data.get('tag')
    description = data.get('description', '')
    
    # ASSERTIONS
    assert name and tag, "Nom et tag requis"
    assert len(name) >= 3 and len(name) <= 50, "Le nom doit faire entre 3 et 50 caractères"
    assert len(tag) >= 2 and len(tag) <= 10, "Le tag doit faire entre 2 et 10 caractères"
    assert current_user.money >= 100_000_000, "Il faut 100,000,000$ pour créer un clan"
    assert current_user.clan_id is None, "Vous êtes déjà dans un clan"
    assert not Clan.query.filter_by(name=name).first(), "Ce nom de clan existe déjà"
    assert not Clan.query.filter_by(tag=tag).first(), "Ce tag existe déjà"
    
    # Créer le clan
    current_user.remove_money(100_000_000)
    
    clan = Clan(
        name=name,
        tag=tag,
        description=description,
        leader_id=current_user.id
    )
    
    db.session.add(clan)
    db.session.commit()
    
    # Ajouter le créateur comme leader
    clan.add_member(current_user, role='leader')
    
    return jsonify({
        'success': True,
        'message': f'Clan [{tag}] {name} créé !',
        'clan_id': clan.id
    })

@app.route('/api/clans/<int:clan_id>')
@login_required
def get_clan(clan_id):
    """Détails d'un clan"""
    clan = Clan.query.get(clan_id)
    assert clan, "Clan non trouvé"
    
    members = []
    for member in clan.members.all():
        stats = member.get_stats()
        
        # Récupérer le rôle
        stmt = clan_members.select().where(
            (clan_members.c.clan_id == clan_id) &
            (clan_members.c.user_id == member.id)
        )
        result = db.session.execute(stmt).first()
        role = result.role if result else 'member'
        
        members.append({
            'id': member.id,
            'username': member.username,
            'money': member.money,
            'total_games': stats['total_games'],
            'win_rate': stats['win_rate'],
            'role': role,
            'is_online': (datetime.utcnow() - member.last_login).seconds < 300
        })
    
    return jsonify({
        'id': clan.id,
        'name': clan.name,
        'tag': clan.tag,
        'description': clan.description,
        'leader_id': clan.leader_id,
        'leader_username': clan.leader.username,
        'members_count': clan.get_member_count(),
        'max_members': clan.max_members,
        'total_money': clan.get_total_money(),
        'bank_money': clan.money,
        'is_public': clan.is_public,
        'created_at': clan.created_at.strftime('%Y-%m-%d'),
        'members': members,
        'is_member': clan.is_member(current_user),
        'is_leader': clan.is_leader(current_user),
        'is_officer': clan.is_officer(current_user)
    })

@app.route('/api/clans/<int:clan_id>/join', methods=['POST'])
@login_required
def join_clan(clan_id):
    """Rejoindre un clan"""
    clan = Clan.query.get(clan_id)
    assert clan, "Clan non trouvé"
    assert clan.is_public, "Ce clan est sur invitation uniquement"
    
    clan.add_member(current_user)
    
    return jsonify({'success': True, 'message': f'Vous avez rejoint [{clan.tag}] {clan.name}'})

@app.route('/api/clans/<int:clan_id>/leave', methods=['POST'])
@login_required
def leave_clan(clan_id):
    """Quitter un clan"""
    clan = Clan.query.get(clan_id)
    assert clan, "Clan non trouvé"
    
    clan.remove_member(current_user)
    
    return jsonify({'success': True, 'message': f'Vous avez quitté [{clan.tag}] {clan.name}'})

@app.route('/api/clans/<int:clan_id>/kick/<int:user_id>', methods=['POST'])
@login_required
def kick_from_clan(clan_id, user_id):
    """Expulser un membre (leader/officer seulement)"""
    clan = Clan.query.get(clan_id)
    assert clan, "Clan non trouvé"
    assert clan.is_leader(current_user) or clan.is_officer(current_user), "Permissions insuffisantes"
    
    user = User.query.get(user_id)
    assert user, "Utilisateur non trouvé"
    
    clan.remove_member(user)
    
    return jsonify({'success': True, 'message': f'{user.username} a été expulsé'})

@app.route('/api/clans/<int:clan_id>/promote/<int:user_id>', methods=['POST'])
@login_required
def promote_member(clan_id, user_id):
    """Promouvoir un membre en officier (leader seulement)"""
    clan = Clan.query.get(clan_id)
    assert clan, "Clan non trouvé"
    assert clan.is_leader(current_user), "Seul le chef peut promouvoir"
    
    user = User.query.get(user_id)
    assert user, "Utilisateur non trouvé"
    
    clan.promote_to_officer(user)
    
    return jsonify({'success': True, 'message': f'{user.username} est maintenant officier'})

@app.route('/api/clans/<int:clan_id>/donate', methods=['POST'])
@login_required
def donate_to_clan(clan_id):
    """Donner de l'argent à la banque du clan"""
    clan = Clan.query.get(clan_id)
    assert clan, "Clan non trouvé"
    assert clan.is_member(current_user), "Vous n'êtes pas membre de ce clan"
    
    data = request.json
    amount = int(data.get('amount', 0))
    
    assert amount > 0, "Montant invalide"
    assert current_user.money >= amount, "Fonds insuffisants"
    
    current_user.remove_money(amount)
    clan.money += amount
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'{amount}$ donnés à la banque du clan',
        'clan_money': clan.money,
        'user_money': current_user.money
    })

# AJOUTER CETTE ROUTE DANS app.py (après /api/clans/<int:clan_id>/donate)

@app.route('/api/clans/<int:clan_id>/withdraw', methods=['POST'])
@login_required
def withdraw_from_clan(clan_id):
    """Retirer de l'argent de la banque du clan (leader seulement)"""
    clan = Clan.query.get(clan_id)
    assert clan, "Clan non trouvé"
    assert clan.is_leader(current_user), "Seul le chef peut retirer de l'argent"
    
    data = request.json
    amount = int(data.get('amount', 0))
    
    assert amount > 0, "Montant invalide"
    assert clan.money >= amount, "Fonds insuffisants dans la banque du clan"
    
    clan.money -= amount
    current_user.add_money(amount)
    
    return jsonify({
        'success': True,
        'message': f'{amount}$ retirés de la banque du clan',
        'clan_money': clan.money,
        'user_money': current_user.money
    })

@app.route('/api/clans/<int:clan_id>/update', methods=['POST'])
@login_required
def update_clan(clan_id):
    """Mettre à jour le clan (leader seulement)"""
    clan = Clan.query.get(clan_id)
    assert clan, "Clan non trouvé"
    assert clan.is_leader(current_user), "Seul le chef peut modifier le clan"
    
    data = request.json
    
    if 'description' in data:
        clan.description = data['description'][:500]
    
    if 'is_public' in data:
        clan.is_public = bool(data['is_public'])
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Clan mis à jour'})


# RECHERCHE D'UTILISATEURS
# ============================================

@app.route('/api/users/search')
@login_required
def search_users():
    """Rechercher des utilisateurs"""
    query = request.args.get('q', '').strip()
    
    if len(query) < 2:
        return jsonify([])
    
    users = User.query.filter(
        User.username.ilike(f'%{query}%')
    ).limit(20).all()
    
    results = []
    for user in users:
        if user.id == current_user.id:
            continue
        
        results.append({
            'id': user.id,
            'username': user.username,
            'money': user.money if user.is_public else None,
            'favorite_game': user.favorite_game,
            'is_friend': current_user.is_friends_with(user),
            'request_sent': current_user.has_sent_request_to(user),
            'clan_tag': Clan.query.get(user.clan_id).tag if user.clan_id else None
        })
    
    return jsonify(results)

    # Ajouter ces routes dans app.py

# Route pour la page sociale
@app.route('/social')
@login_required
def social_page():
    """Page des amis et recherche"""
    return render_template('social.html')

# Corriger la route du profil public pour accepter un ID
@app.route('/profile/user/<int:user_id>')
@login_required
def public_profile_by_id(user_id):
    """Page de profil public d'un utilisateur par ID"""
    user = User.query.get(user_id)
    assert user, "Utilisateur non trouvé"
    return render_template('public_profile.html', profile_user=user)

# Ajouter la route pour les détails de clan
@app.route('/clans/<int:clan_id>')
@login_required
def clan_detail(clan_id):
    """Page de détails d'un clan"""
    clan = Clan.query.get(clan_id)
    assert clan, "Clan non trouvé"
    return render_template('clan_detail.html', clan_id=clan_id)

# ============================================
# PLINKO
# ============================================

@app.route('/api/plinko/drop', methods=['POST'])
@login_required
def plinko_drop():
    """Lâcher la balle dans le Plinko"""
    data = request.json
    bet = int(data.get('bet', 50))
    risk = data.get('risk', 'medium')  # low, medium, high
    
    # ASSERTIONS
    assert bet >= 10, "Mise minimum : 10$"
    assert bet <= current_user.money, "Mise trop élevée"
    assert risk in ['low', 'medium', 'high'], "Niveau de risque invalide"
    
    current_user.remove_money(bet)
    
    # Simuler la chute de la balle (nombre de directions : 16 niveaux)
    path = []
    position = 8  # Centre (sur 17 positions possibles)
    
    for _ in range(16):
        direction = random.choice([-1, 1])
        position += direction
        position = max(0, min(16, position))  # Limiter entre 0 et 16
        path.append(position)
    
    # Multiplicateurs selon le risque et la position finale
    multipliers = {
        'low': [1.5, 1.3, 1.1, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.3, 1.5],
        'medium': [5.0, 3.0, 2.0, 1.5, 1.0, 0.5, 0.3, 0.2, 0.1, 0.2, 0.3, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0],
        'high': [50.0, 20.0, 5.0, 2.0, 0.5, 0.2, 0.1, 0.0, 0.0, 0.0, 0.1, 0.2, 0.5, 2.0, 5.0, 20.0, 50.0]
    }
    
    multiplier = multipliers[risk][position]
    
    winnings = int(bet * multiplier)
    profit = winnings - bet
    result = 'win' if multiplier >= 1.0 else 'lose'
    
    if winnings > 0:
        current_user.add_money(winnings)
    
    # Sauvegarder l'historique
    history = GameHistory(
        user_id=current_user.id,
        game_type='plinko',
        bet_amount=bet,
        result=result,
        profit=profit,
        multiplier=multiplier,
        details={'risk': risk, 'position': position, 'path': path}
    )
    db.session.add(history)
    db.session.commit()
    
    new_achievements = check_and_unlock_achievements(current_user)
    
    return jsonify({
        'result': result,
        'path': path,
        'position': position,
        'multiplier': multiplier,
        'profit': profit,
        'winnings': winnings,
        'money': current_user.money,
        'stats': get_global_stats(),
        'new_achievements': new_achievements
    })

@app.route('/health')
def health():
    return {'status': 'ok'}, 200

init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)