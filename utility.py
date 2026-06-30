import time
import logging
import config
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from helpers.decorators import errors_handler, check_bot_state
from helpers.admins import require_admin
from themes.dark import START_TEXT, HELP_TEXT, get_settings_text
from helpers.inline import get_settings_markup
from database.settings import get_chat_settings, set_volume
from database.db import db as mongo_db
from cache.cache import cache
from utils.lyrics import get_lyrics
from call.call import call_py
logger = logging.getLogger(__name__)
# Track start time for uptime metric
start_time = time.time()
@Client.on_message(filters.command(["start"], prefixes=config.COMMAND_PREFIXES))
@errors_handler
@check_bot_state
async def start_handler(client: Client, message: Message):
    """Start command handler with local banner image and premium layout."""
    import os
    owner_username = getattr(config, "OWNER_USERNAME", None)
    owner_url = f"https://t.me/{owner_username}" if owner_username else f"tg://user?id={config.OWNER_ID}"
    buttons = [
        [
            InlineKeyboardButton("➕ Add Me", url=f"https://t.me/{client.username}?startgroup=true")
        ],
        [
            InlineKeyboardButton("📚 Help", callback_data="help_menu"),
            InlineKeyboardButton("🎵 Commands", callback_data="help_music")
        ],
        [
            InlineKeyboardButton("💬 Support", url="https://t.me/EliteXMusicSupport"),
            InlineKeyboardButton("📢 Updates", url="https://t.me/EliteXMusicUpdates")
        ],
        [
            InlineKeyboardButton("👑 Owner", url=owner_url)
        ]
    ]
    
    first_name = message.from_user.first_name if message.from_user else "User"
    caption_text = START_TEXT.format(first_name=first_name)
    
    banner_path = os.path.join("assets", "banner.png")
    if os.path.exists(banner_path):
        try:
            return await message.reply_photo(
                photo=banner_path,
                caption=caption_text,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode="html"
            )
        except Exception as e:
            logger.error(f"Failed to send start photo: {e}")
            
    # Fallback to text message
    await message.reply_text(
        text=caption_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="html"
    )
@Client.on_message(filters.command(["help"], prefixes=config.COMMAND_PREFIXES))
@errors_handler
@check_bot_state
async def help_handler(client: Client, message: Message):
    """Help command handler displaying directory grid."""
    from helpers.inline import get_help_markup
    await message.reply_text(
        text=HELP_TEXT,
        reply_markup=get_help_markup(),
        parse_mode="html"
    )
@Client.on_message(filters.command(["ping"], prefixes=config.COMMAND_PREFIXES))
@errors_handler
@check_bot_state
async def ping_handler(client: Client, message: Message):
    """Measure ping latencies (API response, MongoDB connection, Redis cache)."""
    start_ping = time.time()
    msg = await message.reply_text("⚡ **Pinging...**")
    api_ping = round((time.time() - start_ping) * 1000, 2)
    
    # Measure DB Ping
    db_ping = "Offline"
    if mongo_db is not None:
        try:
            start_db = time.time()
            # Simple command to test DB latency
            await mongo_db.command("ping")
            db_ping = f"{round((time.time() - start_db) * 1000, 2)} ms"
        except Exception:
            db_ping = "Error"
            
    # Measure Cache Ping
    cache_ping = "Offline"
    if cache.use_redis:
        try:
            start_cache = time.time()
            await cache.redis_client.ping()
            cache_ping = f"{round((time.time() - start_cache) * 1000, 2)} ms"
        except Exception:
            cache_ping = "Error"
    await msg.edit_text(
        f"🚀 **PONG!**\n\n"
        f"🤖 **Bot API Latency**: `{api_ping} ms`\n"
        f"🗄 **MongoDB Latency**: `{db_ping}`\n"
        f"⚡ **Redis Latency**: `{cache_ping}`"
    )
@Client.on_message(filters.command(["alive"], prefixes=config.COMMAND_PREFIXES))
@errors_handler
@check_bot_state
async def alive_handler(client: Client, message: Message):
    """Check if the bot process and dependencies are alive and healthy."""
    uptime_sec = int(time.time() - start_time)
    hours = uptime_sec // 3600
    minutes = (uptime_sec % 3600) // 60
    
    db_status = "🟢 Connected" if mongo_db is not None else "🔴 Disconnected"
    redis_status = "🟢 Connected" if cache.use_redis else "🔴 Offline (Using In-Memory)"
    
    # Check if assistant userbot is active
    assistant_status = "🔴 Offline"
    from core.client import assistant
    if assistant.is_connected:
        assistant_status = f"🟢 Online (@{assistant.username})"
        
    await message.reply_text(
        f"🌌 **EliteX Music Bot Status** 🌌\n\n"
        f"🤖 **Bot Account**: `🟢 Active (@{client.username})`\n"
        f"👤 **Assistant Account**: `{assistant_status}`\n"
        f"🗄 **MongoDB Storage**: `{db_status}`\n"
        f"⚡ **Redis Cache**: `{redis_status}`\n"
        f"⏱ **System Uptime**: `{hours}h {minutes}m`\n\n"
        f"✨ _Everything is running optimally!_"
    )
