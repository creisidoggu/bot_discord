import logging
import os
from datetime import datetime

def setup_logger():
    """Configura el sistema de logging del bot"""
    # Crear la carpeta "logs" si no existe
    os.makedirs("logs", exist_ok=True)
    
    # Obtener la fecha actual para el nombre del archivo
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    
    # Configuración básica de logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(f"./logs/bot_{fecha_actual}.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )