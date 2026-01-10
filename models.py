from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Modèle utilisateur"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    money = db.Column(db.Integer, default=5000, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    clicker_data = db.relationship('ClickerData', backref='user', uselist=False, cascade='all, delete-orphan')
    game_history = db.relationship('GameHistory', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    achievements = db.relationship('Achievement', secondary='user_achievements', backref='users')
    
    def set_password(self, password):
        """Hash le mot de passe"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Vérifie le mot de passe"""
        return check_password_hash(self.password_hash, password)
    
    def add_money(self, amount):
        """Ajoute de l'argent (avec validation)"""
        if amount < 0:
            raise ValueError("Le montant ne peut pas être négatif")
        self.money += amount
        db.session.commit()
    
    def remove_money(self, amount):
        """Retire de l'argent (avec validation)"""
        if amount < 0:
            raise ValueError("Le montant ne peut pas être négatif")
        if self.money < amount:
            raise ValueError("Fonds insuffisants")
        self.money -= amount
        db.session.commit()
    
    def get_stats(self):
        """Retourne les statistiques du joueur"""
        games = self.game_history.all()
        
        total_games = len(games)
        total_wins = sum(1 for g in games if g.result == 'win')
        total_losses = sum(1 for g in games if g.result == 'lose')
        total_wagered = sum(g.bet_amount for g in games)
        total_winnings = sum(g.profit for g in games if g.profit > 0)
        
        return {
            'total_games': total_games,
            'total_wins': total_wins,
            'total_losses': total_losses,
            'win_rate': round((total_wins / total_games * 100), 1) if total_games > 0 else 0,
            'total_wagered': total_wagered,
            'total_winnings': total_winnings,
            'net_profit': total_winnings - total_wagered
        }
    
    def __repr__(self):
        return f'<User {self.username}>'


class ClickerData(db.Model):
    """Données du Money Clicker par utilisateur - VERSION RÉÉQUILIBRÉE"""
    __tablename__ = 'clicker_data'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    click_power = db.Column(db.Integer, default=1)
    click_level = db.Column(db.Integer, default=1)
    auto_level = db.Column(db.Integer, default=0)
    factory_level = db.Column(db.Integer, default=0)
    bank_level = db.Column(db.Integer, default=0)
    
    # NOUVEAUX COÛTS - Plus élevés et progressifs
    click_cost = db.Column(db.Integer, default=25)
    auto_cost = db.Column(db.Integer, default=150)
    factory_cost = db.Column(db.Integer, default=800)
    bank_cost = db.Column(db.Integer, default=5000)
    
    total_clicks = db.Column(db.Integer, default=0)
    total_earned = db.Column(db.Integer, default=0)
    
    @property
    def passive_income(self):
        """Calcule le revenu passif - VERSION RÉÉQUILIBRÉE"""
        auto_income = self.auto_level * 0.5
        factory_income = self.factory_level * 2
        bank_income = self.bank_level * 8
        return int(auto_income + factory_income + bank_income)
    
    def __repr__(self):
        return f'<ClickerData user_id={self.user_id}>'


class GameHistory(db.Model):
    """Historique des parties"""
    __tablename__ = 'game_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    game_type = db.Column(db.String(20), nullable=False, index=True)
    
    bet_amount = db.Column(db.Integer, nullable=False)
    result = db.Column(db.String(10), nullable=False)
    profit = db.Column(db.Integer, default=0)
    multiplier = db.Column(db.Float, default=1.0)
    
    details = db.Column(db.JSON)
    played_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<GameHistory {self.game_type} - {self.result}>'


class Achievement(db.Model):
    """Succès débloquables"""
    __tablename__ = 'achievements'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(10), default='🏆')
    reward = db.Column(db.Integer, default=0)
    
    condition_type = db.Column(db.String(50))
    condition_value = db.Column(db.Integer)
    
    def __repr__(self):
        return f'<Achievement {self.name}>'


user_achievements = db.Table('user_achievements',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('achievement_id', db.Integer, db.ForeignKey('achievements.id'), primary_key=True),
    db.Column('unlocked_at', db.DateTime, default=datetime.utcnow)
)

# ============================================
# PROGRAMMATION ORIENTÉE OBJET + STRUCTURES DE DONNÉES
# ============================================

