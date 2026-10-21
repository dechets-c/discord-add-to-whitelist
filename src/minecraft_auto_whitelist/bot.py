import argparse
from logging import DEBUG, basicConfig, getLevelName, getLogger

from load_env import get_config
from setup_bot import get_bot

logger = getLogger()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the Minecraft Whitelist Discord Bot."
    )
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug-level logging."
    )
    parser.add_argument(
        "--log-level",
        type=str.upper,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    log_level = DEBUG if args.debug else getLevelName(args.log_level)

    basicConfig(
        level=log_level,
        format="[{asctime}] [{levelname:<8}] {name}: {message}",
        style="{",
    )

    logger.info("Stating application")

    config = get_config()

    bot = get_bot(config)

    bot.run(config["TOKEN"])


if __name__ == "__main__":
    main()
