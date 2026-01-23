// Variables globales
let currentMoney = 0;
let selectedColor = null;

// Variables clicker
let clickPower = 1;
let clickLevel = 1;
let autoLevel = 0;
let factoryLevel = 0;
let bankLevel = 0;
let passiveIncome = 0;

let clickCost = 25;
let autoCost = 150;
let factoryCost = 800;
let bankCost = 5000;

// Gestion de la sidebar
function showMenu() {
    document.querySelectorAll('.game-screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById('menu').classList.add('active');
    
    // Mettre à jour les items de la sidebar
    document.querySelectorAll('.sidebar-item').forEach(item => {
        item.classList.remove('active');
    });
    document.querySelector('.sidebar-item[onclick*="showMenu"]').classList.add('active');
}

function formatMoney(amount) {
    // PROTECTION : Si undefined ou null, retourner 0
    if (amount === undefined || amount === null || isNaN(amount)) {
        console.warn('formatMoney reçu une valeur invalide:', amount);
        return '0';
    }
    
    // Convertir en nombre
    amount = Number(amount);
    
    if (amount >= 1000000000) {
        return (amount / 1000000000).toFixed(1) + 'B';
    } else if (amount >= 1000000) {
        return (amount / 1000000).toFixed(1) + 'M';
    } else if (amount >= 1000) {
        return (amount / 1000).toFixed(1) + 'K';
    }
    return amount.toString();
}

// ============================================
// INITIALISATION
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    loadClickerData();
    startPassiveIncome();
    loadLeaderboard();
    
    // Formater l'argent dans la sidebar
    const sidebarMoney = document.getElementById('sidebarMoney');
    if (sidebarMoney) {
        const amount = parseInt(sidebarMoney.textContent.replace(/[^0-9]/g, ''));
        sidebarMoney.textContent = formatMoney(amount) + ' $';
    }
    
    // Faire disparaître le message de bienvenue
    const welcomeMessage = document.querySelector('.welcome-message');
    if (welcomeMessage) {
        setTimeout(() => {
            welcomeMessage.style.transition = 'opacity 0.5s, transform 0.5s';
            welcomeMessage.style.opacity = '0';
            welcomeMessage.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                welcomeMessage.style.display = 'none';
            }, 500);
        }, 4000);
    }
});

async function loadStats() {
    try {
        const response = await fetch('/api/get_stats');
        const stats = await response.json();
        updateStatsDisplay(stats);
    } catch (error) {
        console.error('Erreur chargement stats:', error);
    }
}

// NOUVEAU : Fonction pour charger le leaderboard
async function loadLeaderboard() {
    try {
        const response = await fetch('/api/leaderboard');
        const leaderboard = await response.json();
        
        const tbody = document.getElementById('leaderboardBody');
        if (!tbody) return; // Si pas sur la page d'accueil
        
        if (leaderboard.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" style="text-align: center; color: #64748b; padding: 20px;">
                        Aucun joueur pour le moment
                    </td>
                </tr>
            `;
            return;
        }
        
        tbody.innerHTML = leaderboard.map(player => {
            let rankBadge;
            if (player.rank === 1) {
                rankBadge = `<span class="rank-badge rank-1">${player.rank}</span>`;
            } else if (player.rank === 2) {
                rankBadge = `<span class="rank-badge rank-2">${player.rank}</span>`;
            } else if (player.rank === 3) {
                rankBadge = `<span class="rank-badge rank-3">${player.rank}</span>`;
            } else {
                rankBadge = `<span class="rank-badge rank-other">${player.rank}</span>`;
            }
            
            const winRateClass = player.win_rate >= 60 ? 'win-rate-high' : 
                                 player.win_rate >= 40 ? 'win-rate-medium' : 'win-rate-low';
            
            const rowClass = player.is_current_user ? 'current-user' : '';
            
            return `
                <tr class="${rowClass}">
                    <td>${rankBadge}</td>
                    <td class="player-name">${player.username}</td>
                    <td class="money-value">${player.money} $</td>
                    <td>${player.total_games}</td>
                    <td>${player.total_wins}</td>
                    <td class="${winRateClass}">${player.win_rate}%</td>
                </tr>
            `;
        }).join('');
        
    } catch (error) {
        console.error('Erreur chargement leaderboard:', error);
        const tbody = document.getElementById('leaderboardBody');
        if (tbody) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" style="text-align: center; color: #ef4444; padding: 20px;">
                        Erreur de chargement du classement
                    </td>
                </tr>
            `;
        }
    }
}

async function loadClickerData() {
    try {
        const response = await fetch('/api/clicker/get_data');
        const data = await response.json();
        
        clickPower = data.clickPower;
        clickLevel = data.clickLevel;
        autoLevel = data.autoLevel;
        factoryLevel = data.factoryLevel;
        bankLevel = data.bankLevel;
        
        clickCost = data.clickCost;
        autoCost = data.autoCost;
        factoryCost = data.factoryCost;
        bankCost = data.bankCost;
        
        passiveIncome = data.passiveIncome;
        
        updateClickerDisplay();
    } catch (error) {
        console.error('Erreur chargement clicker:', error);
    }
}

