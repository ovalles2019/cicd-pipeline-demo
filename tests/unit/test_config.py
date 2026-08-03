"""Unit tests for settings helpers."""

from __future__ import annotations

import os
from unittest.mock import patch

from app.config import Settings, get_settings


def test_settings_is_production() -> None:
    prod = Settings(app_name="demo", environment="production", version="1.0.0")
    local = Settings(app_name="demo", environment="local", version="1.0.0")
    assert prod.is_production is True
    assert local.is_production is False


def test_get_settings_reads_env() -> None:
    with patch.dict(
        os.environ,
        {
            "APP_NAME": "demo-app",
            "APP_ENV": "qa",
            "APP_VERSION": "9.9.9",
        },
        clear=False,
    ):
        settings = get_settings()
    assert settings.app_name == "demo-app"
    assert settings.environment == "qa"
    assert settings.version == "9.9.9"
