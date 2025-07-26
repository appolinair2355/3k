"""
Main bot class for Joker's Telegram Bot
"""

import logging
import signal
import sys
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    filters, ContextTypes
)
from telegram import Update
from config import BOT_TOKEN
from handlers import (
    handle_new_chat_members, start_command, help_command,
    about_command, dev_command, handle_message, handle_edited_message,
    stats_command, deploy_command, error_handler
)

logger = logging.getLogger(__name__)

class TelegramBot:
    """Main Telegram Bot class"""
    
    def __init__(self):
        """Initialize the bot"""
        self.application = None
        self.setup_bot()
    
    def start(self):
        """Start the bot using run_polling"""
        try:
            if not self.application:
                raise RuntimeError("Bot application not properly initialized")
                
            # Get bot info and start
            logger.info("Starting Joker's Telegram Bot...")
            self.application.run_polling(
                poll_interval=1.0,
                timeout=10,
                read_timeout=10,
                write_timeout=10,
                connect_timeout=10,
                pool_timeout=10
            )
            
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise
    
    def setup_bot(self):
        """Setup the bot application and handlers"""
        try:
            # Create application
            self.application = Application.builder().token(BOT_TOKEN).build()
            
            # Add command handlers
            self.application.add_handler(CommandHandler("start", start_command))
            self.application.add_handler(CommandHandler("help", help_command))
            self.application.add_handler(CommandHandler("about", about_command))
            self.application.add_handler(CommandHandler("dev", dev_command))
            self.application.add_handler(CommandHandler("stats", stats_command))
            self.application.add_handler(CommandHandler("deploy", deploy_command))
            
            # Add message handlers
            self.application.add_handler(
                MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_chat_members)
            )
            self.application.add_handler(
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
            )
            
            # Add edited message handler
            self.application.add_handler(
                MessageHandler(filters.UpdateType.EDITED_MESSAGE, handle_edited_message)
            )
            
            # Add error handler
            self.application.add_error_handler(error_handler)
            
            logger.info("Bot handlers configured successfully")
            
        except Exception as e:
            logger.error(f"Failed to setup bot: {e}")
            raise
    