// ============================================
// NAVIGATION - VERSION CORRIGÉE
// ============================================
function startGame(game) {
    // Masquer le menu
    document.getElementById('menu').classList.remove('active');
    
    // Masquer TOUS les autres jeux
    document.querySelectorAll('.game-screen').forEach(screen => {
        screen.classList.remove('active');
    });
    
    // Afficher SEULEMENT le jeu sélectionné
    document.getElementById(game).classList.add('active');
    
    // Mettre à jour les items de la sidebar
    document.querySelectorAll('.sidebar-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Activer l'item correspondant dans la sidebar
    const sidebarItem = document.querySelector(`.sidebar-item[onclick*="${game}"]`);
    if (sidebarItem) {
        sidebarItem.classList.add('active');
    }
}

function backToMenu() {
    // Masquer tous les jeux
    document.querySelectorAll('.game-screen').forEach(screen => {
        screen.classList.remove('active');
    });
    
    // Afficher le menu
    document.getElementById('menu').classList.add('active');
    
    // Mettre à jour la sidebar
    document.querySelectorAll('.sidebar-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Activer "Accueil" dans la sidebar
    const homeItem = document.querySelector('.sidebar-item[onclick*="showMenu"]');
    if (homeItem) {
        homeItem.classList.add('active');
    }
}

function showMenu() {
    backToMenu(); // Utilise la même logique
}

// ============================================
// GESTION ARGENT
// ============================================
function updateMoneyDisplay(money) {
    currentMoney = money;
    
    const sidebarMoney = document.getElementById('sidebarMoney');
    if (sidebarMoney) {
        sidebarMoney.textContent = formatMoney(money) + ' $';
        sidebarMoney.classList.add('pulse');
        setTimeout(() => sidebarMoney.classList.remove('pulse'), 500);
    }
}
// ============================================
// STATISTIQUES
// ============================================
function updateStatsDisplay(stats) {
    // VÉRIFIER SI LES ÉLÉMENTS EXISTENT (seulement sur index.html)
    const totalGames = document.getElementById('totalGames');
    if (!totalGames) return; // Si pas sur la page principale, on skip
    
    // Maintenant on peut mettre à jour en toute sécurité
    totalGames.textContent = stats.totalGames;
    document.getElementById('totalWins').textContent = stats.totalWins;
    document.getElementById('totalLosses').textContent = stats.totalLosses;
    document.getElementById('biggestWin').textContent = stats.biggestWin + ' $';
    document.getElementById('biggestLoss').textContent = stats.biggestLoss + ' $';
    document.getElementById('totalWagered').textContent = stats.totalWagered + ' $';
    document.getElementById('totalWinnings').textContent = stats.totalWinnings + ' $';
    
    const winRate = stats.totalGames > 0 ? ((stats.totalWins / stats.totalGames) * 100).toFixed(1) : 0;
    document.getElementById('winRate').textContent = winRate + '%';
    
    // BlackJack
    const bjGames = document.getElementById('bjGames');
    if (bjGames) {
        bjGames.textContent = stats.blackjack.games;
        document.getElementById('bjWins').textContent = stats.blackjack.wins;
        const bjWinRate = stats.blackjack.games > 0 ? ((stats.blackjack.wins / stats.blackjack.games) * 100).toFixed(1) : 0;
        document.getElementById('bjWinRate').textContent = bjWinRate + '%';
        const bjProfit = stats.blackjack.won - stats.blackjack.wagered;
        document.getElementById('bjProfit').textContent = bjProfit + ' $';
        document.getElementById('bjProfit').style.color = bjProfit >= 0 ? '#22c55e' : '#ef4444';
    }
    
    // Roulette
    const rouletteGames = document.getElementById('rouletteGames');
    if (rouletteGames) {
        rouletteGames.textContent = stats.roulette.games;
        document.getElementById('rouletteWins').textContent = stats.roulette.wins;
        const rouletteWinRate = stats.roulette.games > 0 ? ((stats.roulette.wins / stats.roulette.games) * 100).toFixed(1) : 0;
        document.getElementById('rouletteWinRate').textContent = rouletteWinRate + '%';
        const rouletteProfit = stats.roulette.won - stats.roulette.wagered;
        document.getElementById('rouletteProfit').textContent = rouletteProfit + ' $';
        document.getElementById('rouletteProfit').style.color = rouletteProfit >= 0 ? '#22c55e' : '#ef4444';
    }
    
    // MineBomb
    const mbGames = document.getElementById('mbGames');
    if (mbGames) {
        mbGames.textContent = stats.minebomb.games;
        document.getElementById('mbWins').textContent = stats.minebomb.wins;
        const mbWinRate = stats.minebomb.games > 0 ? ((stats.minebomb.wins / stats.minebomb.games) * 100).toFixed(1) : 0;
        document.getElementById('mbWinRate').textContent = mbWinRate + '%';
        const mbProfit = stats.minebomb.won - stats.minebomb.wagered;
        document.getElementById('mbProfit').textContent = mbProfit + ' $';
        document.getElementById('mbProfit').style.color = mbProfit >= 0 ? '#22c55e' : '#ef4444';
    }
    
    // Slots
    if (stats.slots) {
        const slotsGames = document.getElementById('slotsGames');
        if (slotsGames) {
            slotsGames.textContent = stats.slots.games;
            document.getElementById('slotsWins').textContent = stats.slots.wins;
            const slotsWinRate = stats.slots.games > 0 ? ((stats.slots.wins / stats.slots.games) * 100).toFixed(1) : 0;
            document.getElementById('slotsWinRate').textContent = slotsWinRate + '%';
            const slotsProfit = stats.slots.won - stats.slots.wagered;
            document.getElementById('slotsProfit').textContent = slotsProfit + ' $';
            document.getElementById('slotsProfit').style.color = slotsProfit >= 0 ? '#22c55e' : '#ef4444';
        }
    }
}

// ============================================
// MONEY CLICKER
// ============================================

function showFloatingNumber(amount) {
    const container = document.getElementById('floatingNumbers');
    const floatingNum = document.createElement('div');
    floatingNum.className = 'floating-number';
    floatingNum.textContent = '+' + amount + ' $';
    floatingNum.style.left = (Math.random() * 200 - 100) + 'px';
    container.appendChild(floatingNum);
    
    setTimeout(() => {
        floatingNum.remove();
    }, 2000);
}

async function buyUpgrade(type) {
    try {
        const response = await fetch('/api/clicker/upgrade', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({type})
        });
        
        if (!response.ok) {
            const error = await response.json();
            alert(error.error);
            return;
        }
        
        const data = await response.json();
        updateMoneyDisplay(data.money);
        
        clickPower = data.clickPower;
        clickLevel = data.clickLevel;
        autoLevel = data.autoLevel;
        factoryLevel = data.factoryLevel;
        bankLevel = data.bankLevel;
        
        clickCost = data.clickCost;
        autoCost = data.autoCost;
        factoryCost = data.factoryCost;
        bankCost = data.bankCost;
        
        passiveIncome = data.passiveIncome;
        
        updateClickerDisplay();
        
    } catch (error) {
        console.error('Erreur upgrade:', error);
    }
}

function updateClickerDisplay() {
    document.getElementById('clickValue').textContent = clickPower;
    document.getElementById('clickLevel').textContent = clickLevel;
    document.getElementById('autoLevel').textContent = autoLevel;
    document.getElementById('factoryLevel').textContent = factoryLevel;
    document.getElementById('bankLevel').textContent = bankLevel;
    
    document.getElementById('clickCost').textContent = clickCost;
    document.getElementById('autoCost').textContent = autoCost;
    document.getElementById('factoryCost').textContent = factoryCost;
    document.getElementById('bankCost').textContent = bankCost;
    
    const sidebarIncome = document.getElementById('sidebarIncome');
    if (sidebarIncome) {
        sidebarIncome.textContent = '+' + passiveIncome + ' $/s';
    }
}

function startPassiveIncome() {
    setInterval(async () => {
        if (passiveIncome > 0) {
            try {
                const response = await fetch('/api/clicker/passive', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'}
                });
                
                const data = await response.json();
                updateMoneyDisplay(data.money);
            } catch (error) {
                console.error('Erreur revenu passif:', error);
            }
        }
    }, 1000);
}

