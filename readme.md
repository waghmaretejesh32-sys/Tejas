🌌 EliteX Telegram Music Bot
Python VersionPyrogram VersionPyTgCalls
License

EliteX is a premium, feature-rich, production-ready Telegram Music Bot built using Python 3.12, Pyrogram v2, and PyTgCalls. It is optimized for zero-buffering voice chat streaming of audio and video from YouTube, Spotify, JioSaavn, Apple Music, SoundCloud, and Telegram files.

🌟 Features List
🎥 Video Streaming: Stream high-definition videos directly into Telegram voice chats.
⚡ Zero-Buffering: Extracts and streams direct YouTube audio/video links instantly.
🎵 Multi-Platform Support: YouTube, Spotify, Apple Music, SoundCloud, JioSaavn, Radio Streams.
👥 Multi-Group Support: Handles multiple group voice chats simultaneously with isolated states.
⏱ 24/7 Playback: Maintain voice chats running continuously even if the assistant goes offline.
⚙️ Dynamic Settings Panel: Real-time group settings adjustment (volume, stream quality, looping) using inline keyboards.
🔁 Flexible Looping: Loop a single track or the entire active queue.
📊 Queue Management: Shuffle, remove specific items, view upcoming tracks, or skip to index.
📥 Downloader Commands: Downloader commands for /song (MP3) and /video (MP4) sent as Telegram media.
🗑 Auto-Clean Downloads: Automatically cleans up local temporary files after streaming or uploading.
🗄 MongoDB Integration: Persist chat configurations, playlists, histories, stats, blacklists, and maintenance modes.
⚡ Redis Cache Layer: Caches YouTube searches, Spotify track resolutions, and lyrics with a local in-memory fallback.
👑 Dual Roles & Sudo List: Sudo user promotion, dynamic chat/user blacklist management, and system maintenance lock.
🚀 Beautiful Console Logging: Clean startup banner logs and automatic error logging directly to a Telegram log group.
📸 Screenshots
Now Playing Player Card

🌌 NOW PLAYING
🎵 Song: Faded
👤 Artist: Alan Walker
⏱ Duration: 03:32
📊 Queue Position: 1/5
🔊 Volume: 100%
👤 Requested By: @username
⚡ Type: 🎵 Audio Stream
⏱ ▬▬▬●▬▬▬▬▬▬▬▬▬▬▬▬▬
[ ⏮ Prev ]  [ ⏸ Pause ]  [ ▶ Resume ]  [ ⏭ Skip ]
[      🔉 Vol -       ]  [       🔊 Vol +       ]
[      📜 Queue       ]  [       🔁 Loop        ]
[      🎶 Playlist    ]  [       ⚙ Settings     ]
[                 ❌ Close Player                ]
Settings Control Panel

