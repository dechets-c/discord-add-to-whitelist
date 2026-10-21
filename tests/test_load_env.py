import pytest

from minecraft_auto_whitelist.load_env import get_config


@pytest.mark.parametrize(
    ("env_port", "expected_port"),
    [(None, 25575), ("25576", 25576)],
)
def test_get_config_uses_default_or_provided_rcon_port(
    monkeypatch, env_port, expected_port
):
    monkeypatch.setenv("TOKEN_BOT", "token")
    monkeypatch.setenv("CHANEL_ID", "12345")
    monkeypatch.setenv("RCON_PWORD", "secret")
    monkeypatch.setenv("SERVER_URL", "localhost")

    if env_port is None:
        monkeypatch.delenv("RCON_PORT", raising=False)
    else:
        monkeypatch.setenv("RCON_PORT", env_port)

    config = get_config()

    assert config["TOKEN"] == "token"
    assert config["CHANEL_ID"] == 12345
    assert config["RCON_PWORD"] == "secret"
    assert config["SERVER_URL"] == "localhost"
    assert config["RCON_PORT"] == expected_port