// ============================================
// BLACKJACK
// ============================================
async function startBlackjack() {
    const bet = parseInt(document.getElementById('bjBet').value);
    
    try {
        const response = await fetch('/api/blackjack/start', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({bet})
        });
        
        if (!response.ok) {
            const error = await response.json();
            alert(error.error);
            return;
        }
        
        const data = await response.json();
        updateMoneyDisplay(data.money);
        
        document.getElementById('bjBetting').style.display = 'none';
        document.getElementById('bjGame').style.display = 'block';
        document.getElementById('bjMessage').innerHTML = '';
        
        // Update deck info
        const totalCards = data.num_decks * 52;
        document.getElementById('deckInfo').innerHTML = `
            Cette partie utilise <strong>${data.num_decks} paquet${data.num_decks > 1 ? 's' : ''} de cartes</strong> (${totalCards} cartes)
        `;
        
        displayHand('player', data.player_hand, data.player_total);
        displayHand('dealer', data.dealer_hand.slice(0, 1), '?', true);
        
        document.getElementById('hitBtn').disabled = false;
        document.getElementById('standBtn').disabled = false;
        
    } catch (error) {
        console.error('Blackjack error:', error);
        alert('Connection error');
    }
}

async function hit() {
    try {
        const response = await fetch('/api/blackjack/hit', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        });
        
        const data = await response.json();
        displayHand('player', data.player_hand, data.player_total);
        
        if (data.busted) {
            document.getElementById('hitBtn').disabled = true;
            document.getElementById('standBtn').disabled = true;
            stand();
        }
        
    } catch (error) {
        console.error('Hit error:', error);
    }
}

async function stand() {
    try {
        const response = await fetch('/api/blackjack/stand', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        });
        
        const data = await response.json();
        
        displayHand('dealer', data.dealer_hand, data.dealer_total, false);
        
        const msgDiv = document.getElementById('bjMessage');
        msgDiv.className = 'message';
        
        if (data.result === 'win') {
            msgDiv.classList.add('win');
            msgDiv.innerHTML = `✅ Vous avez gagné !<br>Vous gagnez ${data.profit} $`;
        } else if (data.result === 'lose') {
            msgDiv.classList.add('lose');
            msgDiv.innerHTML = `❌ Vous avez perdu!`;
        } else {
            msgDiv.classList.add('info');
            msgDiv.innerHTML = `🤝 ÉGALITÉ ! Votre mise vous a été retournée.`;
        }
        
        updateMoneyDisplay(data.money);
        updateStatsDisplay(data.stats);
        
        document.getElementById('hitBtn').disabled = true;
        document.getElementById('standBtn').disabled = true;
        
        setTimeout(() => {
            document.getElementById('bjGame').style.display = 'none';
            document.getElementById('bjBetting').style.display = 'block';
        }, 3000);
        
    } catch (error) {
        console.error('Stand error:', error);
    }
}

