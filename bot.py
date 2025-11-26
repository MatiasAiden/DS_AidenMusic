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