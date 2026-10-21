from logging import getLogger

from discord import Message
from env_dict import EnvDict
from mcrcon import MCRcon

logger = getLogger()


async def add_user_to_whitelist(message: Message, config: EnvDict) -> None:
    """Try to add the user to the whitelist from the message

    Args:
        message (Message): message to get the user from
        config (EnvDict): Config info to connect to the rcon server
    """
    user = message.content

    try:
        mcr = MCRcon(
            host=config["SERVER_URL"],
            password=config["RCON_PWORD"],
            port=config["RCON_PORT"],
        )
        mcr.connect()
        mcr.command(f"whitelist add {user}")
        logger.info("%s has been added to the whitelist by %s", user, message.author)

        await message.author.send(f"✅ {user} has been added to the server whitelist")
    except Exception as e:
        logger.error("Can't add %s to the whitelist : %e", user, e)

        await message.author.send(
            f"❌ Can't add {user} to the whitelist. Please contact an administrator"
        )
    finally:
        try:
            mcr.disconnect()
        except:
            pass
