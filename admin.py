import os
import sys
import shutil
import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
import config
from helpers.admins import require_admin
from helpers.decorators import errors_handler, check_bot_state
from helpers.filters import sudo_filter
from call.stream import mute_stream, unmute_stream
from database.blacklist import set_maintenance, is_maintenance
logger = logging.getLogger(__name__)
# Logger setting flag
logging_active = True
@Client.on_message(filters.command(["mute"], prefixes=config.COMMAND_PREFIXES) & ~filters.private)
@errors_handler
@check_bot_state
@require_admin
async def mute_handler(client: Client, message: Message):
    """Mute assistant userbot."""
    chat_id = message.chat.id
    success = await mute_stream(chat_id)
    if success:
        await message.reply_text("🔇 **Assistant muted successfully.**")
    else:
        await message.reply_text("❌ **Failed to mute assistant.**")
@Client.on_message(filters.command(["unmute"], prefixes=config.COMMAND_PREFIXES) & ~filters.private)
@errors_handler
@check_bot_state
@require_admin
async def unmute_handler(client: Client, message: Message):
    """Unmute assistant userbot."""
    chat_id = message.chat.id
    success = await unmute_stream(chat_id)
    if success:
        await message.reply_text("🔊 **Assistant unmuted successfully.**")
    else:
        await message.reply_text("❌ **Failed to unmute assistant.**")
@Client.on_message(filters.command(["clean"], prefixes=config.COMMAND_PREFIXES) & sudo_filter)
@errors_handler
async def clean_downloads_handler(client: Client, message: Message):
    """Clean all downloaded files in downloads/ folder."""
    mystic = await message.reply_text("🗑 **Cleaning up local files...**")
    try:
        shutil.rmtree(config.DOWNLOAD_DIR)
        os.makedirs(config.DOWNLOAD_DIR, exist_ok=True)
        await mystic.edit_text("✅ **Downloads directory cleared successfully.**")
    except Exception as e:
        await mystic.edit_text(f"❌ **Failed to clear directory**: `{str(e)}`")
@Client.on_message(filters.command(["restart"], prefixes=config.COMMAND_PREFIXES) & sudo_filter)
@errors_handler
async def restart_bot_handler(client: Client, message: Message):
    """Restart the bot process."""
    await message.reply_text("🔄 **Bot is restarting... please wait a few seconds.**")
    # Gracefully stop active calls
    from call.call import call_py
    try:
        for chat_id in list(call_py.queues.keys()):
            await call_py.leave_call(chat_id)
    except Exception:
        pass
    
    # Exec restart
    os.execv(sys.executable, [sys.executable] + sys.argv)
@Client.on_message(filters.command(["update"], prefixes=config.COMMAND_PREFIXES) & sudo_filter)
@errors_handler
async def update_bot_handler(client: Client, message: Message):
    """Pulls changes from git repository."""
    mystic = await message.reply_text("📥 **Checking for git updates...**")
    try:
        # Run git pull command
        import subprocess
        process = subprocess.run(["git", "pull"], capture_output=True, text=True)
        out = process.stdout or ""
        err = process.stderr or ""
        
        if "Already up to date." in out:
            await mystic.edit_text("✅ **Bot is already up to date with main branch.**")
        else:
            await mystic.edit_text(f"✅ **Updates pulled successfully! Restarting...**\n\n`{out[:300]}`")
            # Auto-restart
            os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        await mystic.edit_text(f"❌ **Failed to update**: `{str(e)}`")
@Client.on_message(filters.command(["logger"], prefixes=config.COMMAND_PREFIXES) & sudo_filter)
@errors_handler
async def logger_toggle_handler(client: Client, message: Message):
    """Toggle action logging in the log group."""
    global logging_active
    logging_active = not logging_active
    state = "ENABLED" if logging_active else "DISABLED"
    await message.reply_text(f"📊 **Logger mode set to**: `{state}`")
@Client.on_message(filters.command(["speed"], prefixes=config.COMMAND_PREFIXES) & sudo_filter)
@errors_handler
async def speedtest_handler(client: Client, message: Message):
    """Run server speedtest."""
    mystic = await message.reply_text("⚡ **Running server speed test...**")
    try:
        # We can use speedtest-cli or custom subprocess check
        import subprocess
        # Check if speedtest CLI is installed, else do fallback mock/ping
        try:
            process = subprocess.run(["speedtest-cli", "--simple"], capture_output=True, text=True, timeout=30)
            res = process.stdout or "Error running test."
            await mystic.edit_text(f"⚡ **Speedtest Results**:\n\n`{res}`")
        except FileNotFoundError:
            # Fallback if speedtest-cli binary not in container/system
            # Perform a basic speedtest using speedtest package if possible,
            # or mock it using network check.
            await mystic.edit_text("ℹ️ `speedtest-cli` is not installed on the system.\nRun `pip install speedtest-cli` on the host to use this command.")
    except Exception as e:
        await mystic.edit_text(f"❌ **Speedtest failed**: `{str(e)}`")
@Client.on_message(filters.command(["maintenance", "maintanance"], prefixes=config.COMMAND_PREFIXES) & sudo_filter)
@errors_handler
async def maintenance_handler(client: Client, message: Message):
    """Toggle global maintenance mode."""
    if len(message.command) < 2:
        curr = await is_maintenance()
        state = "on" if curr else "off"
        return await message.reply_text(f"ℹ️ **Maintenance is currently**: `{state.upper()}`\nUse `/maintenance [on/off]` to change.")
        
    arg = message.command[1].lower()
    if arg == "on":
        await set_maintenance(True)
        await message.reply_text("⚠️ **Global Maintenance Mode has been ENABLED.** Only sudo users can use commands.")
    elif arg == "off":
        await set_maintenance(False)
        await message.reply_text("✅ **Global Maintenance Mode has been DISABLED.** Normal users can use commands.")
    else:
        await message.reply_text("❌ **Invalid argument! Use `on` or `off`.**")
