import discord
from discord import app_commands
import logging

logger = logging.getLogger(__name__)

def setup_message_command(tree: app_commands.CommandTree, data_service):
    """
    Configura el comando /message para crear mensajes de roles
    
    Args:
        tree: CommandTree del bot
        data_service: Servicio de gestión de datos
    """
    
    @tree.command(name="message", description="Crea mensajes para gestionar roles con reacciones")
    @app_commands.describe(action="Acción: create")
    async def message_cmd(interaction: discord.Interaction, action: str):
        action = action.lower()
        
        try:
            if action == "create":
                # Crear embed para el mensaje de roles
                embed = discord.Embed(
                    title="¡Reacciona para obtener un rol!",
                    description="Usa `/role_add` para añadir roles a este mensaje.",
                    color=discord.Color.blue()
                )
                
                # Enviar mensaje
                msg = await interaction.channel.send(embed=embed)
                
                # Registrar mensaje en el servicio de datos
                data_service.add_message_for_roles(msg.id)
                
                await interaction.response.send_message(
                    f"✅ Mensaje creado con ID: `{msg.id}`\nUsa este ID con `/role_add` para añadir roles.",
                    ephemeral=True
                )
                logger.info(f"Mensaje de roles creado con ID {msg.id} por {interaction.user}")
            else:
                await interaction.response.send_message(
                    "❌ Acción no reconocida. Usa `create`.",
                    ephemeral=True
                )
        except Exception as e:
            logger.error(f"Error en comando message: {e}")
            await interaction.response.send_message(
                f"❌ Ocurrió un error: {e}",
                ephemeral=True
            )