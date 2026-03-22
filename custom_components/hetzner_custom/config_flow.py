import voluptuous as vol
import logging
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_API_TOKEN

_LOGGER = logging.getLogger(__name__)

class HetznerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            # Token bereinigen (versteckte Leerzeichen entfernen)
            token = user_input[CONF_API_TOKEN].strip() 
            
            try:
                session = async_get_clientsession(self.hass)
                headers = {"Authorization": f"Bearer {token}"}
                
                # Direkter HTTP Request an die Cloud API
                async with session.get("https://api.hetzner.cloud/v1/servers", headers=headers) as response:
                    if response.status == 200:
                        user_input[CONF_API_TOKEN] = token
                        return self.async_create_entry(title="Hetzner", data=user_input)
                    elif response.status == 401:
                        errors["base"] = "invalid_token"
                    else:
                        _LOGGER.error("Hetzner API antwortete mit Statuscode: %s", response.status)
                        errors["base"] = "cannot_connect"
                        
            except Exception as e:
                _LOGGER.error("Verbindungsfehler im Config Flow: %s", e)
                errors["base"] = "cannot_connect"

        # UI Formular für den einen Token
        data_schema = vol.Schema({
            vol.Required(CONF_API_TOKEN): str,
        })

        return self.async_show_form(
            step_id="user", 
            data_schema=data_schema, 
            errors=errors
        )
