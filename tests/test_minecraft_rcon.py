import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from minecraft_auto_whitelist.minecraft_rcon import add_user_to_whitelist


@pytest.mark.parametrize(
    ("username", "server_reply", "expected_message"),
    [
        (
            "Steve",
            "Added Steve to the whitelist",
            "✅ Steve has been added to the server whitelist\n"
            "Server response: Added Steve to the whitelist",
        ),
        (
            "Steve",
            "Player is already whitelisted",
            "⚠️ Steve is already in the server whitelist\n"
            "Server response: Player is already whitelisted",
        ),
        (
            "Steve",
            "That player does not exist",
            "❌ Steve does not exist on the server\n"
            "Server response: That player does not exist",
        ),
        (
            "Steve",
            "Random unexpected output",
            "❌ Unexpected server response while adding Steve\n"
            "Server response: Random unexpected output",
        ),
    ],
)
def test_add_user_to_whitelist_sends_expected_message(
    monkeypatch, username, server_reply, expected_message
):
    class FakeMCRcon:
        def __init__(self, host, password, port):
            self.host = host
            self.password = password
            self.port = port
            self.connected = False
            self.command_calls = []

        def connect(self):
            self.connected = True

        def command(self, cmd):
            self.command_calls.append(cmd)
            return server_reply

        def disconnect(self):
            self.connected = False

    monkeypatch.setattr("minecraft_auto_whitelist.minecraft_rcon.MCRcon", FakeMCRcon)

    author = SimpleNamespace()
    author.send = AsyncMock()
    message = SimpleNamespace(content=username, author=author)
    config = {
        "SERVER_URL": "localhost",
        "RCON_PWORD": "secret",
        "RCON_PORT": 25575,
    }

    asyncio.run(add_user_to_whitelist(message, config))

    author.send.assert_awaited_once_with(expected_message)
