from logging import getLogger
from os import getenv

from dotenv import load_dotenv

from env_dict import EnvDict

logger = getLogger()
load_dotenv()

logger.debug("env file loaded")

DEFAULT_PORT = 25575


def __load_var_from_env(variable: str) -> str:
    """Load the variable variable from the environnement

    Args:
        variable (str): name of the variable to load

    Raises:
        EnvironmentError: Environnement not setup up with the variable

    Returns:
        str: content of the env variable
    """
    value = getenv(variable)

    if value is None:
        raise EnvironmentError(f"Variable {variable} is not set")
    return value


def get_config() -> EnvDict:
    """Create the config file from env variables

    Returns:
        EnvDict: Information needed from environnement
    """
    try:
        RCON_PORT = int(__load_var_from_env("RCON_PORT"))
    except (ValueError, EnvironmentError) as e:
        logger.warning(
            "Port not in environnement or can't convert value to integer. Backing up to default value %d",
            DEFAULT_PORT,
        )
        RCON_PORT = DEFAULT_PORT

    CHANEL_ID = int(__load_var_from_env("CHANEL_ID"))

    return EnvDict(
        TOKEN=__load_var_from_env("TOKEN_BOT"),
        CHANEL_ID=CHANEL_ID,
        RCON_PORT=RCON_PORT,
        RCON_PWORD=__load_var_from_env("RCON_PWORD"),
        SERVER_URL=__load_var_from_env("SERVER_URL"),
    )
