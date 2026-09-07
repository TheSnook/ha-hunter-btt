"""
Custom integration to integrate Hunter BTT BLE watering system with Home Assistant.

For more details about this integration, please refer to
https://github.com/TheSnook/ha-hunter-btt
"""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_loaded_integration

from .api import HunterBTTApiClient
from .const import DOMAIN, LOGGER
from .coordinator import HunterBTTDataUpdateCoordinator
from .data import HunterBTTData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import HunterBTTConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: HunterBTTConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    coordinator = HunterBTTDataUpdateCoordinator(
        hass=hass,
        logger=LOGGER,
        name=DOMAIN,
        update_interval=timedelta(hours=1),
        config_entry=entry,
    )
    entry.runtime_data = HunterBTTData(
        client=HunterBTTApiClient(
            username=entry.data[CONF_USERNAME],
            password=entry.data[CONF_PASSWORD],
            session=async_get_clientsession(hass),
        ),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: HunterBTTConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
