from logging import getLogger
import aiohttp

logger = getLogger()

INSPIROBOT_API_URL = "https://inspirobot.me/api?generate=true"


async def fetch_inspirobot_quote() -> str | None:
    """Fetch a generated quote image URL from Inspirobot."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(INSPIROBOT_API_URL) as response:
                if response.status == 200:
                    return await response.text()
    except Exception as e:
        logger.error("Error fetching quote from InspiroBot: %s", e)
    return None
