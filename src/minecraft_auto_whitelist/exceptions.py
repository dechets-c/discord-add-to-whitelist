"""Custom exceptions for Minecraft whitelist/RCON flows."""


class WhitelistError(Exception):
    """Base error for whitelist operations."""


class PlayerDoesNotExistError(WhitelistError):
    """Raised when the Minecraft player does not exist."""


class PlayerAlreadyWhitelistedError(WhitelistError):
    """Raised when the player is already in whitelist."""


class UnknownWhitelistResponseError(WhitelistError):
    """Raised when the server response cannot be classified."""
