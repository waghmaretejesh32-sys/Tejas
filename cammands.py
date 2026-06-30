import logging
from pyrogram import Client
from pyrogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeAllChatAdministrators, BotCommandScopeAllPrivateChats, BotCommandScopeChat
import config
logger = logging.getLogger(__name__)
async def set_bot_commands(client: Client):
    """Automatically register bot commands with different scopes on startup."""
    try:
        # 1. General & Music Commands (Default / All Group Chats / All Private Chats)
        general_commands = [
            BotCommand("start", "Start the bot"),
            BotCommand("help", "Open help directory"),
            BotCommand("ping", "Check latency status"),
            BotCommand("alive", "Check system status"),
            BotCommand("settings", "Manage player preferences"),
            BotCommand("about", "About this bot"),
            BotCommand("stats", "Bot usage statistics"),
            BotCommand("uptime", "Bot runtime uptime"),
            BotCommand("privacy", "Privacy policy"),
            
            BotCommand("play", "Play audio in voice chat"),
            BotCommand("vplay", "Play video in voice chat"),
            BotCommand("song", "Download audio track as MP3"),
            BotCommand("video", "Download video clip as MP4"),
            BotCommand("pause", "Pause audio/video stream"),
            BotCommand("resume", "Resume paused stream"),
            BotCommand("skip", "Skip current track"),
            BotCommand("stop", "Stop stream and clear queue"),
            BotCommand("end", "Terminate call and clear queue"),
            BotCommand("queue", "View active playback queue"),
            BotCommand("shuffle", "Shuffle active queue tracks"),
            BotCommand("loop", "Toggle stream loop modes"),
            BotCommand("seek", "Seek to a time in stream"),
            BotCommand("forward", "Forward stream by time"),
            BotCommand("rewind", "Rewind stream by time"),
            BotCommand("lyrics", "Retrieve song lyrics"),
            BotCommand("volume", "Adjust volume level (1-200)"),
            BotCommand("history", "View stream history"),
            BotCommand("playlist", "Saved tracks playlist"),
            BotCommand("download", "Save now playing track")
        ]
        
        # 2. Admin Commands (For Group Chat Administrators)
        admin_commands = general_commands + [
            BotCommand("mute", "Mute assistant in voice chat"),
            BotCommand("unmute", "Unmute assistant in voice chat"),
            BotCommand("clean", "Clear downloaded files"),
            BotCommand("reload", "Reload bot configuration")
        ]
        
        # 3. Sudo Commands (For Developers)
        sudo_commands = admin_commands + [
            BotCommand("maintenance", "Toggle maintenance mode"),
            BotCommand("maintanance", "Toggle maintenance mode (alt spelling)"),
            BotCommand("broadcast", "Broadcast message to all chats"),
            BotCommand("gban", "Globally ban user"),
            BotCommand("ungban", "Globally unban user"),
            BotCommand("addsudo", "Promote user to Sudoer"),
            BotCommand("delsudo", "Demote user from Sudoer"),
            BotCommand("sudolist", "List Sudoer admins"),
            BotCommand("eval", "Run python code snippet"),
            BotCommand("sh", "Run shell terminal command"),
            BotCommand("logs", "Get recent bot logs"),
            BotCommand("backup", "Backup DB data"),
            BotCommand("restore", "Restore DB data"),
            BotCommand("clearcache", "Wipe cache data"),
            BotCommand("cleardb", "Wipe DB collections")
        ]
        
        # Set default commands for everyone
        await client.set_bot_commands(general_commands, scope=BotCommandScopeDefault())
        
        # Set admin commands for all group administrators
        await client.set_bot_commands(admin_commands, scope=BotCommandScopeAllChatAdministrators())
        
        # Set default for all private chats
        await client.set_bot_commands(general_commands, scope=BotCommandScopeAllPrivateChats())
        
        # Set Sudo commands for Sudo Users dynamically
        for user_id in config.SUDO_USERS:
            try:
                await client.set_bot_commands(sudo_commands, scope=BotCommandScopeChat(chat_id=user_id))
            except Exception:
                pass
                
        logger.info("Bot commands successfully registered across all scopes.")
    except Exception as e:
        logger.error(f"Failed to set bot commands: {e}")
