"""The Home Assistant Extra API integration."""
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_AREA_ID
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.const import ATTR_ICON
from homeassistant.const import ATTR_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity_registry import RegistryEntryDisabler
from homeassistant.helpers.entity_registry import RegistryEntryHider
from homeassistant.helpers.typing import UNDEFINED

from .const import ATTR_ALIAS
from .const import ATTR_STATUS
from .const import DOMAIN
from .const import SERVICE_UPDATE_ENTITY
from .const import STATUS_DISABLED
from .const import STATUS_ENABLED
from .const import STATUS_HIDDEN


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Home Assistant Extra API from a config entry."""

    async def async_update_entity(call):
        """Enable a user by service call"""
        entities = call.data.get(ATTR_ENTITY_ID)
        if not isinstance(entities, list):
            entities = [entities]

        aliases = call.data.get(ATTR_ALIAS, UNDEFINED)
        area_id = call.data.get(ATTR_AREA_ID, UNDEFINED)
        icon = call.data.get(ATTR_ICON, UNDEFINED)
        name = call.data.get(ATTR_NAME, UNDEFINED)

        if aliases != UNDEFINED and not isinstance(aliases, list):
            aliases = [aliases]

        status = call.data.get(ATTR_STATUS)
        if status == STATUS_ENABLED:
            disabled_by = None
            hidden_by = None
        elif status == STATUS_DISABLED:
            disabled_by = RegistryEntryDisabler.USER
            hidden_by = None
        elif status == STATUS_HIDDEN:
            disabled_by = None
            hidden_by = RegistryEntryHider.USER
        else:
            disabled_by = UNDEFINED
            hidden_by = UNDEFINED

        entity_registry = hass.helpers.entity_registry.async_get(hass)
        for entity_id in entities:
            entity_registry.async_update_entity(
                entity_id,
                aliases=aliases,
                area_id=area_id,
                disabled_by=disabled_by,
                hidden_by=hidden_by,
                icon=icon,
                name=name,
            )

    hass.services.register(
        DOMAIN,
        SERVICE_UPDATE_ENTITY,
        async_update_entity,
        schema=vol.Schema(
            {
                vol.Optional(ATTR_ALIAS): vol.All(cv.ensure_list, [cv.string]),
                vol.Optional(ATTR_AREA_ID): cv.string,
                vol.Required(ATTR_ENTITY_ID): cv.entity_ids,
                vol.Optional(ATTR_ICON): cv.string,
                vol.Optional(ATTR_NAME): cv.string,
                vol.Optional(ATTR_STATUS): vol.Any(
                    STATUS_ENABLED, STATUS_DISABLED, STATUS_HIDDEN
                ),
            }
        ),
    )

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Unload a config entry."""
    return True
