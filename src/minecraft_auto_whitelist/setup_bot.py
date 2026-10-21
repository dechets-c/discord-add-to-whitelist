from env_dict import EnvDict
from discord.message import Message
from logging import getLogger

from discord import Intents
from discord.ext.commands import Bot

from minecraft_rcon import add_user_to_whitelist

logger = getLogger()


def get_bot(config: EnvDict) -> Bot:
    """Configure the default bot behavior

    Returns:
        Bot: Bot configured
    """
    intents = Intents.default()
    intents.message_content = True  # Required to read chat messages
    bot = Bot(intents=intents, command_prefix="!")

    @bot.event
    async def on_ready() -> None:
        logger.info("%s is ready", bot.user.name)

    @bot.event
    async def on_message(message: Message) -> None:
        logger.debug("Message %s received", message.content)
        if message.author.bot:
            logger.debug("From bot")
            return

        if message.channel.id != config["CHANEL_ID"]:
            logger.debug(
                "Channel %s and %s don't correspond",
                message.channel.id,
                config["CHANEL_ID"],
            )
            return

        await add_user_to_whitelist(message, config)
        logger.debug("Complete, deleting file")
        await message.delete()

    return bot
