import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock

from minecraft_auto_whitelist.minecraft_rcon import add_user_to_whitelist


def test_add_user_to_whitelist_sends_success_message(monkeypatch):
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
            return "OK"

        def disconnect(self):
            self.connected = False

    monkeypatch.setattr("minecraft_auto_whitelist.minecraft_rcon.MCRcon", FakeMCRcon)

    author = SimpleNamespace()
    author.send = AsyncMock()
    message = SimpleNamespace(content="Steve", author=author)
    config = {
        "SERVER_URL": "localhost",
        "RCON_PWORD": "secret",
        "RCON_PORT": 25575,
    }

    asyncio.run(add_user_to_whitelist(message, config))

    author.send.assert_awaited_once_with(
        "✅ Steve has been added to the server whitelist"
    )
