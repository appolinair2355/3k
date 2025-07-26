# Joker's Telegram Bot - Deployment Package

Un bot Telegram sophistiqué pour une communauté de 3K développeurs avec système de prédiction de cartes automatique.

## 🚀 Déploiement Rapide sur Replit

### 1. Configuration Initiale
1. Créez un nouveau projet Python sur Replit
2. Extrayez tous les fichiers de ce package ZIP dans votre projet
3. Ajoutez votre token de bot dans les Secrets

### 2. Variables d'Environnement Requises
```
BOT_TOKEN=votre_token_telegram_bot
PORT=10000
```

### 3. Démarrage
```bash
python main.py
```

## 📋 Fonctionnalités

### 🎯 Système de Prédiction Automatique
- Détection automatique des combinaisons de 3 cartes différentes
- Prédictions basées sur l'analyse des messages de jeu
- Vérification automatique des résultats
- Statistiques de précision en temps réel

### 👥 Gestion Communautaire
- Accueil automatique des nouveaux membres
- Commandes d'aide et d'information
- Limitation de débit anti-spam
- Interface en français pour la communauté

### 🛠️ Architecture Technique
- Python 3.11 + asyncio
- Architecture modulaire et événementielle
- Logging complet et gestion d'erreurs
- Optimisé pour déploiement Replit

## 📁 Structure du Projet

```
jokers-telegram-bot/
├── main.py              # Point d'entrée principal
├── bot.py               # Contrôleur du bot
├── handlers.py          # Gestionnaires d'événements
├── card_predictor.py    # Système de prédiction
├── config.py            # Configuration
├── requirements.txt     # Dépendances Python
├── .replit             # Configuration Replit
├── replit.nix          # Environnement Nix
├── run.sh              # Script de démarrage
└── README.md           # Documentation
```

## 🎮 Commandes Disponibles

- `/start` - Message de bienvenue
- `/help` - Aide et documentation
- `/about` - Informations sur le bot
- `/dev` - Informations techniques
- `/stats` - Statistiques des prédictions
- `/deploy` - Générer package de déploiement

## 🃏 Système de Cartes

Le bot reconnaît les symboles de cartes suivants :
- ♠️ Pique
- ♥️ Cœur  
- ♣️ Trèfle
- ♦️ Carreau

## 📊 Prédictions

Le bot analyse automatiquement les messages contenant des numéros de jeu (#N1234) et fait des prédictions quand il détecte :
- 3 cartes différentes dans le premier parenthèses, OU
- 3 cartes différentes dans le deuxième parenthèses

La vérification se fait quand le message édité contient :
- ✅ ou 🔰 (symboles de succès) ET
- 3 cartes ou plus dans le premier parenthèses

## 👨‍💻 Développé par Kouamé

Spécialement conçu pour la communauté des 3K développeurs.

---

**Version :** 2.0  
**Dernière mise à jour :** Juillet 2025  
**Plateforme :** Replit Optimized
