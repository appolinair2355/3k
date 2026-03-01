"""
Event handlers for the Telegram bot
"""

import logging
from datetime import datetime, timedelta
from collections import defaultdict
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from config import (
    GREETING_MESSAGE, WELCOME_MESSAGE, HELP_MESSAGE, 
    ABOUT_MESSAGE, DEV_MESSAGE, MAX_MESSAGES_PER_MINUTE, RATE_LIMIT_WINDOW
)
from card_predictor import card_predictor

logger = logging.getLogger(__name__)

# Rate limiting storage
user_message_counts = defaultdict(list)

def is_rate_limited(user_id: int) -> bool:
    """Check if user is rate limited"""
    now = datetime.now()
    user_messages = user_message_counts[user_id]

    # Remove old messages outside the window
    user_messages[:] = [msg_time for msg_time in user_messages 
                       if now - msg_time < timedelta(seconds=RATE_LIMIT_WINDOW)]

    # Check if user exceeded limit
    if len(user_messages) >= MAX_MESSAGES_PER_MINUTE:
        return True

    # Add current message time
    user_messages.append(now)
    return False

async def handle_new_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle when bot is added to a channel or group"""
    try:
        if update.message and update.message.new_chat_members:
            for member in update.message.new_chat_members:
                if member.id == context.bot.id:
                    chat = update.effective_chat
                    if chat:
                        logger.info(f"Bot added to {chat.type}: {chat.title} (ID: {chat.id})")
                        await context.bot.send_message(
                            chat_id=chat.id,
                            text=GREETING_MESSAGE
                        )
                        logger.info(f"Greeting sent to {chat.title}")
                    break
    except Exception as e:
        logger.error(f"Error in handle_new_chat_members: {e}")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    try:
        user = update.effective_user
        if user and is_rate_limited(user.id):
            if update.message:
                await update.message.reply_text("⏰ Veuillez patienter avant d'envoyer une autre commande.")
            return

        if update.message:
            await update.message.reply_text(WELCOME_MESSAGE)
    except Exception as e:
        logger.error(f"Error in start_command: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    try:
        user = update.effective_user
        if user and is_rate_limited(user.id):
            if update.message:
                await update.message.reply_text("⏰ Veuillez patienter avant d'envoyer une autre commande.")
            return
        if update.message:
            await update.message.reply_text(HELP_MESSAGE)
    except Exception as e:
        logger.error(f"Error in help_command: {e}")

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /about command"""
    try:
        user = update.effective_user
        if user and is_rate_limited(user.id):
            return
        if update.message:
            await update.message.reply_text(ABOUT_MESSAGE)
    except Exception as e:
        logger.error(f"Error in about_command: {e}")

async def dev_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /dev command"""
    try:
        user = update.effective_user
        if user and is_rate_limited(user.id):
            return
        if update.message:
            await update.message.reply_text(DEV_MESSAGE)
    except Exception as e:
        logger.error(f"Error in dev_command: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular messages and card predictions"""
    try:
        user = update.effective_user
        chat = update.effective_chat
        message = update.message

        if user and is_rate_limited(user.id):
            return

        if user and chat and message and message.text:
            if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL]:
                await process_card_message(update, context, message.text)

        if chat and message and chat.type == ChatType.PRIVATE:
            await message.reply_text(
                "🎭 Salut ! Je suis le bot de Joker.\n"
                "Utilisez /help pour voir mes commandes disponibles."
            )
    except Exception as e:
        logger.error(f"Error in handle_message: {e}")

async def handle_edited_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle edited messages"""
    try:
        user = update.effective_user
        chat = update.effective_chat
        message = update.edited_message

        if user and is_rate_limited(user.id):
            return

        if chat and message and message.text:
            if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL]:
                await process_card_message_for_verification(update, context, message.text)
    except Exception as e:
        logger.error(f"Error in handle_edited_message: {e}")

async def process_card_message(update: Update, context: ContextTypes.DEFAULT_TYPE, message_text: str) -> None:
    """Process message for card predictions"""
    try:
        should_predict, game_number, combination = card_predictor.should_predict(message_text)
        if should_predict and game_number is not None:
            prediction = card_predictor.make_prediction(game_number, combination)
            next_game = game_number + 1
            if update.effective_chat:
                sent_message = await context.bot.send_message(chat_id=update.effective_chat.id, text=prediction)
                card_predictor.sent_predictions[next_game] = {
                    'chat_id': sent_message.chat_id,
                    'message_id': sent_message.message_id
                }

        verification_result = card_predictor.verify_prediction(message_text)
        if verification_result and update.effective_chat:
            if verification_result['type'] == 'update_message':
                predicted_game = verification_result['predicted_game']
                if predicted_game in card_predictor.sent_predictions:
                    message_info = card_predictor.sent_predictions[predicted_game]
                    await context.bot.edit_message_text(
                        chat_id=message_info['chat_id'],
                        message_id=message_info['message_id'],
                        text=verification_result['new_message']
                    )
    except Exception as e:
        logger.error(f"Error in process_card_message: {e}")

async def process_card_message_for_verification(update: Update, context: ContextTypes.DEFAULT_TYPE, message_text: str) -> None:
    """Process edited message for verification"""
    # Logique similaire à process_card_message pour les messages modifiés
    await process_card_message(update, context, message_text)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /stats command"""
    try:
        stats = card_predictor.get_prediction_stats()
        stats_message = f"📊 **Stats**\n\nTotal: {stats['total']}\nPrécision: {stats['accuracy']:.1f}%"
        if update.message:
            await update.message.reply_text(stats_message)
    except Exception as e:
        logger.error(f"Error in stats_command: {e}")

async def deploy_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /deploy command"""
    if update.message:
        await update.message.reply_text("🚀 Commande de déploiement activée.")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors"""
    logger.error(f"Erreur : {context.error}")