function displayHand(player, cards, total, hideSecond = false) {
    const cardsDiv = document.getElementById(player + 'Cards');
    const totalSpan = document.getElementById(player + 'Total');
    
    cardsDiv.innerHTML = '';
    
    cards.forEach((card, index) => {
        const cardDiv = document.createElement('div');
        if (hideSecond && index === 1) {
            cardDiv.className = 'card card-back';
            cardDiv.textContent = '🂠';
        } else {
            const isRed = card.suit === '♥' || card.suit === '♦';
            cardDiv.className = 'card' + (isRed ? ' red' : '');
            cardDiv.innerHTML = card.value + '<br>' + card.suit;
        }
        cardsDiv.appendChild(cardDiv);
    });
    
    totalSpan.textContent = total;
}

// ============================================
// ROULETTE
// ============================================
function updateRouletteMode() {
    const mode = document.getElementById('rouletteMode').value;
    if (mode === 'color') {
        document.getElementById('colorMode').style.display = 'block';
        document.getElementById('numberMode').style.display = 'none';
    } else {
        document.getElementById('colorMode').style.display = 'none';
        document.getElementById('numberMode').style.display = 'block';
    }
    selectedColor = null;
    document.querySelectorAll('.color-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
}

function selectColor(color) {
    selectedColor = color;
    document.querySelectorAll('.color-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    event.target.classList.add('selected');
}

async function spinRoulette() {
    const bet = parseInt(document.getElementById('rouletteBet').value);
    const mode = document.getElementById('rouletteMode').value;
    
    let choice;
    if (mode === 'color') {
        if (!selectedColor) {
            alert('Veuillez sélectionner une couleur!');
            return;
        }
        choice = selectedColor;
    } else {
        choice = document.getElementById('rouletteNumber').value;
    }
    
    const wheel = document.getElementById('rouletteWheel');
    const resultCenter = document.getElementById('rouletteResult');
    wheel.classList.add('spinning');
    
    // Réinitialiser le centre
    resultCenter.textContent = '?';
    resultCenter.style.background = '#1e293b';
    resultCenter.style.color = 'white';
    
    try {
        const response = await fetch('/api/roulette/spin', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({bet, mode, choice})
        });
        
        if (!response.ok) {
            const error = await response.json();
            alert(error.error);
            wheel.classList.remove('spinning');
            return;
        }
        
        const data = await response.json();
        
        setTimeout(() => {
            wheel.classList.remove('spinning');
            
            // Afficher le numéro avec la couleur correspondante
            resultCenter.textContent = data.number;
            
            if (data.color === 'Green') {
                resultCenter.style.background = '#22c55e';
                resultCenter.style.color = 'white';
            } else if (data.color === 'Red') {
                resultCenter.style.background = '#ef4444';
                resultCenter.style.color = 'white';
            } else { // Black
                resultCenter.style.background = '#1f2937';
                resultCenter.style.color = 'white';
            }
            
            const msgDiv = document.getElementById('rouletteMessage');
            msgDiv.className = 'message';
            
            if (data.result === 'win') {
                msgDiv.classList.add('win');
                msgDiv.innerHTML = `✅ ${data.color} ${data.number}!<br>Vous gagnez ${data.profit} $`;
            } else {
                msgDiv.classList.add('lose');
                msgDiv.innerHTML = `❌ ${data.color} ${data.number}<br>Vous perdez ${bet} $`;
            }
            
            updateMoneyDisplay(data.money);
            updateStatsDisplay(data.stats);
            
            setTimeout(() => {
                msgDiv.innerHTML = '';
            }, 3000);
        }, 3000);
        
    } catch (error) {
        console.error('Roulette error:', error);
        wheel.classList.remove('spinning');
        alert('Connection error');
    }
}

// ============================================
// MINEBOMB
// ============================================
async function startMineBomb() {
    const bet = parseInt(document.getElementById('mbBet').value);
    const bombs = parseInt(document.getElementById('mbBombs').value);
    
    if (bombs < 3 || bombs > 10) {
        alert('Le nombre de bombes doit être entre 3 et 10!');
        return;
    }
    
    try {
        const response = await fetch('/api/minebomb/start', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({bet, bombs})
        });
        
        if (!response.ok) {
            const error = await response.json();
            alert(error.error);
            return;
        }
        
        const data = await response.json();
        updateMoneyDisplay(data.money);
        
        document.getElementById('mbBetting').style.display = 'none';
        document.getElementById('mbGame').style.display = 'block';
        document.getElementById('mbMessage').innerHTML = '';
        
        document.getElementById('multiplier').textContent = '1.00';
        document.getElementById('potentialWin').textContent = '0';
        document.getElementById('bombCount').textContent = bombs;
        document.getElementById('diamondCount').textContent = '0';
        
        const grid = document.getElementById('mineGrid');
        grid.innerHTML = '';
        for (let i = 0; i < 25; i++) {
            const cell = document.createElement('div');
            cell.className = 'mine-cell';
            cell.dataset.index = i;
            cell.onclick = () => revealCell(i);
            grid.appendChild(cell);
        }
        
        document.getElementById('cashoutBtn').disabled = true;
        
    } catch (error) {
        console.error('MineBomb error:', error);
        alert('Connection error');
    }
}

