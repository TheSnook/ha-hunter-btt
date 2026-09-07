"""Custom types for hunter_btt."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import HunterBTTApiClient
    from .coordinator import HunterBTTDataUpdateCoordinator


type HunterBTTConfigEntry = ConfigEntry[HunterBTTData]


@dataclass
class HunterBTTData:
    """Data for the Hunter BTT integration."""

    client: HunterBTTApiClient
    coordinator: HunterBTTDataUpdateCoordinator
    integration: Integration
