"""Test entity_registry API."""
import pytest
from custom_components.ha_registry import async_setup_entry
from custom_components.ha_registry.const import DOMAIN
from custom_components.ha_registry.const import SERVICE_REMOVE_ENTITY
from custom_components.ha_registry.const import SERVICE_UPDATE_ENTITY
from homeassistant.const import ATTR_DEVICE_CLASS
from homeassistant.const import ATTR_ICON
from homeassistant.exceptions import NoEntitySpecifiedError
from homeassistant.helpers.device_registry import DeviceEntryDisabler
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry
from homeassistant.helpers.entity_registry import RegistryEntry
from homeassistant.helpers.entity_registry import RegistryEntryDisabler
from homeassistant.helpers.entity_registry import RegistryEntryHider
from pytest_homeassistant_custom_component.common import mock_device_registry
from pytest_homeassistant_custom_component.common import mock_registry
from pytest_homeassistant_custom_component.common import MockConfigEntry
from pytest_homeassistant_custom_component.common import MockEntity
from pytest_homeassistant_custom_component.common import MockEntityPlatform


@pytest.fixture
async def entity_registry(hass):
    """Return an loaded, registry."""
    entity_registry = mock_registry(
        hass,
        {
            "test_domain.world": RegistryEntry(
                entity_id="test_domain.world",
                unique_id="1234",
                platform="test_platform",
                name="before update",
                icon="icon:before update",
            )
        },
    )
    platform = MockEntityPlatform(hass)
    entity = MockEntity(unique_id="1234")
    await platform.async_add_entities([entity])
    return entity_registry


@pytest.fixture
def device_registry(hass):
    """Return an empty, loaded, registry."""
    return mock_device_registry(hass)


async def test_update_entity(hass, entity_registry):
    """Test updating entity."""

    await async_setup_entry(hass, {})

    # UPDATE AREA, DEVICE_CLASS, ICON, AND NAME
    await hass.services.async_call(
        DOMAIN,
        SERVICE_UPDATE_ENTITY,
        {
            "entity_id": "test_domain.world",
            "aliases": ["alias_1", "alias_2"],
            "area_id": "mock-area-id",
            "device_class": "custom_device_class",
            "icon": "icon:after update",
            "name": "after update",
        },
        blocking=True,
    )

    state = hass.states.get("test_domain.world")
    assert state.attributes[ATTR_DEVICE_CLASS] == "custom_device_class"
    assert state.attributes[ATTR_ICON] == "icon:after update"
    assert state.name == "after update"
    entry = entity_registry.entities["test_domain.world"]
    assert entry.aliases == {"alias_1", "alias_2"}
    assert entry.area_id == "mock-area-id"


async def test_update_entity_disabled_and_hidden(hass, entity_registry):
    """Test updating entity disabled and hidden."""

    await async_setup_entry(hass, {})

    # Disable and hide
    await hass.services.async_call(
        DOMAIN,
        SERVICE_UPDATE_ENTITY,
        {
            "entity_id": ["test_domain.world"],
            "disabled": True,
            "hidden": True,
        },
        blocking=True,
    )

    assert hass.states.get("test_domain.world") is None
    assert (
        entity_registry.entities["test_domain.world"].disabled_by
        is RegistryEntryDisabler.USER
    )
    assert (
        entity_registry.entities["test_domain.world"].hidden_by
        is RegistryEntryHider.USER
    )

    # Enable and unhide
    await hass.services.async_call(
        DOMAIN,
        SERVICE_UPDATE_ENTITY,
        {
            "entity_id": "test_domain.world",
            "disabled": False,
            "hidden": False,
        },
        blocking=True,
    )

    assert entity_registry.entities["test_domain.world"].disabled_by is None
    assert entity_registry.entities["test_domain.world"].hidden_by is None