@Client.on_message(filters.command(["lyrics"], prefixes=config.COMMAND_PREFIXES))
@errors_handler
@check_bot_state
async def lyrics_handler(client: Client, message: Message):
    """Retrieve lyrics of a song."""
    if len(message.command) < 2:
        # If no argument, try to search lyrics of the currently playing song in this chat
        chat_id = message.chat.id
        queue = await call_py.get_queue(chat_id)
        if queue:
            query = f"{queue[0]['artist']} - {queue[0]['title']}"
        else:
            return await message.reply_text("ℹ️ **Usage**: `/lyrics [song name]`")
    else:
        query = message.text.split(None, 1)[1]
        
    mystic = await message.reply_text(f"🔍 **Searching lyrics for** `{query}`...")
    
    lyrics = await get_lyrics(query)
    # Split text if it exceeds Telegram's 4096 character limit
    if len(lyrics) > 4000:
        parts = [lyrics[i:i+4000] for i in range(0, len(lyrics), 4000)]
        await mystic.delete()
        for part in parts:
            await message.reply_text(part)
    else:
        await mystic.edit_text(lyrics)
@Client.on_message(filters.command(["settings"], prefixes=config.COMMAND_PREFIXES) & ~filters.private)
@errors_handler
@check_bot_state
@require_admin
async def settings_handler(client: Client, message: Message):
    """Manage group audio preferences."""
    chat_id = message.chat.id
    settings = await get_chat_settings(chat_id)
    
    text = get_settings_text(
        chat_title=message.chat.title,
        volume=settings.get("volume", 100),
        quality=settings.get("quality", "high"),
        loop=settings.get("loop", 0)
    )
    
    markup = get_settings_markup(
        quality=settings.get("quality", "high"),
        loop=settings.get("loop", 0)
    )
    await message.reply_text(text=text, reply_markup=markup, parse_mode="html")
@Client.on_message(filters.command(["volume"], prefixes=config.COMMAND_PREFIXES) & ~filters.private)
@errors_handler
@check_bot_state
@require_admin
async def volume_handler(client: Client, message: Message):
    """Check or update group stream volume (1-200)."""
    chat_id = message.chat.id
    settings = await get_chat_settings(chat_id)
    curr_vol = settings.get("volume", 100)
    
    if len(message.command) < 2:
        return await message.reply_text(f"🔊 <b>Current volume is set to</b>: <code>{curr_vol}%</code>\nTo update: <code>/volume [1-200]</code>", parse_mode="html")
        
    vol_str = message.command[1]
    if not vol_str.isdigit():
        return await message.reply_text("❌ <b>Volume must be a positive integer.</b>", parse_mode="html")
        
    vol = int(vol_str)
    if vol < 1 or vol > 200:
        return await message.reply_text("❌ <b>Volume range must be between 1 and 200.</b>", parse_mode="html")
        
    # Update DB
    await set_volume(chat_id, vol)
    
    # Update active call if playing
    try:
        await call_py.change_volume_call(chat_id, vol)
    except Exception:
        pass
        
    await message.reply_text(f"🔊 <b>Volume level updated to</b>: <code>{vol}%</code>", parse_mode="html")
@Client.on_message(filters.command(["admin"], prefixes=config.COMMAND_PREFIXES) & ~filters.private)
@errors_handler
@check_bot_state
@require_admin
async def admin_panel_handler(client: Client, message: Message):
    """Admin controls dashboard."""
    from themes.dark import get_admin_text
    from helpers.inline import get_admin_markup
    text = get_admin_text(message.chat.title)
    markup = get_admin_markup()
    await message.reply_text(text=text, reply_markup=markup, parse_mode="html")
@Client.on_message(filters.command(["sudo"], prefixes=config.COMMAND_PREFIXES))
@errors_handler
@check_bot_state
async def sudo_panel_handler(client: Client, message: Message):
    """Sudo controls dashboard (Restricted to Sudo users)."""
    from database.sudoers import is_sudo
    if not await is_sudo(message.from_user.id):
        return await message.reply_text("❌ <b>This command is restricted to Sudo/Developer admins.</b>", parse_mode="html")
        
    from themes.dark import get_sudo_text
    from helpers.inline import get_sudo_markup
    text = get_sudo_text(client.username)
    markup = get_sudo_markup()
    await message.reply_text(text=text, reply_markup=markup, parse_mode="html")
@Client.on_message(filters.command(["stats"], prefixes=config.COMMAND_PREFIXES))
@errors_handler
@check_bot_state
async def stats_handler(client: Client, message: Message):
    """Show bot statistics to Sudo/Owner or Group Admins."""
    user_id = message.from_user.id if message.from_user else None
    if not user_id:
        return
        
    # Check if user is Sudo / Owner
    from database.sudoers import is_sudo
    is_authorized = await is_sudo(user_id)
    
    if not is_authorized and message.chat.type.name != "PRIVATE":
        # Check if user is Group Admin/Owner
        try:
            member = await client.get_chat_member(message.chat.id, user_id)
            if member.status.name in ["ADMINISTRATOR", "OWNER"]:
                is_authorized = True
        except Exception:
            pass
            
    if not is_authorized:
        return await message.reply_text("❌ **You are not authorized to view system statistics!**")
    from database.settings import get_stats
    import time
    start_ping = time.time()
    msg = await message.reply_text("⚡ <b>Fetching statistics...</b>", parse_mode="html")
    ping = round((time.time() - start_ping) * 1000, 2)
    db_stats = await get_stats()
    total_chats = db_stats.get("total_chats", 0)
    total_songs = db_stats.get("total_songs", 0)
    stats_text = (
        "📊 <b>Bot Statistics</b>\n\n"
        f"👥 <b>Total Chats</b>: <code>{total_chats}</code>\n"
        f"🎵 <b>Tracks Played</b>: <code>{total_songs}</code>\n"
        f"📶 <b>Bot Latency</b>: <code>{ping} ms</code>\n"
        f"👑 <b>Owner</b>: <code>{config.OWNER_ID}</code>"
    )
    await msg.edit_text(stats_text, parse_mode="html")