⚙️ Chat Settings Dashboard
👥 Group: Music Enthusiasts
🔊 Volume level: 100%
🎧 Audio Quality: HIGH
🔁 Looping Mode: ❌ Disabled
💡 Adjust settings using the inline keyboard below:
[      🔈 Vol -10     ]  [      🔊 Vol +10      ]
[ 🎧 Quality: ] [ Low ] [ Medium ] [ 🔹 High ]
[  Loop State: ] [ 🔹 Off ] [ Track ] [ Queue ]
[                ❌ Close Settings               ]
📋 Requirements
Python 3.12 or higher.
FFmpeg installed on the host system.
MongoDB Database (Self-hosted or MongoDB Atlas Cluster).
Redis Server (Self-hosted or Redis Labs instance).
Telegram API Credentials (API_ID, API_HASH) and Bot Token.
Telegram Account (to generate the userbot String Session).
🛠 Setup & Installation Guides
How to Retrieve Credentials
1. How to get API_ID & API_HASH
Open your browser and log in to my.telegram.org using your Telegram phone number.
Go to API development tools.
Create a new application. Fill in the title and short name.
Copy the generated App api_id and App api_hash.
2. How to create a Telegram Bot Token
Open Telegram and search for the @BotFather.
Send /newbot and follow the prompts to choose a bot name and username.
Copy the HTTP API token (e.g. 123456789:ABCdefGhIJK...).
3. How to create a MongoDB Database
Create a free account on MongoDB Atlas.
Deploy a free cluster (M0 sandbox).
Under Database Access, create a user with read/write credentials.
Under Network Access, whitelist connection IP addresses (use 0.0.0.0/0 to allow all servers).
Go to Database -> Connect -> Connect your application. Copy the connection string (mongodb+srv://...).
4. How to generate a String Session
Generate a Pyrogram String Session using a script:

python

# session_gen.py
import asyncio
from pyrogram import Client
async def main():
    api_id = int(input("API_ID: "))
    api_hash = input("API_HASH: ")
    async with Client("session_gen", api_id, api_hash) as app:
        print("Here is your Pyrogram String Session:")
        print(await app.export_session_string())
asyncio.run(main())
Run python session_gen.py, enter your credentials and phone number verification code, then copy the output.

Prerequisites Installation
Installing FFmpeg
Ubuntu / Debian:
bash

sudo apt update
sudo apt install ffmpeg -y
macOS (via Homebrew):
bash

brew install ffmpeg
Windows: Download binaries from Gyan.dev and add the bin directory to your System PATH variables.
Setting up Redis
Ubuntu / Debian:
bash

sudo apt install redis-server -y
sudo systemctl enable redis-server.service
sudo systemctl start redis-server.service
Local/Ubuntu VPS Installation Guide
Clone the repository:
bash

git clone https://github.com/yourusername/telegram-music-bot.git
cd telegram-music-bot
Create a virtual environment and install packages:
bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Configure environment variables: Create a .env file in the root folder using the .env.example template:
bash

cp .env.example .env
nano .env
Run the Bot:
bash

python bot.py
🐳 Docker Deployment
Build the Docker Image:
bash

docker build -t music-bot .
Run in background (detached):
bash

docker run -d --env-file .env --name active-music-bot music-bot
☁️ Cloud Deployments
Railway Deployment
Log in to Railway.app.
Click New Project -> Deploy from GitHub repo.
Select your bot repository.
Add the required Environment Variables in the project variables dashboard.
Railway will automatically build and run the project using the provided Dockerfile.
Koyeb Deployment
Log in to Koyeb.com.
Create a new App service linked to your GitHub repository.
Choose Docker build system or let Koyeb run it via the Dockerfile in the root.
Add all environment variables listed in .env.example.
Deploy.
Render Deployment
Log in to Render.com.
Click New -> Background Worker.
Select your repository.
Set the build command to pip install -r requirements.txt and start command to python bot.py (or let it build using the Dockerfile by setting runtime environment to Docker).
Add the environment variables.
⚙️ Environment Variables Explanation
Variable Name	Type	Description	Required
API_ID	Integer	Telegram API ID from my.telegram.org	Yes
API_HASH	String	Telegram API Hash from my.telegram.org	Yes
BOT_TOKEN	String	Bot HTTP token from @BotFather	Yes
STRING_SESSION	String	Pyrogram String Session for the Assistant userbot	Yes
MONGO_URI	String	Connection string for MongoDB Atlas/Self-hosted	Yes
MONGO_DB_NAME	String	MongoDB database name (default: telegram_music_bot)	No
REDIS_URL	String	Redis cache URL (e.g. redis://localhost:6379/0)	No
OWNER_ID	Integer	Telegram ID of the primary owner	Yes
SUDO_USERS	CSV	Comma-separated user IDs of additional bot admins	No
LOG_GROUP_ID	Integer	Chat ID of the group/channel where error reports are sent	No
DURATION_LIMIT_MIN	Integer	Maximum allowed track length in minutes (default: 180)	No
AUTO_LEAVE_TIME	Integer	Seconds to wait before leaving empty voice chat (default: 120)	No
⌨️ Bot Commands List
User Commands
/start - Initialize contact with the bot, view invite buttons.
/help - View documentation of commands.
/play [query/URL] - Play audio in the voice chat.
/vplay [query/URL] - Play video stream in the voice chat.
/song [query] - Download track as MP3 audio format.
/video [query] - Download video as MP4 format.
/lyrics [query] - Find lyrics of a song.
/queue - View upcoming tracks.
/playlist - View personal custom playlist.
/playlist play - Stream personal playlist.
/playlist add - Add currently playing track to playlist.
/playlist remove [index] - Remove a song from your playlist.
/playlist clear - Delete all songs in playlist.
/history - View recently played tracks in the group chat.
/volume - View current volume.
/ping - Calculate Bot API, DB, and Cache latency response times.
/alive - View bot and assistant uptime details.
Administrator Commands (Group Admins & Sudoers)
/pause - Pause stream playback.
/resume - Resume stream playback.
/skip - Skip current song to the next track.
/stop or /end - Stop playback, clear queue, and leave voice chat.
/mute - Mute assistant userbot.
/unmute - Unmute assistant userbot.
/shuffle - Shuffle upcoming songs in the queue.
/loop [0/1/2] - Set loop mode (0: Off, 1: Track Loop, 2: Queue Loop).
/seek [seconds] - Seek playback to a specific timestamp.
/forward [seconds] - Seek forward.
/rewind [seconds] - Seek backward.
/volume [1-200] - Change streaming volume.
/settings - View settings dashboard.
Sudo & Owner Commands
/blacklist [chat_id/user_id] - Restrict chat/user from using commands.
/whitelist [chat_id/user_id] - Allow blacklisted chat/user.
/addsudo [user_id] - Add user as a bot administrator (Owner only).
/delsudo [user_id] - Remove user from bot administrators (Owner only).
/addpremium [user_id] - Add user to Premium list.
/delpremium [user_id] - Remove user from Premium list.
/clean - Clean up local downloads folder.
/logger - Toggle log group error reporting.
/speed - Run server speed test.
/maintenance [on/off] - Lock bot commands globally.
/restart - Restart the bot process.
/update - Check and pull git updates.
🛠 Troubleshooting & FAQ
Q: Bot crashes during start saying: STRING_SESSION is missing.
A: The Assistant account must join the group calls, so a Pyrogram user string session must be created. Refer to the How to generate a String Session section above.

Q: Audio streams are quiet or sound distorted.
A: Set the volume to 100 or 120 using /volume 120. Make sure FFmpeg is updated to its latest version.

Q: The bot does not join the voice chat when I type /play.
A: Ensure that:

A Voice Chat is already open in the group chat.
The Assistant userbot account has been added to the group chat (or is permitted to join via group permissions/invite links).
The main bot account is promoted to administrator.
Q: Can I run this without Redis?
A: Yes, the system includes an in-memory database cache fallback that automatically runs if connection to the Redis server fails.

📣 Community & Support
💬 Support Group: EliteX Music Support
📣 Updates Channel: EliteX Music Updates
📄 License
This project is licensed under the MIT License. Refer to the 
LICENSE
 file for more details.

📈 Changelog
v2.0.0 (Latest Release)
Fully migrated to Python 3.12 and Pyrogram v2.
Implemented PyTgCalls v2 audio/video engine.
Added live stream URL processing and direct YouTube URL streaming.
Implemented Redis caching layer with in-memory fallback.
Designed a beautiful premium dark theme inline dashboard.
🤝 Contributing Guide
Fork the Project repository.
Create a Feature Branch (git checkout -b feature/AmazingFeature).
Commit your changes (git commit -m 'Add some AmazingFeature').
Push to the Branch (git push origin feature/AmazingFeature).
Open a Pull Request for review