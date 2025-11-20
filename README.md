# 🤖 Discord Bot - Gestión de Roles y Personajes

Bot de Discord multifuncional desarrollado en Python que permite gestionar roles mediante reacciones y enviar mensajes personalizados como diferentes personajes.

## 📋 Características

### 🎭 Sistema de Roles por Reacción
- Crea mensajes interactivos donde los usuarios pueden reaccionar para obtener roles
- Asignación y eliminación automática de roles según las reacciones
- Verificación de jerarquía de roles para evitar errores de permisos
- Persistencia de datos entre reinicios

### 👤 Sistema de Personajes
- Envía mensajes como si fueran de un personaje específico
- Personaliza nombre y avatar para cada mensaje
- Perfecto para roleplay, storytelling o anuncios creativos

### 📊 Información del Servidor
- Consulta estadísticas y detalles del servidor
- Visualización de miembros, roles, canales y más

### 🔧 Utilidades
- Listado de comandos disponibles
- Sistema de logging detallado
- Persistencia automática de datos

## 🏗️ Arquitectura del Proyecto

El proyecto sigue los principios **SOLID** para mantener un código limpio, mantenible y escalable:

```
proyecto_bot/
├── main.py                          # Punto de entrada del bot
├── .env                             # Variables de entorno (TOKEN)
├── requirements.txt                 # Dependencias del proyecto
│
├── bot/
│   ├── __init__.py
│   └── my_bot.py                    # Clase principal del bot
│
├── commands/                        # Comandos slash del bot
│   ├── __init__.py
│   ├── message_command.py           # /message - Crear mensajes de roles
│   ├── role_command.py              # /role_add - Añadir roles
│   ├── server_info_command.py      # /servidor_info - Info del servidor
│   ├── list_commands_command.py    # /listar_comandos - Lista comandos
│   └── character_command.py         # /personaje - Mensajes como personaje
│
├── handlers/                        # Manejadores de eventos
│   ├── __init__.py
│   └── reaction_handler.py          # Gestión de reacciones
│
├── services/                        # Lógica de negocio
│   ├── __init__.py
│   ├── data_service.py              # Persistencia de datos (JSON)
│   └── webhook_service.py           # Gestión de webhooks
│
└── utils/                           # Utilidades
    ├── __init__.py
    └── logger.py                    # Configuración de logging
```

### 📦 Módulos Principales

#### **bot/my_bot.py**
Clase principal que hereda de `commands.Bot`. Inicializa servicios, configura eventos y coordina la sincronización de comandos.

#### **services/data_service.py**
Gestiona la persistencia de datos en archivos JSON:
- `reaction_roles.json` - Mapeo de mensajes, emojis y roles
- `guilds.json` - Información de servidores

#### **services/webhook_service.py**
Maneja la creación y uso de webhooks para el sistema de personajes.

#### **handlers/reaction_handler.py**
Procesa eventos de reacciones (añadir/quitar) y gestiona la asignación de roles.

#### **commands/**
Cada comando está en su propio archivo siguiendo el principio de **Single Responsibility**.

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Una aplicación de bot en Discord Developer Portal

### Paso 1: Clonar o Descargar el Proyecto

```bash
git clone <url-del-repositorio>
cd proyecto_bot
```

### Paso 2: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 3: Configurar el Bot

