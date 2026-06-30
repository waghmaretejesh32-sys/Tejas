# Premium Dark Theme templates (HTML format) for Music Bot
import config
START_TEXT = """╭━━━━━━━━━━━━━━━━━━━━╮
      🎧 ELITE MUSIC BOT
╰━━━━━━━━━━━━━━━━━━━━╯
✨ High Quality Music Streaming
🎵 YouTube
🎧 Spotify
🎙 Voice Chat
⚡ Ultra Fast Playback
🌍 Unlimited Groups
"""
HELP_TEXT = """╭━━━━━━━━━━━━━━━━━━━━╮
       📚 HELP CENTER
╰━━━━━━━━━━━━━━━━━━━━╯
🎵 Music Commands
👮 Admin Commands
👑 Sudo Commands
⚙ Settings
📜 Queue
❓ FAQ
"""
HELP_MUSIC = """╭━━━━━━━━━━━━━━━━━━━━╮
      🎵 MUSIC COMMANDS
╰━━━━━━━━━━━━━━━━━━━━╯
Stream audio and video in group voice chats.
• <code>/play [name/url]</code> - Stream audio
• <code>/vplay [name/url]</code> - Stream video
• <code>/lyrics [song]</code> - Retrieve lyrics
• <code>/volume [1-200]</code> - Adjust volume
"""
HELP_ADMIN = """╭━━━━━━━━━━━━━━━━━━━━╮
      👮 ADMIN COMMANDS
╰━━━━━━━━━━━━━━━━━━━━╯
Group Administrators playback commands.
• <code>/pause</code> - Pause stream
• <code>/resume</code> - Resume stream
• <code>/skip</code> - Skip current track
• <code>/stop</code> | <code>/end</code> - Stop & clear
• <code>/mute</code> | <code>/unmute</code> - Mute/Unmute assistant
• <code>/shuffle</code> - Shuffle queue
"""
HELP_SUDO = """╭━━━━━━━━━━━━━━━━━━━━╮
      👑 SUDO COMMANDS
╰━━━━━━━━━━━━━━━━━━━━╯
Global bot developer instructions.
• <code>/broadcast [text]</code> - Send announcement
• <code>/blacklist</code> | <code>/whitelist</code> - Block lists
• <code>/addsudo</code> | <code>/delsudo</code> - Sudoers list
• <code>/maintenance [on/off]</code> - Toggle lock
• <code>/restart</code> - Reboot process
• <code>/clean</code> - Wipe downloaded files
"""
HELP_PLAYLIST = """╭━━━━━━━━━━━━━━━━━━━━╮
      📂 PLAYLIST COMMANDS
╰━━━━━━━━━━━━━━━━━━━━╯
Manage your saved tracks.
• <code>/playlist</code> - View playlist
• <code>/playlist add</code> - Save track
• <code>/playlist play</code> - Play playlist
• <code>/playlist clear</code> - Clear playlist
"""
HELP_VC = """╭━━━━━━━━━━━━━━━━━━━━╮
      🎙️ VOICE CHAT CONTROL
╰━━━━━━━━━━━━━━━━━━━━╯
Assistant connection details.
• Join: Triggered automatically
• Leave: Leaves if empty for 2m
• Recovery: Auto lag reconnect
"""
HELP_DOWNLOAD = """╭━━━━━━━━━━━━━━━━━━━━╮
      📥 DOWNLOADER UTILS
╰━━━━━━━━━━━━━━━━━━━━╯
Download files to Telegram.
• <code>/song [query]</code> - Get MP3
• <code>/video [query]</code> - Get MP4
"""
HELP_SETTINGS = """╭━━━━━━━━━━━━━━━━━━━━╮
      🌐 CHAT SETTINGS
╰━━━━━━━━━━━━━━━━━━━━╯
Configure group streaming preferences.
• <code>/settings</code> - Load preferences panel
• <code>/volume [1-200]</code> - Configure volume
"""
def get_progress_bar(current_sec: int, total_sec: int) -> str:
    """Generate a clean progress bar formatted like: 01:32 ━━━━━━━⬤━━━━━━ 03:54"""
    from helpers.formatters import seconds_to_duration
    curr_str = seconds_to_duration(current_sec)
    total_str = seconds_to_duration(total_sec)
    if total_sec <= 0:
        return f"<code>{curr_str} ━━━━━━━⬤━━━━━━ {curr_str}</code>"
        
    total_lines = 15
    percent = min(1.0, max(0.0, current_sec / total_sec))
    dot_position = int(percent * total_lines)
    
    # Generate the slider
    bar = "━" * dot_position + "⬤" + "━" * (total_lines - dot_position)
    return f"<code>{curr_str} {bar} {total_str}</code>"
