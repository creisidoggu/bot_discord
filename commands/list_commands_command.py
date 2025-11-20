import discord
from discord import app_commands
import logging

logger = logging.getLogger(__name__)

def setup_list_commands_command(tree: app_commands.CommandTree):
    """
    Configura el comando /listar_comandos para mostrar todos los comandos registrados
    
    Args:
        tree: CommandTree del bot
    """
    
    @tree.command(name="listar_comandos", description="Lista todos los comandos registrados")
    async def list_commands_cmd(interaction: discord.Interaction):
        commands_list = []
        
        try:
            # Obtener comandos globales
            global_commands = await tree.fetch_commands()
            if global_commands:
                commands_list.append("**📌 Comandos Globales:**")
                for cmd in global_commands:
                    commands_list.append(f"• `/{cmd.name}` - {cmd.description}")
            
            # Obtener comandos del servidor
            if interaction.guild:
                guild_commands = await tree.fetch_commands(guild=interaction.guild)
                if guild_commands:
                    commands_list.append("\n**🏠 Comandos del Servidor:**")
                    for cmd in guild_commands:
                        commands_list.append(f"• `/{cmd.name}` - {cmd.description}")
            
            if not commands_list:
                commands_list.append("❌ No hay comandos registrados.")
            
            # Crear embed
            embed = discord.Embed(
                title="📋 Lista de Comandos",
                description="\n".join(commands_list),
                color=discord.Color.green()
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            logger.info(f"{interaction.user} listó los comandos disponibles")
            
        except Exception as e:
            logger.error(f"Error al listar comandos: {e}")
            await interaction.response.send_message(
                f"❌ Error al obtener la lista de comandos: {e}",
                ephemeral=True
            )