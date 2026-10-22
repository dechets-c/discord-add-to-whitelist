from discord.app_commands import command
from typing import Literal
from logging import getLogger

from discord import Message
from mcrcon import MCRcon

from .env_dict import EnvDict
from .exceptions import (
    PlayerAlreadyWhitelistedError,
    PlayerDoesNotExistError,
    UnknownWhitelistResponseError,
    WhitelistError,
)

commands = Literal["whitelist", "fwhitelist"]

logger = getLogger()


async def send_to_server(user: str, mcr: MCRcon, command: commands) -> str:
    """Send a whitelist command to the Minecraft server over RCON.

    Args:
        user (str): Minecraft username to add.
        mcr (MCRcon): Connected RCON client.
        command (Literal["whitelist", "fwhitelist"]): RCON command prefix.

    Returns:
        str: Server response text, or a fallback when empty.
    """
    response = mcr.command(f"{command} add {user}")
    return response.strip() or "(no response from server)"


async def treet_response(
    server_response: str, user: str, message: Message, command: commands
) -> None:
    """Handle the server response and notify the Discord user.

    Args:
        server_response (str): Raw response returned by the RCON server.
        user (str): Minecraft username being processed.
        message (Message): Original Discord message used for responses.

    Raises:
        PlayerDoesNotExistError: If the server reports that player does not exist.
        UnknownWhitelistResponseError: If the response is not recognized.
    """
    logger.debug(server_response)
    if server_response == f"Added {user} to the whitelist":
        await message.author.send(f"✅ {user} has been added to the server whitelist")
    elif server_response == "That player does not exist":
        raise PlayerDoesNotExistError(server_response)
    elif command == "fwhitelist":
        await message.author.send(f"Maybe it worked idk if not try uuid")
    else:
        raise PlayerAlreadyWhitelistedError(server_response)


async def add_user_to_whitelist(message: Message, config: EnvDict) -> None:
    """Try to add the user to the whitelist from a Discord message.

    Args:
        message (Message): Discord message containing the requested username.
        config (EnvDict): Configuration required to connect to the RCON server.
    """
    user = message.content

    command = "fwhitelist" if user.startswith(".") else "whitelist"

    user = user[1:] if user.startswith(".") else user

    mcr = None
    try:
        mcr = MCRcon(
            host=config["SERVER_URL"],
            password=config["RCON_PWORD"],
            port=config["RCON_PORT"],
        )
        mcr.connect()
        logger.info("%s has been added to the whitelist by %s", user, message.author)

        # send the command to the server
        server_response = await send_to_server(user, mcr, command)
        await treet_response(server_response, user, message, command)

    except PlayerDoesNotExistError:
        await message.author.send(f"❌ {user} does not exist on the server")

    except PlayerAlreadyWhitelistedError:
        await message.author.send(f"⚠️ {user} is already in the server whitelist")

    except UnknownWhitelistResponseError:
        await message.author.send(f"❌ Can't classify server response for {user}")

    except WhitelistError:
        await message.author.send(f"❌ Whitelist error for {user}")

    except Exception as e:
        # add msg per exception here
        logger.exception("Can't add %s to the whitelist: %s", user, e)

        await message.author.send(
            f"❌ Can't add {user} to the whitelist. Please contact an administrator"
        )
    finally:
        if mcr is not None:
            try:
                mcr.disconnect()
                logger.debug("Disconnected from RCON server")
            except Exception:
                pass
