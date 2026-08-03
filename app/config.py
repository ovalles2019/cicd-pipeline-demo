"""Runtime configuration — environment name is set at deploy time."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str
    environment: str
    version: str

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


def get_settings() -> Settings:
    from app import __version__

    return Settings(
        app_name=os.getenv("APP_NAME", "cicd-pipeline-demo"),
        environment=os.getenv("APP_ENV", "local"),
        version=os.getenv("APP_VERSION", __version__),
    )