def get_now_playing_text(track: dict, volume: int, position: int, total: int, current_sec: int = 0) -> str:
    """Return a premium HTML formatted string for the now playing card."""
    title = track.get("title", "Unknown Track")
    artist = track.get("artist", "Unknown Artist")
    duration = track.get("duration", "00:00")
    req_by = track.get("req_by", "Unknown User")
    
    from helpers.formatters import duration_to_seconds
    total_sec = duration_to_seconds(duration)
    progress = get_progress_bar(current_sec, total_sec)
    
    text = (
        f"╭━━━━━━━━━━━━━━━━━━━━╮\n"
        f"      🎶 NOW PLAYING\n"
        f"╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
        f"🎵 <b>Song</b>: <code>{title}</code>\n\n"
        f"👤 <b>Artist</b>: <code>{artist}</code>\n\n"
        f"⏱ <b>Duration</b>: <code>{duration}</code>\n\n"
        f"🙋 <b>Requested By</b>: {req_by}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{progress}\n\n"
        f"✨ High Quality Streaming..."
    )
    return text
def get_settings_text(chat_title: str, volume: int, quality: str, loop: int) -> str:
    """Return premium HTML formatted settings dashboard."""
    loop_str = "Disabled" if loop == 0 else ("Track" if loop == 1 else "Queue")
    return (
        f"╭━━━━━━━━━━━━━━━━━━━━╮\n"
        f"│   ⚙️  SETTINGS      \n"
        f"╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
        f"🎚 <b>Audio Quality</b>: <code>{quality.upper()}</code>\n"
        f"🔊 <b>Default Volume</b>: <code>{volume}%</code>\n"
        f"🌍 <b>Language</b>: <code>English (EN)</code>\n"
        f"🎙 <b>Auto Join</b>: <code>Enabled</code>\n"
        f"🚪 <b>Auto Leave</b>: <code>Enabled</code>\n"
        f"🔁 <b>Loop Mode</b>: <code>{loop_str}</code>"
    )
def get_queue_text(queue: list, loop_mode: int, page: int = 0) -> str:
    """Return premium HTML formatted queue layout with pagination."""
    text = (
        "╭━━━━━━━━━━━━━━━━━━━━╮\n"
        "        📜 MUSIC QUEUE\n"
        "╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
    )
    
    items_per_page = 3
    start_index = page * items_per_page
    end_index = start_index + items_per_page
    page_items = queue[start_index:end_index]
    
    if not page_items:
        text += "💬 <i>Upcoming queue is empty. Use /play to add songs!</i>"
        return text
        
    circles = ["①", "②", "③"]
    
    for i, track in enumerate(page_items):
        title = track.get("title", "Unknown Track")
        req_by = track.get("req_by", "Unknown User")
        
        text += (
            f"{circles[i]} <b>{title}</b>\n"
            f"👤 Requested by <b>{req_by}</b>\n"
        )
        if i < len(page_items) - 1:
            text += "━━━━━━━━━━━━\n\n"
            
    return text
def get_admin_text(chat_title: str) -> str:
    """Return premium HTML formatted admin panel layout."""
    return (
        f"╭━━━━━━━━━━━━━━━━━━━━╮\n"
        f"     👮 Admin Controls\n"
        f"╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
        f"👥 <b>Group</b>: <code>{chat_title}</code>\n\n"
        f"Choose administrative actions below:"
      )
def get_sudo_text(bot_username: str) -> str:
    """Return premium HTML formatted sudo panel layout."""
    return (
        f"╭━━━━━━━━━━━━━━━━━━━━╮\n"
        f"     👑 Sudo Controls\n"
        f"╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
        f"🤖 <b>Bot</b>: <code>@{bot_username}</code>\n\n"
        f"Choose developer actions below:"
    )
MAINTENANCE_TEXT = """╭━━━━━━━━━━━━━━━━━━━━╮
│  🚧  UNDER MAINTENANCE  🚧
├━━━━━━━━━━━━━━━━━━━━┤
│ 🛠 The bot is undergoing maintenance.
│ Please try again later.
╰━━━━━━━━━━━━━━━━━━━━╯
"""
