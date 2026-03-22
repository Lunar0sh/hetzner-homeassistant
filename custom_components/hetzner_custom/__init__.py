import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_API_TOKEN
from .coordinator import HetznerDataCoordinator

_LOGGER = logging.getLogger(__name__)

# Definiert, welche Plattformen wir unterstützen (aktuell nur Sensoren)
PLATFORMS = ["sensor"]

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Wird ganz am Anfang aufgerufen, um die Integration vorzubereiten."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Richtet die Hetzner Integration aus dem gespeicherten Token ein."""
    hass.data.setdefault(DOMAIN, {})

    # API Token aus der gespeicherten Konfiguration auslesen
    api_token = entry.data.get(CONF_API_TOKEN)

    # Den Koordinator initialisieren
    coordinator = HetznerDataCoordinator(hass, api_token)

    # Ersten Datenabruf erzwingen
    await coordinator.async_config_entry_first_refresh()

    # Den Koordinator speichern, damit die sensor.py später darauf zugreifen kann
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Die sensor.py laden und die Entitäten erstellen lassen
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Wird aufgerufen, wenn die Integration gelöscht oder neu geladen wird."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
