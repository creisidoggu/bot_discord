import discord
from discord.ext import commands
import asyncio
import logging
from services.data_service import DataService
from services.webhook_service import WebhookService
from handlers.reaction_handler import ReactionHandler
from commands.message_command import setup_message_command
from commands.role_command import setup_role_command
from commands.server_info_command import setup_server_info_command
from commands.list_commands_command import setup_list_commands_command
from commands.character_command import setup_character_command

logger = logging.getLogger(__name__)

class MyBot(commands.Bot):
    """Bot principal de Discord con gestión de roles y personajes"""
    
    def __init__(self, intents: discord.Intents):
        super().__init__(command_prefix="!", intents=intents)
        
        # Inicializar servicios
        self.data_service = DataService()
        self.webhook_service = WebhookService(self)
        self.reaction_handler = ReactionHandler(self, self.data_service)
    
    async def setup_hook(self):
        """Se ejecuta antes de on_ready"""
        # Cargar datos
        self.data_service.load_data()
        logger.info("Datos cargados desde archivos")
        
        # Configurar comandos
        await self.setup_commands()
        logger.info("Comandos configurados")
    
    async def setup_commands(self):
        """Configura y sincroniza todos los comandos del bot"""
        # Limpiar comandos existentes
        self.tree.clear_commands(guild=None)
        logger.info("Comandos globales eliminados")
        
        for guild in self.guilds:
            guild_obj = discord.Object(id=guild.id)
            self.tree.clear_commands(guild=guild_obj)
            logger.info(f"Comandos eliminados para el servidor {guild.name}")
        
        await asyncio.sleep(2)
        
        # Sincronizar para eliminar comandos antiguos
        try:
            await self.tree.sync()
            logger.info("Sincronización global completada para eliminar comandos")
            
            for guild in self.guilds:
                guild_obj = discord.Object(id=guild.id)
                await self.tree.sync(guild=guild_obj)
                logger.info(f"Sincronización completada para eliminar comandos en {guild.name}")
        except Exception as e:
            logger.error(f"Error en la sincronización inicial: {e}")
        
        await asyncio.sleep(2)
        
        # Registrar nuevos comandos
        setup_message_command(self.tree, self.data_service)
        setup_role_command(self.tree, self.data_service)
        setup_server_info_command(self.tree)
        setup_list_commands_command(self.tree)
        setup_character_command(self.tree, self.webhook_service)
        
        logger.info("Preparando para sincronizar comandos...")
        await asyncio.sleep(1)
        
        # Sincronizar nuevos comandos
        try:
            await self.tree.sync()
            logger.info("Comandos globales sincronizados")
            
            for guild in self.guilds:
                guild_obj = discord.Object(id=guild.id)
                self.data_service.add_guild(guild.id, guild.name)
                await self.tree.sync(guild=guild_obj)
                logger.info(f"Comandos sincronizados para {guild.name}")
        except Exception as e:
            logger.error(f"Error en la sincronización final: {e}")
    
    async def on_ready(self):
        """Evento que se ejecuta cuando el bot está listo"""
        logger.info(f"Bot listo y conectado como {self.user}. ID: {self.user.id}")
        logger.info(f"Presente en {len(self.guilds)} servidores:")
        
        for guild in self.guilds:
            logger.info(f"- {guild.name} (ID: {guild.id})")
            self.data_service.add_guild(guild.id, guild.name)
        
        self.data_service.save_data()
    
    async def on_guild_join(self, guild: discord.Guild):
        """Evento cuando el bot se une a un nuevo servidor"""
        logger.info(f"Bot unido a nuevo servidor: {guild.name} (ID: {guild.id})")
        self.data_service.add_guild(guild.id, guild.name)
        
        # Sincronizar comandos para este servidor
        guild_obj = discord.Object(id=guild.id)
        await self.tree.sync(guild=guild_obj)
        logger.info(f"Comandos sincronizados para {guild.name}")
    
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Evento cuando se añade una reacción"""
        await self.reaction_handler.handle_reaction_add(payload)
    
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """Evento cuando se remueve una reacción"""
        await self.reaction_handler.handle_reaction_remove(payload)