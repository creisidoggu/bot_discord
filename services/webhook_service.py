import discord
import logging

logger = logging.getLogger(__name__)

class WebhookService:
    """Servicio para gestionar webhooks de Discord"""
    
    def __init__(self, bot):
        self.bot = bot
    
    async def get_or_create_webhook(self, channel: discord.TextChannel):
        """
        Obtiene un webhook existente del bot o crea uno nuevo
        
        Args:
            channel: Canal donde obtener/crear el webhook
            
        Returns:
            Webhook de Discord o None si hay error
        """
        try:
            webhooks = await channel.webhooks()
            
            # Buscar webhook existente del bot
            for webhook in webhooks:
                if webhook.user == self.bot.user:
                    return webhook
            
            # Si no existe, crear uno nuevo
            webhook = await channel.create_webhook(name="Bot Personajes")
            logger.info(f"Webhook creado en el canal {channel.name}")
            return webhook
            
        except discord.Forbidden:
            logger.error(f"Sin permisos para crear webhook en {channel.name}")
            return None
        except Exception as e:
            logger.error(f"Error al obtener/crear webhook: {e}")
            return None
    
    async def send_as_character(self, webhook: discord.Webhook, message: str, 
                               character_name: str, avatar_url: str = None):
        """
        Envía un mensaje usando un webhook como un personaje
        
        Args:
            webhook: Webhook a usar
            message: Contenido del mensaje
            character_name: Nombre del personaje
            avatar_url: URL del avatar del personaje (opcional)
            
        Returns:
            True si se envió correctamente, False si hubo error
        """
        try:
            await webhook.send(
                content=message,
                username=character_name,
                avatar_url=avatar_url if avatar_url else None
            )
            logger.info(f"Mensaje enviado como {character_name}")
            return True
            
        except discord.HTTPException as e:
            logger.error(f"Error al enviar mensaje como personaje: {e}")
            return False