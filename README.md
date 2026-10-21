# Minecraft Auto Whitelist

A small Discord bot that watches a specific Discord channel and automatically adds the message text to a Minecraft server whitelist through RCON.

## What it does

When a user sends a message in the configured Discord channel, the bot:

- checks that the message was not sent by another bot
- verifies the message came from the configured channel
- connects to the Minecraft server over RCON
- runs the command `whitelist add <message>`
- sends the result back to the user in Discord
- deletes the original message from the channel

This is useful for lightweight whitelist requests where the username is simply the value of the message itself.

## Project structure

- `src/minecraft_auto_whitelist/bot.py` — entry point for the application
- `src/minecraft_auto_whitelist/setup_bot.py` — Discord bot setup and message handling
- `src/minecraft_auto_whitelist/load_env.py` — loads configuration from environment variables
- `src/minecraft_auto_whitelist/minecraft_rcon.py` — adds players to the whitelist via RCON

## Requirements

- Python 3.14 or newer (as declared in `pyproject.toml`)
- A Discord bot token
- A Minecraft server exposed with RCON enabled
- A Discord text channel ID to monitor

## Installation

Clone the repository and install it in a virtual environment:

```bash
git clone https://github.com/<your-user>/minecraft_auto_whitelist.git
cd minecraft_auto_whitelist
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# On Windows PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

If you prefer to use `uv`:

```bash
uv sync
```

## Configuration

Create a `.env` file in the project root with the required variables:

```env
TOKEN_BOT=your_discord_bot_token
CHANEL_ID=123456789012345678
SERVER_URL=your_minecraft_server_ip_or_hostname
RCON_PWORD=your_rcon_password
RCON_PORT=25575
```

### Environment variables

- `TOKEN_BOT`: Discord bot token used to log in.
- `CHANEL_ID`: Discord channel ID to monitor for whitelist requests.
- `SERVER_URL`: Hostname or IP of the Minecraft server.
- `RCON_PWORD`: Password for the Minecraft RCON connection.
- `RCON_PORT`: Optional RCON port. If it is missing or invalid, the bot falls back to `25575`.

> The project currently uses the key name `CHANEL_ID` with an "a" in "channel". Keep that exact spelling in the environment file.

## Run the bot

After installation and configuration, start the bot with:

```bash
minecraft-auto-whitelist
```

You can also run it directly:

```bash
python -m minecraft_auto_whitelist.bot
```

## Usage

1. Add the bot to your Discord server.
2. Give it permission to read and manage messages in the chosen channel.
3. Set the target channel ID in `.env`.
4. Send a username in that channel.
5. The bot will try to add it to the Minecraft whitelist and reply with a success or failure message.

## Notes

- The bot deletes the original request message after processing.
- The whitelist name is taken directly from the text of the message.
- If RCON fails, the user receives a failure message instead of a whitelist entry.