async function revealCell(index) {
    const cell = document.querySelectorAll('.mine-cell')[index];
    if (cell.classList.contains('revealed')) return;
    
    try {
        const response = await fetch('/api/minebomb/reveal', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({index})
        });
        
        const data = await response.json();
        cell.classList.add('revealed');
        
        if (data.type === 'bomb') {
            cell.classList.add('bomb');
            cell.innerHTML = '💣';
            
            if (data.grid) {
                document.querySelectorAll('.mine-cell').forEach((c, i) => {
                    c.onclick = null;
                    if (data.grid[i] === 'bomb' && !c.classList.contains('revealed')) {
                        setTimeout(() => {
                            c.classList.add('revealed', 'bomb');
                            c.innerHTML = '💣';
                        }, Math.random() * 1000);
                    }
                });
            }
            
            const msgDiv = document.getElementById('mbMessage');
            msgDiv.className = 'message lose';
            msgDiv.innerHTML = '💥 BOUM! Vous avez perdu';
            
            updateMoneyDisplay(data.money);
            updateStatsDisplay(data.stats);
            
            document.getElementById('cashoutBtn').disabled = true;
            
            setTimeout(() => {
                document.getElementById('mbGame').style.display = 'none';
                document.getElementById('mbBetting').style.display = 'block';
            }, 3000);
            
        } else {
            cell.classList.add('safe');
            cell.innerHTML = '💎';
            document.getElementById('multiplier').textContent = data.multiplier.toFixed(2);
            document.getElementById('potentialWin').textContent = data.potential_win;
            document.getElementById('diamondCount').textContent = data.diamonds_found;
            document.getElementById('cashoutBtn').disabled = false;
        }
        
    } catch (error) {
        console.error('Reveal error:', error);
    }
}

async function cashout() {
    try {
        const response = await fetch('/api/minebomb/cashout', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        });
        
        const data = await response.json();
        
        // VÉRIFIER SI ERREUR
        if (!response.ok || !data.success) {
            const errorMsg = data.error || 'Erreur inconnue';
            alert('❌ ' + errorMsg);
            
            // Si session expirée, reload la page
            if (errorMsg.includes('session') || errorMsg.includes('partie')) {
                setTimeout(() => location.reload(), 1500);
            }
            return;
        }
        
        // SUCCÈS - Mettre à jour l'argent
        if (data.money !== undefined) {
            updateMoneyDisplay(data.money);
        }
        
        if (data.stats) {
            updateStatsDisplay(data.stats);
        }
        
        const msgDiv = document.getElementById('mbMessage');
        msgDiv.className = 'message win';
        msgDiv.innerHTML = `💰 CASHOUT!<br>Vous gagnez ${data.profit} $ (x${data.multiplier})`;
        
        document.querySelectorAll('.mine-cell').forEach(cell => {
            cell.onclick = null;
        });
        document.getElementById('cashoutBtn').disabled = true;
        
        setTimeout(() => {
            document.getElementById('mbGame').style.display = 'none';
            document.getElementById('mbBetting').style.display = 'block';
        }, 3000);
        
    } catch (error) {
        console.error('Cashout error:', error);
        alert('❌ Erreur de connexion. Vérifie ta connexion internet.');
    }
}

// ============================================
// SLOT MACHINE
// ============================================
async function spinSlots() {
    const bet = parseInt(document.getElementById('slotsBet').value);
    const btn = document.getElementById('spinSlotsBtn');
    
    btn.disabled = true;
    
    try {
        const reel1 = document.getElementById('reel1');
        const reel2 = document.getElementById('reel2');
        const reel3 = document.getElementById('reel3');
        
        const symbols = ['🎰', '🍋', '🍊', '🍇', '7️⃣', '💎'];
        
        let count = 0;
        const interval = setInterval(() => {
            reel1.textContent = symbols[Math.floor(Math.random() * symbols.length)];
            reel2.textContent = symbols[Math.floor(Math.random() * symbols.length)];
            reel3.textContent = symbols[Math.floor(Math.random() * symbols.length)];
            count++;
            
            if (count >= 20) {
                clearInterval(interval);
            }
        }, 100);
        
        const response = await fetch('/api/slots/spin', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({bet})
        });
        
        if (!response.ok) {
            const error = await response.json();
            alert(error.error);
            btn.disabled = false;
            clearInterval(interval);
            return;
        }
        
        const data = await response.json();
        
        setTimeout(() => {
            clearInterval(interval);
            
            reel1.textContent = data.reels[0];
            reel2.textContent = data.reels[1];
            reel3.textContent = data.reels[2];
            
            const msgDiv = document.getElementById('slotsMessage');
            msgDiv.className = 'message';
            
            if (data.result === 'win') {
                msgDiv.classList.add('win');
                let jackpotMsg = '';
                if (data.multiplier === 100) {
                    jackpotMsg = '🎊 MEGA JACKPOT! 🎊<br>';
                } else if (data.multiplier === 50) {
                    jackpotMsg = '🎉 JACKPOT! 🎉<br>';
                }
                msgDiv.innerHTML = `${jackpotMsg}✅ ${data.reels.join(' ')}!<br>Vous gagnez ${data.profit} $ (x${data.multiplier})`;
            } else {
                msgDiv.classList.add('lose');
                msgDiv.innerHTML = `❌ ${data.reels.join(' ')}<br>Vous perdez ${bet} $`;
            }
            
            updateMoneyDisplay(data.money);
            updateStatsDisplay(data.stats);
            
            setTimeout(() => {
                msgDiv.innerHTML = '';
                btn.disabled = false;
            }, 3000);
        }, 2000);
        
    } catch (error) {
        console.error('Slots error:', error);
        alert('Connection error');
        btn.disabled = false;
    }
}

