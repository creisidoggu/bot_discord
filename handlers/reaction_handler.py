import discord
import logging

logger = logging.getLogger(__name__)

class ReactionHandler:
    """Manejador de eventos de reacciones para asignar/remover roles"""
    
    def __init__(self, bot, data_service):
        self.bot = bot
        self.data_service = data_service
    
    async def handle_reaction_add(self, payload: discord.RawReactionActionEvent):
        """
        Maneja el evento de añadir una reacción
        
        Args:
            payload: Información del evento de reacción
        """
        # Ignorar reacciones del bot
        if payload.user_id == self.bot.user.id:
            return
        
        message_id = payload.message_id
        emoji = str(payload.emoji)
        
        # Verificar si hay un rol asociado a esta reacción
        role_id = self.data_service.get_role_for_reaction(message_id, emoji)
        if role_id is None:
            return
        
        # Obtener objetos de Discord
        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return
        
        role = guild.get_role(role_id)
        if role is None:
            logger.warning(f"Rol {role_id} no encontrado en {guild.name}")
            return
        
        member = guild.get_member(payload.user_id)
        if member is None:
            return
        
        # Verificar jerarquía de roles
        if not self._can_manage_role(guild, role):
            logger.warning(f"No puedo asignar el rol {role.name} porque está por encima de mi rol")
            return
        
        # Asignar rol
        try:
            await member.add_roles(role)
            logger.info(f"Asignado rol {role.name} a {member.display_name} en {guild.name}")
        except discord.Forbidden:
            logger.error("Sin permisos para asignar roles")
        except Exception as e:
            logger.error(f"Error al asignar rol: {e}")
    
    async def handle_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """
        Maneja el evento de remover una reacción
        
        Args:
            payload: Información del evento de reacción
        """
        message_id = payload.message_id
        emoji = str(payload.emoji)
        
        # Verificar si hay un rol asociado a esta reacción
        role_id = self.data_service.get_role_for_reaction(message_id, emoji)
        if role_id is None:
            return
        
        # Obtener objetos de Discord
        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return
        
        role = guild.get_role(role_id)
        if role is None:
            return
        
        member = guild.get_member(payload.user_id)
        if member is None:
            return
        
        # Verificar jerarquía de roles
        if not self._can_manage_role(guild, role):
            logger.warning(f"No puedo remover el rol {role.name} porque está por encima de mi rol")
            return
        
        # Remover rol
        try:
            await member.remove_roles(role)
            logger.info(f"Removido rol {role.name} de {member.display_name} en {guild.name}")
        except discord.Forbidden:
            logger.error("Sin permisos para remover roles")
        except Exception as e:
            logger.error(f"Error al remover rol: {e}")
    
    def _can_manage_role(self, guild: discord.Guild, role: discord.Role) -> bool:
        """
        Verifica si el bot puede gestionar un rol específico
        
        Args:
            guild: Servidor de Discord
            role: Rol a verificar
            
        Returns:
            True si el bot puede gestionar el rol, False en caso contrario
        """
        bot_member = guild.me
        return role < bot_member.top_role