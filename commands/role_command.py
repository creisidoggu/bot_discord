import discord
from discord import app_commands
import logging

logger = logging.getLogger(__name__)

def setup_role_command(tree: app_commands.CommandTree, data_service):
    """
    Configura el comando /role_add para añadir roles a mensajes
    
    Args:
        tree: CommandTree del bot
        data_service: Servicio de gestión de datos
    """
    
    @tree.command(name="role_add", description="Añade un rol a un mensaje de reacción")
    @app_commands.describe(
        message_id="ID del mensaje donde añadir el rol",
        role="Rol a asignar",
        emoji="Emoji para la reacción",
        description="Descripción del rol"
    )
    async def role_add_cmd(
        interaction: discord.Interaction,
        message_id: str,
        role: discord.Role,
        emoji: str,
        description: str
    ):
        guild_id = interaction.guild_id
        
        # Validar ID del mensaje
        try:
            message_id_int = int(message_id)
        except ValueError:
            await interaction.response.send_message(
                "❌ El ID del mensaje debe ser un número válido.",
                ephemeral=True
            )
            return
        
        # Obtener servidor
        guild_obj = interaction.guild
        if guild_obj is None:
            await interaction.response.send_message(
                "❌ No puedo acceder al servidor.",
                ephemeral=True
            )
            return
        
        # Verificar jerarquía de roles
        bot_member = guild_obj.me
        if role >= bot_member.top_role:
            await interaction.response.send_message(
                "❌ No puedo asignar ese rol porque está al mismo nivel o por encima de mi rol.\n"
                "Por favor, ajusta la jerarquía de roles en el servidor.",
                ephemeral=True
            )
            return
        
        # Obtener mensaje
        channel = interaction.channel
        try:
            msg = await channel.fetch_message(message_id_int)
        except discord.NotFound:
            await interaction.response.send_message(
                "❌ No se encontró el mensaje con ese ID en este canal.",
                ephemeral=True
            )
            return
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ No tengo permiso para leer ese mensaje.",
                ephemeral=True
            )
            return
        except discord.HTTPException:
            await interaction.response.send_message(
                "❌ Error al obtener el mensaje.",
                ephemeral=True
            )
            return
        
        # Actualizar embed del mensaje
        if msg.embeds:
            embed = msg.embeds[0]
            embed.add_field(name=f"{emoji} {role.name}", value=description, inline=False)
        else:
            embed = discord.Embed(
                title="Roles disponibles",
                color=discord.Color.blue()
            )
            embed.add_field(name=f"{emoji} {role.name}", value=description, inline=False)
        
        await msg.edit(embed=embed)
        
        # Añadir reacción al mensaje
        try:
            await msg.add_reaction(emoji)
        except discord.HTTPException:
            await interaction.response.send_message(
                "❌ No pude añadir la reacción. ¿Es un emoji válido y tengo permisos?",
                ephemeral=True
            )
            return
        
        # Guardar en el servicio de datos
        data_service.add_reaction_role(message_id_int, emoji, role.id)
        
        await interaction.response.send_message(
            f"✅ Rol **{role.name}** añadido con el emoji {emoji} al mensaje `{message_id}`.",
            ephemeral=True
        )
        logger.info(f"Rol {role.name} añadido al mensaje {message_id} por {interaction.user}")