class GameAction:
    """
    Classe représentant une action de jeu (POO)
    Utilisée pour l'historique avec une PILE (Stack)
    """
    def __init__(self, action_type, card=None, total=0, details=None):
        self.action_type = action_type  # 'hit', 'stand', 'start', 'bet'
        self.card = card  # Carte tirée (pour BlackJack)
        self.total = total  # Total de la main
        self.details = details or {}  # Détails supplémentaires
        self.timestamp = datetime.utcnow()
    
    def __repr__(self):
        if self.card:
            return f'<GameAction {self.action_type} - {self.card["value"]}{self.card["suit"]} (Total: {self.total})>'
        return f'<GameAction {self.action_type} - Total: {self.total}>'
    
    def to_dict(self):
        """Convertit l'action en dictionnaire"""
        return {
            'action_type': self.action_type,
            'card': self.card,
            'total': self.total,
            'details': self.details,
            'timestamp': self.timestamp.isoformat()
        }


class ActionStack:
    """
    PILE (Stack - LIFO: Last In First Out)
    Structure de données pour gérer l'historique des actions
    Permet d'annuler la dernière action (UNDO)
    """
    def __init__(self, max_size=50):
        self.stack = []  # PILE
        self.max_size = max_size
    
    def push(self, action):
        """Empiler une action (ajouter au sommet)"""
        if isinstance(action, GameAction):
            self.stack.append(action)
            # Limiter la taille pour éviter surcharge mémoire
            if len(self.stack) > self.max_size:
                self.stack.pop(0)  # Retirer la plus ancienne
        else:
            raise TypeError("L'action doit être une instance de GameAction")
    
    def pop(self):
        """Dépiler (retirer et retourner la dernière action)"""
        if not self.is_empty():
            return self.stack.pop()
        return None
    
    def peek(self):
        """Voir le sommet de la pile sans dépiler"""
        if not self.is_empty():
            return self.stack[-1]
        return None
    
    def is_empty(self):
        """Vérifier si la pile est vide"""
        return len(self.stack) == 0
    
    def size(self):
        """Retourner la taille de la pile"""
        return len(self.stack)
    
    def clear(self):
        """Vider complètement la pile"""
        self.stack = []
    
    def get_all(self):
        """Obtenir toutes les actions (du plus ancien au plus récent)"""
        return list(self.stack)
    
    def __repr__(self):
        return f'<ActionStack size={self.size()}>'

class GameManager:
    """
    Classe de gestion des jeux (POO)
    Utilise la structure PILE (ActionStack) pour l'historique
    """
    def __init__(self):
        self.action_history = ActionStack()  # PILE pour l'historique
        self.active_games = {}               # Dictionnaire des parties actives
        # SUPPRIMÉ : self.pending_games = GameQueue()
        
    def start_game(self, user_id, game_type, bet):
        """Démarre une nouvelle partie"""
        game_data = {
            'user_id': user_id,
            'game_type': game_type,
            'bet': bet,
            'started_at': datetime.utcnow()
        }
        
        action = GameAction('start', details={'game_type': game_type, 'bet': bet})
        self.action_history.push(action)
        
        # Activer immédiatement
        self.active_games[user_id] = game_data
        
        return game_data
    
    def end_game(self, user_id):
        """Termine une partie"""
        if user_id in self.active_games:
            game_data = self.active_games.pop(user_id)
            action = GameAction('end', details={'game_type': game_data['game_type']})
            self.action_history.push(action)
            return game_data
        return None
    
    def record_action(self, action_type, card=None, total=0, details=None):
        """Enregistre une action dans l'historique (PILE)"""
        action = GameAction(action_type, card, total, details)
        self.action_history.push(action)
        return action
    
    def undo_last_action(self):
        """Annule la dernière action (dépile)"""
        return self.action_history.pop()
    
    def get_action_history(self):
        """Récupère tout l'historique des actions"""
        return self.action_history.get_all()
    
    def clear_history(self):
        """Réinitialise l'historique"""
        self.action_history.clear()
    
    def __repr__(self):
        return f'<GameManager active={len(self.active_games)} history={self.action_history.size()}>'


# Instance globale du gestionnaire de jeux
game_manager = GameManager()