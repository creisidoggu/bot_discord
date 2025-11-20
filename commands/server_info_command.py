import discord
from discord import app_commands
import logging

logger = logging.getLogger(__name__)

def setup_server_info_command(tree: app_commands.CommandTree):
    """
    Configura el comando /servidor_info para mostrar información del servidor
    
    Args:
        tree: CommandTree del bot
    """
    
    @tree.command(name="servidor_info", description="Muestra información sobre el servidor actual")
    async def servidor_info_cmd(interaction: discord.Interaction):
        guild = interaction.guild
        
        if guild is None:
            await interaction.response.send_message(
                "❌ Este comando solo se puede usar en un servidor.",
                ephemeral=True
            )
            return
        
        # Crear embed con información del servidor
        embed = discord.Embed(
            title=f"Información del Servidor: {guild.name}",
            description=f"ID: `{guild.id}`",
            color=discord.Color.blue(),
            timestamp=guild.created_at
        )
        
        # Añadir campos de información
        embed.add_field(
            name="👑 Dueño",
            value=f"{guild.owner.mention}" if guild.owner else "Desconocido",
            inline=True
        )
        embed.add_field(
            name="👥 Miembros",
            value=f"{guild.member_count}",
            inline=True
        )
        embed.add_field(
            name="🎭 Roles",
            value=f"{len(guild.roles)}",
            inline=True
        )
        embed.add_field(
            name="💬 Canales",
            value=f"{len(guild.channels)}",
            inline=True
        )
        embed.add_field(
            name="😀 Emojis",
            value=f"{len(guild.emojis)}",
            inline=True
        )
        embed.add_field(
            name="🚀 Nivel de impulso",
            value=f"{guild.premium_tier} ({guild.premium_subscription_count} impulsos)",
            inline=True
        )
        
        # Añadir icono del servidor si existe
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        embed.set_footer(text="Servidor creado el")
        
        await interaction.response.send_message(embed=embed)
        logger.info(f"{interaction.user} consultó información del servidor {guild.name}")