import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
from bot.my_bot import MyBot
from utils.logger import setup_logger

# Configurar logger
setup_logger()
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv("api_key")

def main():
    """Punto de entrada principal del bot"""
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    intents.reactions = True
    intents.guilds = True

    bot = MyBot(intents=intents)
    
    try:
        bot.run(TOKEN)
    except Exception as e:
        logger.error(f"Error al iniciar el bot: {e}")

if __name__ == "__main__":
    main()