1. Ve al [Discord Developer Portal](https://discord.com/developers/applications)
2. Crea una nueva aplicación
3. Ve a la sección "Bot" y crea un bot
4. Copia el token del bot
5. Crea un archivo `.env` en la raíz del proyecto:

```env
api_key=TU_TOKEN_AQUI
```

### Paso 4: Configurar Permisos

En el Developer Portal, ve a "OAuth2 > URL Generator" y selecciona:

**Scopes:**
- `bot`
- `applications.commands`

**Bot Permissions:**
- Manage Roles
- Manage Webhooks
- Send Messages
- Manage Messages
- Add Reactions
- Read Message History
- View Channels

Copia la URL generada e invita al bot a tu servidor.

### Paso 5: Ejecutar el Bot

```bash
python main.py
```

## 📖 Uso de Comandos

### `/message create`
Crea un mensaje embed para gestionar roles con reacciones.

**Uso:**
```
/message action:create
```

**Ejemplo:**
1. Ejecuta el comando en un canal
2. El bot creará un mensaje y te dará su ID
3. Usa ese ID con `/role_add` para añadir roles

---

### `/role_add`
Añade un rol a un mensaje de reacción existente.

**Parámetros:**
- `message_id` - ID del mensaje (obtenido con `/message create`)
- `role` - Rol a asignar
- `emoji` - Emoji para la reacción
- `description` - Descripción del rol

**Uso:**
```
/role_add message_id:123456789 role:@Jugador emoji:🎮 description:"Rol para jugadores"
```

**Ejemplo completo:**
```
1. /message create
   → El bot responde: "Mensaje creado con ID: 123456789"

2. /role_add message_id:123456789 role:@Gamer emoji:🎮 description:"Amantes de videojuegos"
3. /role_add message_id:123456789 role:@Artista emoji:🎨 description:"Creadores de contenido"
4. /role_add message_id:123456789 role:@Músico emoji:🎵 description:"Productores musicales"
```

Los usuarios ahora pueden reaccionar con 🎮, 🎨 o 🎵 para obtener los roles correspondientes.

---

### `/personaje`
Envía un mensaje como si fuera de un personaje con nombre e imagen personalizados.

**Parámetros:**
- `nombre` - Nombre del personaje
- `mensaje` - Contenido del mensaje
- `imagen_url` (opcional) - URL de la imagen del avatar

**Uso:**
```
/personaje nombre:"Gandalf" mensaje:"¡No pasarás!" imagen_url:"https://ejemplo.com/gandalf.png"
```

**Requisitos:**
- El usuario debe tener el permiso "Gestionar Webhooks"
- El bot necesita el permiso "Manage Webhooks"

**Casos de uso:**
- Roleplay en servidores de juegos de rol
- Anuncios creativos e inmersivos
- Storytelling y narrativa
- Mensajes de personajes de eventos

---

### `/servidor_info`
Muestra información detallada sobre el servidor actual.

**Uso:**
```
/servidor_info
```

**Información mostrada:**
- Dueño del servidor
- Número de miembros
- Cantidad de roles
- Canales totales
- Emojis disponibles
- Nivel de impulso del servidor
- Fecha de creación

---

### `/listar_comandos`
Lista todos los comandos disponibles (útil para debugging).

**Uso:**
```
/listar_comandos
```

## 🔧 Configuración Avanzada

### Logging

Los logs se guardan automáticamente en la carpeta `logs/` con el formato:
```
logs/bot_YYYY-MM-DD.log
```

Cada día se crea un nuevo archivo de log. Los logs incluyen:
- Inicio y conexión del bot
- Sincronización de comandos
- Asignación/remoción de roles
- Errores y excepciones
- Uso de comandos

### Persistencia de Datos

El bot guarda automáticamente:

**reaction_roles.json:**
```json
{
  "123456789": {
    "🎮": 987654321,
    "🎨": 876543210
  }
}
```

**guilds.json:**
```json
{
  "111111111": {
    "name": "Mi Servidor Genial"
  }
}
```

## 🛡️ Seguridad y Permisos

### Jerarquía de Roles
El bot **NO puede** asignar roles que estén:
- Al mismo nivel que su rol más alto
- Por encima de su rol más alto

**Solución:** Asegúrate de que el rol del bot esté por encima de los roles que deseas gestionar en la configuración del servidor.

### Permisos del Bot
El bot necesita estos permisos en el servidor:
- `Manage Roles` - Para asignar/quitar roles
- `Manage Webhooks` - Para el comando `/personaje`
- `Send Messages` - Para enviar mensajes
- `Manage Messages` - Para editar mensajes de roles
- `Add Reactions` - Para añadir emojis a mensajes
- `Read Message History` - Para leer mensajes antiguos

### Permisos de Usuarios
Para usar `/personaje`, el usuario necesita:
- `Manage Webhooks` - Permiso de servidor

## 🐛 Solución de Problemas

### El bot no responde a comandos
1. Verifica que el bot esté online
2. Comprueba que los comandos estén sincronizados con `/listar_comandos`
3. Revisa los logs en `logs/bot_YYYY-MM-DD.log`
4. Reinicia el bot

### Los roles no se asignan
1. Verifica la jerarquía de roles (el rol del bot debe estar arriba)
2. Comprueba que el bot tenga el permiso `Manage Roles`
3. Revisa que el emoji usado sea válido

### El comando `/personaje` no funciona
1. Verifica que tengas el permiso `Manage Webhooks`
2. Comprueba que el bot tenga el permiso `Manage Webhooks`
3. Verifica que la URL de la imagen sea válida (opcional)

### Los comandos no se actualizan
1. Los cambios en comandos pueden tardar hasta 1 hora en Discord
2. Reinicia Discord completamente
3. Si persiste, usa `/listar_comandos` para verificar

## 📚 Principios SOLID Aplicados

### **S - Single Responsibility Principle**
Cada clase tiene una única responsabilidad:
- `DataService` → Solo persistencia
- `WebhookService` → Solo webhooks
- `ReactionHandler` → Solo eventos de reacciones

### **O - Open/Closed Principle**
Puedes añadir nuevos comandos sin modificar código existente.

### **L - Liskov Substitution Principle**
Los servicios pueden ser reemplazados por implementaciones alternativas.

### **I - Interface Segregation Principle**
Cada servicio expone solo los métodos necesarios.

### **D - Dependency Inversion Principle**
Las clases dependen de abstracciones (servicios), no de implementaciones concretas.

## 🤝 Contribuir

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

Desarrollado con ❤️ para mi comunidad de rol

## 🔗 Enlaces Útiles

- [Discord.py Documentación](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Python Documentación](https://docs.python.org/3/)

## 📞 Soporte

Si encuentras algún bug o tienes sugerencias, por favor abre un issue en el repositorio.

---

**¡Disfruta tu bot de Discord! 🎉**