async def test_enable_entity_disabled_device(hass, device_registry):
    """Test enabling entity of disabled device."""

    await async_setup_entry(hass, {})

    entity_id = "test_domain.test_platform_1234"
    config_entry = MockConfigEntry(domain="test_platform")
    config_entry.add_to_hass(hass)

    device = device_registry.async_get_or_create(
        config_entry_id="1234",
        connections={("ethernet", "12:34:56:78:90:AB:CD:EF")},
        identifiers={("bridgeid", "0123")},
        manufacturer="manufacturer",
        model="model",
        disabled_by=DeviceEntryDisabler.USER,
    )
    device_info = {
        "connections": {("ethernet", "12:34:56:78:90:AB:CD:EF")},
    }

    platform = MockEntityPlatform(hass)
    platform.config_entry = config_entry
    entity = MockEntity(unique_id="1234", device_info=device_info)
    await platform.async_add_entities([entity])

    state = hass.states.get(entity_id)
    assert state is None

    entity_registry = async_get_entity_registry(hass)
    entity_entry = entity_registry.async_get(entity_id)
    assert entity_entry.config_entry_id == config_entry.entry_id
    assert entity_entry.device_id == device.id
    assert entity_entry.disabled_by == RegistryEntryDisabler.DEVICE

    # Enable
    with pytest.raises(ValueError):
        await hass.services.async_call(
            DOMAIN,
            SERVICE_UPDATE_ENTITY,
            {
                "entity_id": entity_id,
                "disabled": False,
            },
            blocking=True,
        )


async def test_update_entity_option(hass, entity_registry):
    """Test updating entity option."""

    await async_setup_entry(hass, {})

    await hass.services.async_call(
        DOMAIN,
        SERVICE_UPDATE_ENTITY,
        {
            "entity_id": "test_domain.world",
            "options_domain": "sensor",
            "options": {"unit_of_measurement": "beard_second"},
        },
        blocking=True,
    )

    assert entity_registry.entities["test_domain.world"].options == {
        "sensor": {"unit_of_measurement": "beard_second"}
    }


async def test_update_entity_id(hass, entity_registry):
    """Test update entity id."""

    await async_setup_entry(hass, {})

    assert entity_registry.async_is_registered("test_domain.world") is not None

    await hass.services.async_call(
        DOMAIN,
        SERVICE_UPDATE_ENTITY,
        {
            "entity_id": "test_domain.world",
            "new_entity_id": "test_domain.planet",
        },
        blocking=True,
    )

    assert not entity_registry.async_is_registered("test_domain.world")
    assert entity_registry.async_is_registered("test_domain.planet")


async def test_update_non_existing_entity(hass):
    """Test update non existing entity."""

    await async_setup_entry(hass, {})

    mock_registry(hass, {})

    with pytest.raises(NoEntitySpecifiedError):
        await hass.services.async_call(
            DOMAIN,
            SERVICE_UPDATE_ENTITY,
            {
                "entity_id": ["test_domain.world"],
            },
            blocking=True,
        )


async def test_remove_entity(hass):
    """Test removing entity."""

    await async_setup_entry(hass, {})

    registry = mock_registry(
        hass,
        {
            "test_domain.world": RegistryEntry(
                entity_id="test_domain.world",
                unique_id="1234",
                # Using component.async_add_entities is equal to platform "domain"
                platform="test_platform",
                name="before update",
            ),
            "test_domain.world2": RegistryEntry(
                entity_id="test_domain.world2",
                unique_id="12345",
                # Using component.async_add_entities is equal to platform "domain"
                platform="test_platform",
                name="before update",
            ),
        },
    )

    await hass.services.async_call(
        DOMAIN,
        SERVICE_REMOVE_ENTITY,
        {
            "entity_id": ["test_domain.world", "test_domain.world2"],
        },
        blocking=True,
    )

    assert len(registry.entities) == 0


async def test_remove_non_existing_entity(hass):
    """Test removing non existing entity."""

    await async_setup_entry(hass, {})

    mock_registry(hass, {})

    with pytest.raises(NoEntitySpecifiedError):
        await hass.services.async_call(
            DOMAIN,
            SERVICE_REMOVE_ENTITY,
            {
                "entity_id": ["test_domain.world"],
            },
            blocking=True,
        )
