import discord
from discord import app_commands
import logging

logger = logging.getLogger(__name__)

def setup_character_command(tree: app_commands.CommandTree, webhook_service):
    """
    Configura el comando /personaje para enviar mensajes como personajes
    
    Args:
        tree: CommandTree del bot
        webhook_service: Servicio de gestión de webhooks
    """
    
    @tree.command(name="personaje", description="Envía un mensaje como si fueras un personaje")
    @app_commands.describe(
        nombre="Nombre del personaje",
        mensaje="Mensaje que dirá el personaje",
        imagen_url="URL de la imagen del personaje (opcional)"
    )
    async def personaje_cmd(
        interaction: discord.Interaction,
        nombre: str,
        mensaje: str,
        imagen_url: str = None
    ):
        # Verificar permisos
        if not interaction.user.guild_permissions.manage_webhooks:
            await interaction.response.send_message(
                "❌ No tienes permisos para usar este comando.\n"
                "Necesitas el permiso **Gestionar Webhooks**.",
                ephemeral=True
            )
            logger.warning(f"{interaction.user} intentó usar /personaje sin permisos")
            return
        
        try:
            # Responder inmediatamente para evitar timeout
            await interaction.response.defer(ephemeral=True)
            
            # Obtener o crear webhook
            webhook = await webhook_service.get_or_create_webhook(interaction.channel)
            
            if webhook is None:
                await interaction.followup.send(
                    "❌ No tengo permisos para crear o usar webhooks en este canal.",
                    ephemeral=True
                )
                return
            
            # Enviar mensaje como personaje
            success = await webhook_service.send_as_character(
                webhook=webhook,
                message=mensaje,
                character_name=nombre,
                avatar_url=imagen_url
            )
            
            if success:
                await interaction.followup.send(
                    f"✅ Mensaje enviado como **{nombre}**!",
                    ephemeral=True
                )
                logger.info(f"{interaction.user} envió mensaje como '{nombre}' en {interaction.channel.name}")
            else:
                await interaction.followup.send(
                    "❌ Error al enviar el mensaje como personaje.",
                    ephemeral=True
                )
                
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ No tengo permisos para crear o usar webhooks en este canal.",
                ephemeral=True
            )
            logger.error(f"Sin permisos para webhooks en {interaction.channel.name}")
        except Exception as e:
            logger.error(f"Error en comando personaje: {e}")
            try:
                await interaction.followup.send(
                    f"❌ Ocurrió un error inesperado: {e}",
                    ephemeral=True
                )
            except:
                pass