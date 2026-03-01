"""
Configuration settings for Joker's Telegram Bot - Deployment Version
"""
import os

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Port configuration for deployment
PORT = int(os.getenv('PORT', 10000))

# Message templates (Correction: Nommé GREETING_MESSAGE pour correspondre aux handlers)
GREETING_MESSAGE = """
👋 Bienvenue dans la communauté des développeurs !

Je suis Joker, votre bot assistant pour ce groupe de 3K développeurs.

Commandes disponibles :
• /help - Afficher l'aide
• /about - À propos du bot
• /dev - Informations pour développeurs
• /stats - Statistiques des prédictions
• /deploy - Package de déploiement

🎯 **Système de prédiction de cartes automatique :**
Le bot analyse automatiquement vos messages de jeu et fait des prédictions quand il détecte 3 cartes différentes !
"""

HELP_MESSAGE = """
🆘 **Aide - Joker's Bot**

**Commandes disponibles :**
• `/start` - Message de bienvenue
• `/help` - Afficher cette aide
• `/about` - Informations sur le bot
• `/dev` - Informations techniques
• `/stats` - Statistiques des prédictions
• `/deploy` - Générer package de déploiement

**🎯 Système de prédiction automatique :**
Le bot surveille vos messages de jeu et fait automatiquement des prédictions quand il détecte des combinaisons valides de 3 cartes différentes.

**Symboles de cartes supportés :** ♠️ ♥️ ♣️ ♦️

Développé avec ❤️ pour la communauté des développeurs
"""

ABOUT_MESSAGE = """
🤖 **Joker's Telegram Bot v2.0**

**Développé par :** Kouamé
**Communauté :** 3K Développeurs
**Langage :** Python 3.11
**Framework :** python-telegram-bot v20.7

**Fonctionnalités :**
✅ Système de prédiction de cartes automatique
✅ Gestion des nouveaux membres
✅ Limitation de débit anti-spam
✅ Statistiques de prédiction en temps réel
✅ Architecture modulaire et extensible

**Déploiement :** Optimisé pour Render
**Port :** 10000 (configurable)

🔧 Bot opensource développé spécialement pour cette communauté
"""

DEV_MESSAGE = """
👨‍💻 **Informations Techniques**

**Architecture :**
• Python 3.11 + asyncio
• python-telegram-bot v20.7
• Architecture modulaire événementielle
• Logging complet (fichier + console)

**Modules :**
• `bot.py` - Contrôleur principal
• `handlers.py` - Gestionnaires d'événements
• `card_predictor.py` - Système de prédiction
• `config.py` - Configuration centralisée

**Variables d'environnement :**
• `BOT_TOKEN` - Token du bot Telegram (requis)
• `PORT` - Port d'écoute (défaut: 10000)

**Déploiement :**
Optimisé pour Render avec support complet des workflows.
"""

# Rate limiting settings
RATE_LIMIT_MESSAGES = 5
RATE_LIMIT_WINDOW = 60  # seconds

# Prediction system settings
VALID_CARD_SYMBOLS = ['♠️', '♥️', '♣️', '♦️']
MAX_PREDICTION_HISTORY = 100
