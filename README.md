# 🎵 Documentación Completa: Bot de Música Discord en Debian

## Tabla de contenidos
1. [Requisitos previos](#requisitos-previos)
2. [Instalación de dependencias en Debian](#instalación-de-dependencias-en-debian)
3. [Instalación de FFmpeg](#instalación-de-ffmpeg)
4. [Configuración de Python](#configuración-de-python)
5. [Configuración de Discord](#configuración-de-discord)
6. [Instalación del proyecto](#instalación-del-proyecto)
7. [Ejecución del bot](#ejecución-del-bot)
8. [Ejecutar bot en segundo plano](#ejecutar-bot-en-segundo-plano)
9. [Comandos disponibles](#comandos-disponibles)
10. [Archivos del proyecto](#archivos-del-proyecto)
11. [Solución de problemas](#solución-de-problemas)

---

## Requisitos previos

- **Debian 11 o superior** (bullseye, bookworm)
- Acceso a terminal con permisos sudo
- Conexión a Internet
- Una cuenta de Discord
- Un servidor de Discord donde tengas permisos administrativos

**Verificar versión de Debian:**
```bash
lsb_release -a
```

---

## Instalación de dependencias en Debian

### Paso 1: Actualizar el sistema

Primero, actualiza los repositorios e instala actualizaciones:

```bash
sudo apt update
sudo apt upgrade -y
```

### Paso 2: Instalar Python 3 y herramientas necesarias

```bash
sudo apt install -y python3 python3-pip python3-venv git curl wget
```

**Verificar versión de Python:**
```bash
python3 --version
```

Deberías ver Python 3.9 o superior. Si necesitas una versión más nueva:

```bash
sudo apt install -y python3.11
# O la versión que necesites
```

### Paso 3: Instalar herramientas de desarrollo

```bash
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
```

---

## Instalación de FFmpeg

FFmpeg es esencial para que el bot pueda reproducir audio en Discord.

### Instalación simple (recomendado)

```bash
sudo apt install -y ffmpeg
```

### Verificar instalación

```bash
ffmpeg -version
```

Deberías ver algo como:
```
ffmpeg version 4.4.2-1~deb11u10
```

### Si necesitas una versión más reciente (opcional)

```bash
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:savoury1/ffmpeg4
sudo apt update
sudo apt install -y ffmpeg
```

---

## Configuración de Python

### Verificar pip3

```bash
pip3 --version
```

### Actualizar pip3 a la versión más reciente

```bash
pip3 install --upgrade pip
```

---

## Configuración de Discord

### 1. Crear una aplicación en Discord Developer Portal

1. Ve a [Discord Developer Portal](https://discord.com/developers/applications)
2. Haz clic en "New Application"
3. Dale un nombre a tu aplicación (ej: "Music Bot")
4. Acepta los términos y crea la aplicación

### 2. Crear el token del bot

1. En la aplicación creada, ve a la sección "Bot" en el menú lateral
2. Haz clic en "Add Bot"
3. En la sección "TOKEN", haz clic en "Copy" para copiar el token
4. **Guarda este token en un lugar seguro** - lo necesitarás en el archivo `.env`

**⚠️ IMPORTANTE: Nunca compartas tu token. Si lo expones, regenera inmediatamente.**

### 3. Configurar permisos del bot

1. Ve a la sección "OAuth2" → "URL Generator"
2. En "SCOPES", selecciona:
   - `bot`
3. En "PERMISSIONS", selecciona:
   - `Send Messages`
   - `Connect` (para conectarse a canales de voz)
   - `Speak` (para reproducir audio)
4. Copia la URL generada y úsala en tu navegador para invitar el bot a tu servidor

---

## Instalación del proyecto

### Paso 1: Navegar a la carpeta de inicio

```bash
cd ~
```

### Paso 2: Clonar o descargar el proyecto

**Con Git (recomendado):**
```bash
git clone https://github.com/tu-usuario/discord-music-bot.git
cd discord-music-bot
```

**Sin Git:**
Descarga los archivos y extrae el ZIP:
```bash
unzip discord-music-bot.zip
cd discord-music-bot
```

### Paso 3: Crear entorno virtual

```bash
python3 -m venv venv
```

### Paso 4: Activar entorno virtual

```bash
source venv/bin/activate
```

Deberías ver `(venv)` al inicio de tu línea de comandos. Ejemplo:
```
(venv) usuario@debian:~/discord-music-bot$
```

### Paso 5: Actualizar pip en el entorno virtual

```bash
pip install --upgrade pip
```

### Paso 6: Instalar dependencias del proyecto

```bash
pip install -r requirements.txt
```

**Esto instalará:**
- discord.py - Librería para Discord
- yt-dlp - Descargador de YouTube
- python-dotenv - Para variables de entorno

**Verificar instalación:**
```bash
pip list
```

### Paso 7: Crear archivo .env

```bash
nano .env
```

Añade lo siguiente:
```
TOKEN=tu_token_de_bot_aqui
PREFIX=a!
```

**Reemplaza `tu_token_de_bot_aqui` con el token del Discord Developer Portal.**

Guarda y cierra con `Ctrl + X`, luego `Y`, luego `Enter`.

### Paso 8: Verificar archivos

```bash
ls -la
```

Deberías ver:
```
bot.py
.env
.gitignore
requirements.txt
venv/ (carpeta)
```

### Verificación final

```bash
python3 -c "import discord; import yt_dlp; print('✅ Todas las dependencias están instaladas')"
```

---

## Ejecución del bot

### Asegúrate de:
1. Estar en la carpeta del proyecto: `cd ~/discord-music-bot`
2. Estar en el entorno virtual: `source venv/bin/activate`
3. Tener el archivo `.env` con tu token
4. Haber invitado el bot a tu servidor Discord

### Ejecutar el bot

```bash
python3 bot.py
```

Deberías ver algo como:
```
Bot conectado como NombreDelBot#1234
```

El bot está listo cuando veas ese mensaje. Prueba con un comando en Discord:
```
a!play Never Gonna Give You Up
```

### Detener el bot

Presiona `Ctrl + C` en la terminal.

### Desactivar entorno virtual (cuando termines)

```bash
deactivate
```

---

## Ejecutar bot en segundo plano

Para que el bot continúe ejecutándose incluso si cierras la terminal, usa `screen` o `systemd`.

### Opción 1: Usar screen (Más simple)

**Instalar screen:**
```bash
sudo apt install -y screen
```

**Ejecutar el bot en una sesión de screen:**
```bash
cd ~/discord-music-bot
source venv/bin/activate
screen -S discord-bot python3 bot.py
```

**Ver sesiones activas:**
```bash
screen -ls
```

**Volver a conectar a la sesión:**
```bash
screen -r discord-bot
```

**Desconectar sin detener el bot** (desde dentro de screen):
Presiona `Ctrl + A`, luego `D`

**Eliminar sesión (después de detener el bot):**
```bash
screen -S discord-bot -X quit
```

### Opción 2: Usar systemd (Más profesional)

**Crear archivo de servicio:**
```bash
sudo nano /etc/systemd/system/discord-bot.service
```

**Añade el siguiente contenido:**
```ini
[Unit]
Description=Discord Music Bot
After=network.target

[Service]
Type=simple
User=tu_usuario
WorkingDirectory=/home/tu_usuario/discord-music-bot
ExecStart=/home/tu_usuario/discord-music-bot/venv/bin/python3 /home/tu_usuario/discord-music-bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Reemplaza `tu_usuario` con tu usuario de Debian.**

**Guarda con `Ctrl + X`, `Y`, `Enter`**

**Habilitar y iniciar el servicio:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable discord-bot
sudo systemctl start discord-bot
```

**Ver estado del bot:**
```bash
sudo systemctl status discord-bot
```

**Ver logs en tiempo real:**
```bash
journalctl -u discord-bot -f
```

**Detener el bot:**
```bash
sudo systemctl stop discord-bot
```

**Reiniciar el bot:**
```bash
sudo systemctl restart discord-bot
```

---

## Comandos disponibles

| Comando | Descripción | Ejemplo |
|---------|------------|---------|
| `a!play <canción>` | Reproduce una canción de YouTube | `a!play Bohemian Rhapsody` |
| `a!pause` | Pausa la reproducción actual | `a!pause` |
| `a!resume` | Reanuda la reproducción pausada | `a!resume` |
| `a!skip` | Salta a la siguiente canción | `a!skip` |
| `a!stop` | Detiene la reproducción y limpia la cola | `a!stop` |
| `a!volume <0-100>` | Ajusta el volumen en porcentaje | `a!volume 50` |
| `a!queue` | Muestra las próximas canciones en la cola | `a!queue` |

### Ejemplos de uso en Discord

```
Usuario: a!play The Beatles - Hey Jude
Bot: 🎵 Reproduciendo: The Beatles - Hey Jude

Usuario: a!queue
Bot: [Muestra embed con las próximas 10 canciones]

Usuario: a!volume 75
Bot: 🔊 Volumen establecido a 75%

Usuario: a!skip
Bot: ⏭️ Canción saltada
```

---

## Archivos del proyecto

### bot.py

Archivo principal del bot:

```python
import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración del bot
intents = discord.Intents.default()
intents.message_content = True
PREFIX = os.getenv("PREFIX", "a!")
TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Opciones para yt-dlp
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'default_search': 'ytsearch',
    'quiet': False,
    'no_warnings': False,
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

class MusicPlayer:
    def __init__(self, ctx):
        self.ctx = ctx
        self.queue = []
        self.current = None
        self.is_playing = False
        self.vc = None
        
    async def connect(self):
        """Conectar al canal de voz"""
        if self.ctx.author.voice is None:
            raise commands.CommandError("Debes estar en un canal de voz")
        
        channel = self.ctx.author.voice.channel
        self.vc = await channel.connect()
        return self.vc
    
    async def disconnect(self):
        """Desconectar del canal de voz"""
        if self.vc and self.vc.is_connected():
            await self.vc.disconnect()
    
    async def get_info(self, query):
        """Obtener información de YouTube"""
        loop = asyncio.get_event_loop()
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = await loop.run_in_executor(None, lambda: ydl.extract_info(query, download=False))
        return info
    
    async def play_next(self):
        """Reproducir siguiente canción de la cola"""
        if not self.queue:
            self.is_playing = False
            await self.disconnect()
            return
        
        self.current = self.queue.pop(0)
        url = self.current['url']
        
        def after_playing(error):
            if error:
                print(f"Error: {error}")
            asyncio.run_coroutine_threadsafe(self.play_next(), bot.loop)
        
        try:
            self.vc.play(
                discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS),
                after=after_playing
            )
            self.is_playing = True
        except Exception as e:
            print(f"Error al reproducir: {e}")
            await self.play_next()

# Diccionario para almacenar players por servidor
music_players = {}

def get_player(guild_id):
    """Obtener o crear el player del servidor"""
    if guild_id not in music_players:
        music_players[guild_id] = None
    return music_players[guild_id]

def set_player(guild_id, player):
    """Establecer el player del servidor"""
    music_players[guild_id] = player

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.command(name="play")
async def play(ctx, *, query):
    """Reproducir una canción de YouTube"""
    player = get_player(ctx.guild.id)
    
    if player is None:
        player = MusicPlayer(ctx)
        set_player(ctx.guild.id, player)
        await player.connect()
    
    async with ctx.typing():
        try:
            info = await player.get_info(query)
            
            if 'entries' in info:
                info = info['entries'][0]
            
            song = {
                'title': info.get('title', 'Canción desconocida'),
                'url': info.get('url'),
                'duration': info.get('duration', 0)
            }
            
            player.queue.append(song)
            
            if not player.is_playing:
                await player.play_next()
                await ctx.send(f"🎵 Reproduciendo: **{song['title']}**")
            else:
                await ctx.send(f"✅ Agregado a la cola: **{song['title']}**")
                
        except Exception as e:
            await ctx.send(f"❌ Error: No se pudo encontrar la canción. {str(e)}")

@bot.command(name="pause")
async def pause(ctx):
    """Pausar la reproducción"""
    player = get_player(ctx.guild.id)
    
    if player is None or player.vc is None:
        await ctx.send("❌ No hay reproducción activa")
        return
    
    if player.vc.is_playing():
        player.vc.pause()
        await ctx.send("⏸️ Reproducción pausada")
    else:
        await ctx.send("❌ No hay nada reproduciéndose")

@bot.command(name="resume")
async def resume(ctx):
    """Reanudar la reproducción"""
    player = get_player(ctx.guild.id)
    
    if player is None or player.vc is None:
        await ctx.send("❌ No hay reproducción pausada")
        return
    
    if player.vc.is_paused():
        player.vc.resume()
        await ctx.send("▶️ Reproducción reanudada")
    else:
        await ctx.send("❌ La reproducción no está pausada")

@bot.command(name="stop")
async def stop(ctx):
    """Detener la reproducción y limpiar la cola"""
    player = get_player(ctx.guild.id)
    
    if player is None or player.vc is None:
        await ctx.send("❌ No hay reproducción activa")
        return
    
    player.vc.stop()
    player.queue.clear()
    player.is_playing = False
    await player.disconnect()
    set_player(ctx.guild.id, None)
    await ctx.send("⏹️ Reproducción detenido")

@bot.command(name="skip")
async def skip(ctx):
    """Saltar a la siguiente canción"""
    player = get_player(ctx.guild.id)
    
    if player is None or player.vc is None:
        await ctx.send("❌ No hay reproducción activa")
        return
    
    if player.vc.is_playing():
        player.vc.stop()
        await ctx.send("⏭️ Canción saltada")
    else:
        await ctx.send("❌ No hay nada reproduciéndose")

@bot.command(name="volume")
async def volume(ctx, vol: int):
    """Cambiar el volumen (0-100)"""
    player = get_player(ctx.guild.id)
    
    if player is None or player.vc is None:
        await ctx.send("❌ No hay reproducción activa")
        return
    
    if not (0 <= vol <= 100):
        await ctx.send("❌ El volumen debe estar entre 0 y 100")
        return
    
    # Convertir porcentaje a rango de volumen de Discord
    volume_float = vol / 100
    
    if player.vc.source:
        player.vc.source.volume = volume_float
        await ctx.send(f"🔊 Volumen establecido a **{vol}%**")
    else:
        await ctx.send("❌ No hay fuente de audio activa")

@bot.command(name="queue")
async def queue_cmd(ctx):
    """Mostrar la cola de reproducción"""
    player = get_player(ctx.guild.id)
    
    if player is None or not player.queue:
        await ctx.send("❌ La cola está vacía")
        return
    
    embed = discord.Embed(title="Cola de reproducción", color=discord.Color.blue())
    
    if player.current:
        embed.add_field(
            name="Reproduciendo ahora",
            value=f"**{player.current['title']}**",
            inline=False
        )
    
    songs_text = "\n".join([f"{i+1}. {song['title']}" for i, song in enumerate(player.queue[:10])])
    embed.add_field(name="Próximas canciones", value=songs_text or "Ninguna", inline=False)
    
    await ctx.send(embed=embed)

# Token del bot
if TOKEN:
    bot.run(TOKEN)
else:
    print("ERROR: No se encontró el token en .env")
```

### .env

```
TOKEN=tu_token_de_bot_aqui
PREFIX=a!
```

### .gitignore

```
# Variables de entorno
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
```

### requirements.txt

```
discord.py==2.3.2
yt-dlp==2023.12.30
python-dotenv==1.0.0
```

---

## Solución de problemas

### Error: "ffmpeg: command not found"

**Solución:**
```bash
sudo apt install -y ffmpeg
ffmpeg -version
```

Si persiste, intenta:
```bash
sudo apt update
sudo apt install -y ffmpeg
hash -r
ffmpeg -version
```

### Error: "python3: command not found"

**Solución:**
```bash
sudo apt install -y python3 python3-pip
python3 --version
```

### Error: "No module named 'discord'"

**Solución:**
1. Asegúrate de estar en el entorno virtual: `source venv/bin/activate`
2. Reinstala las dependencias:
```bash
pip install --upgrade -r requirements.txt
```

### Error: "TOKEN no encontrado en .env"

**Solución:**
1. Verifica que el archivo `.env` existe:
```bash
ls -la .env
```
2. Verifica el contenido:
```bash
cat .env
```
3. Debe mostrar:
```
TOKEN=tu_token_aqui
PREFIX=a!
```

### Error: "No se puede conectar al canal de voz"

**Soluciones:**
1. Verifica que el bot tenga permisos de "Connect" y "Speak"
2. Asegúrate de estar en un canal de voz
3. Reinicia el bot:
```bash
sudo systemctl restart discord-bot
```

### El bot se desconecta constantemente

**Soluciones:**
1. Verifica la conexión a Internet
2. Actualiza yt-dlp:
```bash
pip install --upgrade yt-dlp
```
3. Reinicia el servicio:
```bash
sudo systemctl restart discord-bot
```

### Ver logs del bot (si usas systemd)

```bash
journalctl -u discord-bot -f
```

Ver últimas 50 líneas:
```bash
journalctl -u discord-bot -n 50
```

Ver logs del último reinicio:
```bash
journalctl -u discord-bot --since today
```

### Error de permisos al crear el servicio systemd

Asegúrate de usar `sudo`:
```bash
sudo nano /etc/systemd/system/discord-bot.service
```

### El bot consume mucha RAM

**Soluciones:**
1. Limita la cola de canciones
2. Usa `a!stop` cuando no se use
3. Reinicia el bot regularmente:
```bash
sudo systemctl restart discord-bot
```

### ¿Cómo resetear todo?

Si quieres empezar desde cero:

```bash
# Detener el servicio
sudo systemctl stop discord-bot

# Desactivar el servicio
sudo systemctl disable discord-bot

# Ir a la carpeta del proyecto
cd ~/discord-music-bot

# Eliminar entorno virtual
rm -rf venv

# Crear uno nuevo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Verificar .env
cat .env

# Iniciar nuevamente
sudo systemctl start discord-bot
```

---

## Comandos útiles de Debian para el bot

```bash
# Ver uso de recursos
top
# O mejor aún
htop

# Ver procesos Python
ps aux | grep python3

# Ver acceso a la red del bot
netstat -tlnp | grep python3

# Limpiar caché de pip
pip cache purge

# Actualizar todas las dependencias
pip install --upgrade -r requirements.txt
```

---

## Próximas mejoras

El código está preparado para:
- Soporte de Spotify
- Base de datos
- Sistema de permisos
- Comando de búsqueda
- Lyrics
- Playlists personalizadas

---

**¡Tu bot de música en Debian está listo! 🎵**