// ============================================
// Plinko le sang de la veine
// ============================================

let plinkoCanvas = null;
let plinkoCtx = null;
let plinkoBall = null;
let plinkoAnimating = false;
let plinkoMultipliers = [];
let plinkoPegs = [];

const PLINKO_ROWS = 16;
const PLINKO_PEG_RADIUS = 5;
const PLINKO_BALL_RADIUS = 10;
const PLINKO_SPACING = 48;
const PLINKO_START_X = 425;
const PLINKO_START_Y = 70;
const GRAVITY = 0.5;
const BOUNCE = 0.65;
const FRICTION = 0.98;

// Classe Balle avec physique réaliste
class Ball {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.vx = (Math.random() - 0.5) * 0.5; // Petite variation aléatoire initiale
        this.vy = 0;
        this.radius = PLINKO_BALL_RADIUS;
        this.color = '#fbbf24';
        this.glowIntensity = 0;
        this.trail = [];
        this.maxTrail = 12;
    }

    update() {
        // Gravité
        this.vy += GRAVITY;
        
        // Friction de l'air très légère
        this.vx *= FRICTION;
        this.vy *= FRICTION;
        
        // Limiter vitesse max pour éviter bugs
        const maxSpeed = 18;
        const speed = Math.sqrt(this.vx * this.vx + this.vy * this.vy);
        if (speed > maxSpeed) {
            this.vx = (this.vx / speed) * maxSpeed;
            this.vy = (this.vy / speed) * maxSpeed;
        }
        
        // Update position
        this.x += this.vx;
        this.y += this.vy;
        
        // Trail effect
        if (Math.random() > 0.3) {
            this.trail.push({x: this.x, y: this.y, alpha: 1});
        }
        
        // Fade trail
        this.trail = this.trail.filter(t => {
            t.alpha -= 0.05;
            return t.alpha > 0;
        });
        
        if (this.trail.length > this.maxTrail) {
            this.trail.shift();
        }
        
        // Glow effect basé sur la vitesse
        this.glowIntensity = Math.min(speed / 10, 1);
        
        // Collision avec pegs
        this.checkPegCollisions();
        
        // Rebond sur les bords latéraux
        if (this.x - this.radius < 20) {
            this.x = 20 + this.radius;
            this.vx *= -BOUNCE;
        }
        if (this.x + this.radius > plinkoCanvas.width - 20) {
            this.x = plinkoCanvas.width - 20 - this.radius;
            this.vx *= -BOUNCE;
        }
    }

    checkPegCollisions() {
        plinkoPegs.forEach(peg => {
            const dx = this.x - peg.x;
            const dy = this.y - peg.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            const minDist = this.radius + peg.radius;
            
            if (distance < minDist) {
                // Collision détectée !
                const angle = Math.atan2(dy, dx);
                const targetX = peg.x + Math.cos(angle) * minDist;
                const targetY = peg.y + Math.sin(angle) * minDist;
                
                // Corriger position
                this.x = targetX;
                this.y = targetY;
                
                // Calculer nouvelle vitesse avec effet de rebond
                const speed = Math.sqrt(this.vx * this.vx + this.vy * this.vy);
                this.vx = Math.cos(angle) * speed * BOUNCE;
                this.vy = Math.sin(angle) * speed * BOUNCE;
                
                // Ajouter rotation aléatoire légère
                const randomSpin = (Math.random() - 0.5) * 2;
                this.vx += randomSpin;
                
                // Effet visuel sur le peg
                peg.hit = true;
                setTimeout(() => peg.hit = false, 150);
            }
        });
    }

    draw(ctx) {
        // Dessiner trail
        this.trail.forEach((point, i) => {
            const size = (this.radius * 0.6) * (i / this.trail.length);
            ctx.beginPath();
            ctx.arc(point.x, point.y, size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(251, 191, 36, ${point.alpha * 0.4})`;
            ctx.fill();
        });
        
        // Glow effect
        if (this.glowIntensity > 0) {
            const gradient = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.radius * 2.5);
            gradient.addColorStop(0, `rgba(251, 191, 36, ${this.glowIntensity * 0.6})`);
            gradient.addColorStop(0.5, `rgba(251, 191, 36, ${this.glowIntensity * 0.3})`);
            gradient.addColorStop(1, 'rgba(251, 191, 36, 0)');
            
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius * 2.5, 0, Math.PI * 2);
            ctx.fillStyle = gradient;
            ctx.fill();
        }
        
        // Balle principale avec gradient
        const ballGradient = ctx.createRadialGradient(
            this.x - this.radius * 0.3, 
            this.y - this.radius * 0.3, 
            0,
            this.x, 
            this.y, 
            this.radius
        );
        ballGradient.addColorStop(0, '#fef3c7');
        ballGradient.addColorStop(0.5, '#fbbf24');
        ballGradient.addColorStop(1, '#d97706');
        
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = ballGradient;
        ctx.fill();
        
        // Contour brillant
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.4)';
        ctx.lineWidth = 2;
        ctx.stroke();
        
        // Reflet
        ctx.beginPath();
        ctx.arc(this.x - this.radius * 0.35, this.y - this.radius * 0.35, this.radius * 0.3, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
        ctx.fill();
    }

    isAtBottom() {
        return this.y > plinkoCanvas.height - 50 && Math.abs(this.vy) < 1;
    }

    getFinalSlot() {
        const slotsStart = 20;
        const slotsEnd = plinkoCanvas.width - 20;
        const totalWidth = slotsEnd - slotsStart;
        const slotWidth = totalWidth / 17;
        const slot = Math.floor((this.x - slotsStart) / slotWidth);
        return Math.max(0, Math.min(16, slot));
    }
}

async function dropPlinko() {
    if (plinkoAnimating) {
        alert('Une balle est déjà en train de tomber !');
        return;
    }

    const bet = parseInt(document.getElementById('plinkoBet').value);
    const risk = document.getElementById('plinkoRisk').value;

    if (!bet || bet < 10) {
        alert('Mise minimum : 10$');
        return;
    }

    const btn = document.getElementById('plinkoDropBtn');
    btn.disabled = true;
    plinkoAnimating = true;

    try {
        // Appel API
        const response = await fetch('/api/plinko/drop', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({bet, risk})
        });

        if (!response.ok) {
            const error = await response.json();
            alert(error.error);
            btn.disabled = false;
            plinkoAnimating = false;
            return;
        }

        const data = await response.json();

        // Initialiser si nécessaire
        if (!plinkoCanvas) {
            initPlinkoCanvas();
        }

        // Mettre à jour multiplicateurs
        updatePlinkoMultipliers(risk);

        // Créer et animer la balle
        plinkoBall = new Ball(PLINKO_START_X, PLINKO_START_Y);
        
        await animatePlinko(data.position);

        // Afficher résultat
        const msgDiv = document.getElementById('plinkoMessage');
        msgDiv.className = 'message';

        if (data.result === 'win') {
            msgDiv.classList.add('win');
            msgDiv.innerHTML = `
                ✅ GAGNÉ !<br>
                Multiplicateur : x${data.multiplier}<br>
                <strong style="font-size: 24px;">+${data.profit} $</strong>
            `;
        } else {
            msgDiv.classList.add('lose');
            msgDiv.innerHTML = `
                ❌ PERDU<br>
                Multiplicateur : x${data.multiplier}<br>
                <strong style="font-size: 20px;">${data.profit} $</strong>
            `;
        }

        updateMoneyDisplay(data.money);
        updateStatsDisplay(data.stats);

        setTimeout(() => {
            msgDiv.innerHTML = '';
            btn.disabled = false;
            plinkoAnimating = false;
        }, 4000);

    } catch (error) {
        console.error('Erreur Plinko:', error);
        alert('Erreur de connexion');
        btn.disabled = false;
        plinkoAnimating = false;
    }
}

function initPlinkoCanvas() {
    plinkoCanvas = document.getElementById('plinkoCanvas');
    if (!plinkoCanvas) return;

    plinkoCtx = plinkoCanvas.getContext('2d');

    // Créer les pegs
    plinkoPegs = [];
    for (let row = 0; row < PLINKO_ROWS; row++) {
        const pegsInRow = row + 3;
        const rowY = PLINKO_START_Y + row * PLINKO_SPACING;
        const startX = PLINKO_START_X - ((pegsInRow - 1) * PLINKO_SPACING / 2);

        for (let col = 0; col < pegsInRow; col++) {
            plinkoPegs.push({
                x: startX + col * PLINKO_SPACING,
                y: rowY,
                radius: PLINKO_PEG_RADIUS,
                hit: false
            });
        }
    }

    // Dessiner le board initial
    drawPlinkoBoard();
}

function drawPlinkoBoard() {
    if (!plinkoCtx) return;

    // Clear
    plinkoCtx.clearRect(0, 0, plinkoCanvas.width, plinkoCanvas.height);

    // Dessiner les pegs avec effet 3D
    plinkoPegs.forEach(peg => {
        // Ombre du peg
        plinkoCtx.beginPath();
        plinkoCtx.arc(peg.x + 1, peg.y + 2, peg.radius, 0, Math.PI * 2);
        plinkoCtx.fillStyle = 'rgba(0, 0, 0, 0.3)';
        plinkoCtx.fill();

        // Peg principal avec gradient
        const gradient = plinkoCtx.createRadialGradient(
            peg.x - peg.radius * 0.3,
            peg.y - peg.radius * 0.3,
            0,
            peg.x,
            peg.y,
            peg.radius * 1.5
        );
        
        if (peg.hit) {
            gradient.addColorStop(0, '#fbbf24');
            gradient.addColorStop(1, '#f59e0b');
        } else {
            gradient.addColorStop(0, '#60a5fa');
            gradient.addColorStop(1, '#2563eb');
        }

        plinkoCtx.beginPath();
        plinkoCtx.arc(peg.x, peg.y, peg.radius, 0, Math.PI * 2);
        plinkoCtx.fillStyle = gradient;
        plinkoCtx.fill();

        // Contour brillant
        plinkoCtx.strokeStyle = peg.hit ? 'rgba(251, 191, 36, 0.8)' : 'rgba(96, 165, 250, 0.5)';
        plinkoCtx.lineWidth = 2;
        plinkoCtx.stroke();

        // Reflet
        plinkoCtx.beginPath();
        plinkoCtx.arc(peg.x - peg.radius * 0.4, peg.y - peg.radius * 0.4, peg.radius * 0.4, 0, Math.PI * 2);
        plinkoCtx.fillStyle = 'rgba(255, 255, 255, 0.6)';
        plinkoCtx.fill();
    });
}

async function animatePlinko(finalSlot) {
    return new Promise((resolve) => {
        let stuckFrames = 0;
        let lastY = 0;
        
        const animate = () => {
            drawPlinkoBoard();
            
            if (plinkoBall) {
                plinkoBall.update();
                plinkoBall.draw(plinkoCtx);

                // Détection si la balle est coincée
                if (Math.abs(plinkoBall.y - lastY) < 0.1) {
                    stuckFrames++;
                } else {
                    stuckFrames = 0;
                }
                lastY = plinkoBall.y;

                // Fin si au fond OU coincée trop longtemps
                if (plinkoBall.isAtBottom() || stuckFrames > 60) {
                    const slot = plinkoBall.getFinalSlot();
                    highlightMultiplier(slot);
                    plinkoBall = null;
                    resolve();
                    return;
                }
            }

            requestAnimationFrame(animate);
        };

        animate();
    });
}

function updatePlinkoMultipliers(risk) {
    const multipliers = {
        'low': [1.5, 1.3, 1.1, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.3, 1.5],
        'medium': [5.0, 3.0, 2.0, 1.5, 1.0, 0.5, 0.3, 0.2, 0.1, 0.2, 0.3, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0],
        'high': [50, 20, 5, 2, 0.5, 0.2, 0.1, 0.0, 0.0, 0.0, 0.1, 0.2, 0.5, 2, 5, 20, 50]
    };

    plinkoMultipliers = multipliers[risk];

    const container = document.getElementById('plinkoMultipliers');
    container.innerHTML = plinkoMultipliers.map((mult, i) => {
        let color = '#64748b';
        let bgColor = 'rgba(100, 116, 139, 0.1)';
        
        if (mult >= 10) {
            color = '#fbbf24';
            bgColor = 'rgba(251, 191, 36, 0.2)';
        } else if (mult >= 2) {
            color = '#22c55e';
            bgColor = 'rgba(34, 197, 94, 0.2)';
        } else if (mult >= 1) {
            color = '#3b82f6';
            bgColor = 'rgba(59, 130, 246, 0.2)';
        } else {
            color = '#ef4444';
            bgColor = 'rgba(239, 68, 68, 0.2)';
        }

        return `
            <div id="mult-${i}" style="
                flex: 1;
                padding: 10px 4px;
                background: ${bgColor};
                border: 2px solid ${color};
                border-radius: 8px;
                font-weight: bold;
                color: ${color};
                font-size: 13px;
                text-align: center;
                transition: all 0.3s;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            ">
                x${mult}
            </div>
        `;
    }).join('');
}

function highlightMultiplier(position) {
    const multEl = document.getElementById(`mult-${position}`);
    if (multEl) {
        multEl.style.transform = 'scale(1.3) translateY(-8px)';
        multEl.style.boxShadow = '0 8px 24px currentColor';
        multEl.style.zIndex = '10';
        
        setTimeout(() => {
            multEl.style.transform = 'scale(1) translateY(0)';
            multEl.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.2)';
            multEl.style.zIndex = '1';
        }, 2500);
    }
}

// Initialiser au chargement
document.addEventListener('DOMContentLoaded', () => {
    const plinkoTab = document.getElementById('plinko');
    if (plinkoTab) {
        const observer = new MutationObserver(() => {
            if (plinkoTab.classList.contains('active') && !plinkoCanvas) {
                setTimeout(() => {
                    initPlinkoCanvas();
                    updatePlinkoMultipliers('medium');
                }, 100);
            }
        });
        
        observer.observe(plinkoTab, { attributes: true, attributeFilter: ['class'] });
    }
});



let clickTimes = [];
let clickWarnings = 0;
const CLICK_THRESHOLD = 30; // Max 30 clics par seconde (humainement impossible de maintenir)
const WARNING_THRESHOLD = 3; // 3 avertissements avant blocage
const TIME_WINDOW = 1000; // Fenêtre de 1 seconde

async function doClick() {
    const now = Date.now();
    
    // Nettoyer les clics de plus d'1 seconde
    clickTimes = clickTimes.filter(time => now - time < TIME_WINDOW);
    
    // Ajouter le clic actuel
    clickTimes.push(now);
    
    // Vérifier si autoclick détecté (plus de X clics en 1 seconde)
    if (clickTimes.length > CLICK_THRESHOLD) {
        clickWarnings++;
        
        if (clickWarnings >= WARNING_THRESHOLD) {
            alert('❌ ANTI-AUTOCLICKER\nVous avez été temporairement bloqué pour 30 secondes.\nRaison: Plus de 30 clics par seconde détectés.');
            document.getElementById('clickButton').disabled = true;
            clickTimes = [];
            setTimeout(() => {
                document.getElementById('clickButton').disabled = false;
                clickWarnings = 0;
            }, 30000);
            return;
        } else {
            alert(`⚠️ ANTI-AUTOCLICKER\nAvertissement ${clickWarnings}/${WARNING_THRESHOLD}\n${clickTimes.length} clics en 1 seconde détectés (max: ${CLICK_THRESHOLD})`);
            clickTimes = [];
        }
        return;
    }
    
    try {
        const response = await fetch('/api/clicker/click', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        });
        
        const data = await response.json();
        updateMoneyDisplay(data.money);
        
        const btn = document.getElementById('clickButton');
        btn.classList.add('clicked');
        setTimeout(() => btn.classList.remove('clicked'), 100);
        
        showFloatingNumber(clickPower);
        
    } catch (error) {
        console.error('Erreur clic:', error);
    }
}

