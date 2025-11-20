import json
import os
import logging

logger = logging.getLogger(__name__)

class DataService:
    """Servicio para gestionar la persistencia de datos"""
    
    def __init__(self, reaction_roles_file="reaction_roles.json", guilds_file="guilds.json"):
        self.reaction_roles_file = reaction_roles_file
        self.guilds_file = guilds_file
        self.reaction_role_data = {}
        self.guild_data = {}
    
    def load_data(self):
        """Carga los datos desde los archivos JSON"""
        self._load_reaction_roles()
        self._load_guilds()
        logger.info("Datos cargados desde archivos")
    
    def save_data(self):
        """Guarda los datos en los archivos JSON"""
        self._save_reaction_roles()
        self._save_guilds()
        logger.info("Datos guardados en archivos")
    
    def _load_reaction_roles(self):
        """Carga los datos de roles por reacción"""
        if os.path.isfile(self.reaction_roles_file):
            with open(self.reaction_roles_file, "r", encoding="utf-8") as f:
                self.reaction_role_data = json.load(f)
                self.reaction_role_data = {int(k): v for k, v in self.reaction_role_data.items()}
        else:
            self.reaction_role_data = {}
    
    def _load_guilds(self):
        """Carga los datos de servidores"""
        if os.path.isfile(self.guilds_file):
            with open(self.guilds_file, "r", encoding="utf-8") as f:
                self.guild_data = json.load(f)
                self.guild_data = {int(k): v for k, v in self.guild_data.items()}
        else:
            self.guild_data = {}
    
    def _save_reaction_roles(self):
        """Guarda los datos de roles por reacción"""
        with open(self.reaction_roles_file, "w", encoding="utf-8") as f:
            json.dump(self.reaction_role_data, f, ensure_ascii=False, indent=4)
    
    def _save_guilds(self):
        """Guarda los datos de servidores"""
        with open(self.guilds_file, "w", encoding="utf-8") as f:
            json.dump(self.guild_data, f, ensure_ascii=False, indent=4)
    
    def add_reaction_role(self, message_id: int, emoji: str, role_id: int):
        """Añade un rol a un mensaje de reacción"""
        if message_id not in self.reaction_role_data:
            self.reaction_role_data[message_id] = {}
        self.reaction_role_data[message_id][emoji] = role_id
        self.save_data()
    
    def get_role_for_reaction(self, message_id: int, emoji: str):
        """Obtiene el ID del rol asociado a una reacción"""
        if message_id in self.reaction_role_data:
            return self.reaction_role_data[message_id].get(emoji)
        return None
    
    def add_message_for_roles(self, message_id: int):
        """Registra un mensaje para gestionar roles"""
        self.reaction_role_data[message_id] = {}
        self.save_data()
    
    def add_guild(self, guild_id: int, guild_name: str):
        """Añade información de un servidor"""
        self.guild_data[guild_id] = {"name": guild_name}
        self.save_data()