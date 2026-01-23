from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

# ============================================
# TABLES D'ASSOCIATION (Many-to-Many)
# ============================================

# Table pour les amitiés
friendships = db.Table('friendships',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

# Table pour les demandes d'amis
friend_requests = db.Table('friend_requests',
    db.Column('sender_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('receiver_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

# Table pour les membres de clans
clan_members = db.Table('clan_members',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('clan_id', db.Integer, db.ForeignKey('clans.id'), primary_key=True),
    db.Column('joined_at', db.DateTime, default=datetime.utcnow),
    db.Column('role', db.String(20), default='member')  # 'leader', 'officer', 'member'
)

# Table pour les achievements des utilisateurs
user_achievements = db.Table('user_achievements',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('achievement_id', db.Integer, db.ForeignKey('achievements.id'), primary_key=True),
    db.Column('unlocked_at', db.DateTime, default=datetime.utcnow)
)


# ============================================
# MODÈLES
# ============================================

class User(UserMixin, db.Model):
    """Modèle utilisateur avec système social"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    money = db.Column(db.Integer, default=5000, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    last_ip = db.Column(db.String(45), default='')
    is_banned = db.Column(db.Boolean, default=False)
    ban_reason = db.Column(db.String(255), default='')
    
    # Profil public
    bio = db.Column(db.String(500), default='')
    avatar_url = db.Column(db.String(255), default='')
    is_public = db.Column(db.Boolean, default=True)
    favorite_game = db.Column(db.String(50), default='')
    
    # Relations
    clicker_data = db.relationship('ClickerData', backref='user', uselist=False, cascade='all, delete-orphan')
    game_history = db.relationship('GameHistory', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    achievements = db.relationship('Achievement', secondary='user_achievements', backref='users')
    
    # Relations sociales
    friends = db.relationship(
        'User',
        secondary=friendships,
        primaryjoin=(friendships.c.user_id == id),
        secondaryjoin=(friendships.c.friend_id == id),
        backref=db.backref('friended_by', lazy='dynamic'),
        lazy='dynamic'
    )
    
    sent_requests = db.relationship(
        'User',
        secondary=friend_requests,
        primaryjoin=(friend_requests.c.sender_id == id),
        secondaryjoin=(friend_requests.c.receiver_id == id),
        backref=db.backref('received_requests', lazy='dynamic'),
        lazy='dynamic'
    )
    
    # Clan
    clan_id = db.Column(db.Integer, db.ForeignKey('clans.id'), nullable=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def add_money(self, amount):
        assert amount >= 0, "Le montant ne peut pas être négatif"
        self.money += amount
        db.session.commit()
    
    def remove_money(self, amount):
        assert amount >= 0, "Le montant ne peut pas être négatif"
        assert self.money >= amount, "Fonds insuffisants"
        self.money -= amount
        db.session.commit()
    
    def get_stats(self):
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
    
    # Méthodes sociales
    def is_friends_with(self, user):
        return self.friends.filter(friendships.c.friend_id == user.id).count() > 0
    
    def has_sent_request_to(self, user):
        return self.sent_requests.filter(friend_requests.c.receiver_id == user.id).count() > 0
    
    def has_received_request_from(self, user):
        return self.received_requests.filter(friend_requests.c.sender_id == user.id).count() > 0
    
    def send_friend_request(self, user):
        assert user.id != self.id, "Vous ne pouvez pas vous ajouter vous-même"
        assert not self.is_friends_with(user), "Déjà amis"
        assert not self.has_sent_request_to(user), "Demande déjà envoyée"
        
        self.sent_requests.append(user)
        db.session.commit()
    
    def accept_friend_request(self, user):
        assert self.has_received_request_from(user), "Pas de demande de cet utilisateur"
        
        self.received_requests.remove(user)
        self.friends.append(user)
        user.friends.append(self)
        
        db.session.commit()
    
    def reject_friend_request(self, user):
        assert self.has_received_request_from(user), "Pas de demande de cet utilisateur"
        self.received_requests.remove(user)
        db.session.commit()
    
    def remove_friend(self, user):
        assert self.is_friends_with(user), "Pas amis"
        self.friends.remove(user)
        user.friends.remove(self)
        db.session.commit()
    
    def get_public_profile(self):
        stats = self.get_stats()
        clan = Clan.query.get(self.clan_id) if self.clan_id else None
        
        return {
            'id': self.id,
            'username': self.username,
            'bio': self.bio,
            'avatar_url': self.avatar_url,
            'money': self.money if self.is_public else None,
            'created_at': self.created_at.strftime('%Y-%m-%d'),
            'favorite_game': self.favorite_game,
            'total_games': stats['total_games'],
            'total_wins': stats['total_wins'],
            'win_rate': stats['win_rate'],
            'achievements_count': len(self.achievements),
            'clan': {
                'id': clan.id,
                'name': clan.name,
                'tag': clan.tag
            } if clan else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'


class Clan(db.Model):
    """Modèle pour les clans"""
    __tablename__ = 'clans'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    tag = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.String(500), default='')
    
    leader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    leader = db.relationship('User', foreign_keys=[leader_id], backref='led_clan')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    money = db.Column(db.Integer, default=0)
    
    max_members = db.Column(db.Integer, default=50)
    is_public = db.Column(db.Boolean, default=True)
    
    members = db.relationship(
        'User',
        secondary=clan_members,
        backref=db.backref('clans_joined', lazy='dynamic'),
        lazy='dynamic'
    )
    
    def get_member_count(self):
        return self.members.count()
    
    def get_total_money(self):
        members_money = sum(m.money for m in self.members.all())
        return members_money + self.money
    
    def get_officers(self):
        stmt = clan_members.select().where(
            (clan_members.c.clan_id == self.id) & 
            (clan_members.c.role == 'officer')
        )
        result = db.session.execute(stmt)
        officer_ids = [row.user_id for row in result]
        return User.query.filter(User.id.in_(officer_ids)).all()
    
    def is_leader(self, user):
        return user.id == self.leader_id
    
    def is_officer(self, user):
        stmt = clan_members.select().where(
            (clan_members.c.clan_id == self.id) &
            (clan_members.c.user_id == user.id) &
            (clan_members.c.role == 'officer')
        )
        return db.session.execute(stmt).first() is not None
    
    def is_member(self, user):
        return self.members.filter_by(id=user.id).count() > 0
    
    def add_member(self, user, role='member'):
        assert self.get_member_count() < self.max_members, "Clan plein"
        assert not self.is_member(user), "Déjà membre"
        assert user.clan_id is None, "Déjà dans un clan"
        
        stmt = clan_members.insert().values(
            user_id=user.id,
            clan_id=self.id,
            role=role,
            joined_at=datetime.utcnow()
        )
        db.session.execute(stmt)
        
        user.clan_id = self.id
        db.session.commit()
    
    def remove_member(self, user):
        assert self.is_member(user), "Pas membre du clan"
        assert not self.is_leader(user), "Le chef ne peut pas quitter son clan"
        
        self.members.remove(user)
        user.clan_id = None
        db.session.commit()
    
    def promote_to_officer(self, user):
        assert self.is_member(user), "Pas membre du clan"
        assert not self.is_officer(user), "Déjà officier"
        
        stmt = clan_members.update().where(
            (clan_members.c.clan_id == self.id) &
            (clan_members.c.user_id == user.id)
        ).values(role='officer')
        db.session.execute(stmt)
        db.session.commit()
    
    def __repr__(self):
        return f'<Clan [{self.tag}] {self.name}>'


class ClickerData(db.Model):
    """Données du Money Clicker"""
    __tablename__ = 'clicker_data'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    click_power = db.Column(db.Integer, default=1)
    click_level = db.Column(db.Integer, default=1)
    auto_level = db.Column(db.Integer, default=0)
    factory_level = db.Column(db.Integer, default=0)
    bank_level = db.Column(db.Integer, default=0)
    
    click_cost = db.Column(db.Integer, default=25)
    auto_cost = db.Column(db.Integer, default=150)
    factory_cost = db.Column(db.Integer, default=800)
    bank_cost = db.Column(db.Integer, default=5000)
    
    total_clicks = db.Column(db.Integer, default=0)
    total_earned = db.Column(db.Integer, default=0)
    
    @property
    def passive_income(self):
        assert self.auto_level >= 0, "Le niveau auto ne peut pas être négatif"
        assert self.factory_level >= 0, "Le niveau factory ne peut pas être négatif"
        assert self.bank_level >= 0, "Le niveau bank ne peut pas être négatif"
        
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


# ============================================
# PROGRAMMATION ORIENTÉE OBJET + PILE
# ============================================

class GameAction:
    """Classe représentant une action de jeu"""
    def __init__(self, action_type, card=None, total=0, details=None):
        assert isinstance(action_type, str), "Le type d'action doit être une chaîne"
        assert action_type in ['hit', 'stand', 'start', 'bet', 'deal_player', 'deal_dealer', 'dealer_hit', 'end'], \
            "Type d'action invalide"
        assert isinstance(total, (int, float)), "Le total doit être un nombre"
        assert total >= 0, "Le total ne peut pas être négatif"
        
        self.action_type = action_type
        self.card = card
        self.total = total
        self.details = details or {}
        self.timestamp = datetime.utcnow()
    
    def __repr__(self):
        if self.card:
            return f'<GameAction {self.action_type} - {self.card["value"]}{self.card["suit"]} (Total: {self.total})>'
        return f'<GameAction {self.action_type} - Total: {self.total}>'
    
    def to_dict(self):
        return {
            'action_type': self.action_type,
            'card': self.card,
            'total': self.total,
            'details': self.details,
            'timestamp': self.timestamp.isoformat()
        }


class ActionStack:
    """Pile pour gérer l'historique des actions"""
    def __init__(self, max_size=50):
        assert isinstance(max_size, int), "La taille maximale doit être un entier"
        assert max_size > 0, "La taille maximale doit être positive"
        
        self.stack = []
        self.max_size = max_size
    
    def push(self, action):
        assert isinstance(action, GameAction), "L'action doit être une instance de GameAction"
        self.stack.append(action)
        if len(self.stack) > self.max_size:
            self.stack.pop(0)
    
    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        return None
    
    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        return None
    
    def is_empty(self):
        return len(self.stack) == 0
    
    def size(self):
        return len(self.stack)
    
    def clear(self):
        self.stack = []
    
    def get_all(self):
        return list(self.stack)
    
    def __repr__(self):
        return f'<ActionStack size={self.size()}>'


class GameManager:
    """Gestionnaire de jeux avec historique"""
    def __init__(self):
        self.action_history = ActionStack()
        self.active_games = {}
        
    def start_game(self, user_id, game_type, bet):
        assert isinstance(user_id, int), "L'ID utilisateur doit être un entier"
        assert user_id > 0, "L'ID utilisateur doit être positif"
        assert isinstance(game_type, str), "Le type de jeu doit être une chaîne"
        assert game_type in ['blackjack', 'roulette', 'minebomb', 'slots'], "Type de jeu invalide"
        assert isinstance(bet, (int, float)), "La mise doit être un nombre"
        assert bet >= 10, "Mise minimum : 10$"
        
        game_data = {
            'user_id': user_id,
            'game_type': game_type,
            'bet': bet,
            'started_at': datetime.utcnow()
        }
        
        action = GameAction('start', details={'game_type': game_type, 'bet': bet})
        self.action_history.push(action)
        self.active_games[user_id] = game_data
        
        return game_data
    
    def end_game(self, user_id):
        assert isinstance(user_id, int), "L'ID utilisateur doit être un entier"
        
        if user_id in self.active_games:
            game_data = self.active_games.pop(user_id)
            action = GameAction('end', details={'game_type': game_data['game_type']})
            self.action_history.push(action)
            return game_data
        return None
    
    def record_action(self, action_type, card=None, total=0, details=None):
        action = GameAction(action_type, card, total, details)
        self.action_history.push(action)
        return action
    
    def undo_last_action(self):
        return self.action_history.pop()
    
    def get_action_history(self):
        return self.action_history.get_all()
    
    def clear_history(self):
        self.action_history.clear()
    
    def __repr__(self):
        return f'<GameManager active={len(self.active_games)} history={self.action_history.size()}>'


game_manager = GameManager()