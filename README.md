# Home Assistant Registry

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![pre-commit][pre-commit-shield]][pre-commit]
[![Black][black-shield]][black]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Community Forum][forum-shield]][forum]

## Description

Adds services for home assistant registry operations.

> **WARNING**: These are low level APIs that only have basic validation. They are intended for power users. Misuse could result in entities getting into strange states.

HA core has decided to not support services for common registry operations mentioned in https://github.com/home-assistant/core/pull/86281#event-8320797538.

### Services

#### Remove Entity

Remove all targeted entity registry configs,

`entity_id` is a repeated field that takes comma separated values in a string or a yaml list

```yaml
service: ha_registry.remove_entity
data:
  entity_id:
    - sensor.bathroom_temperature
    - sensor.bedroom_temperature
```

#### Update Entity

Updates all targeted entity registry configs to the specified values.

`entity_id` and `aliases` are repeated fields that take comma separated values in a string or a yaml list

```yaml
service: ha_registry.update_entity
data:
  entity_id: sensor.bathroom_temperature,sensor.bedroom_temperature
  aliases:
    - Alias1
    - Alias2
  area_id: bedroom
  device_class: temperature
  disabled: true
  hidden: true
  icon: mdi:home
  name: Bedroom Temperature
  new_entity_id: sensor.new_entity_id
  options_domain: sensor
  options:
    unit_of_measurement: °F
```

{% if not installed %}

## Installation

### HACS

1. Install [HACS](https://hacs.xyz/)
2. Go to HACS "Integrations >" section
3. In the lower right click "+ Explore & Download repositories"
4. Search for "Home Assistant Registry" and add it
   - HA Restart is not needed since it is configured in UI config flow
5. In the Home Assistant (HA) UI go to "Configuration"
6. Click "Integrations"
7. Click "+ Add Integration"
8. Search for "Home Assistant Registry"

### Manual

1. Using the tool of choice open the directory (folder) for your [HA configuration](https://www.home-assistant.io/docs/configuration/) (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `ha_registry`.
4. Download _all_ the files from the `custom_components/ha_registry/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the Home Assistant (HA) UI go to "Configuration"
8. Click "Integrations"
9. Click "+ Add Integration"
10. Search for "Home Assistant Registry"

{% endif %}

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](https://github.com/amosyuen/ha-registry/blob/master/CONTRIBUTING.md)

## Credits

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[black]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
[buymecoffee]: https://paypal.me/amosyuen
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/amosyuen/ha-registry.svg?style=for-the-badge
[commits]: https://github.com/amosyuen/ha-registry/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/amosyuen/ha-registry.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40amosyuen-blue.svg?style=for-the-badge
[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/amosyuen/ha-registry.svg?style=for-the-badge
[releases]: https://github.com/amosyuen/ha-registry/releases
[user_profile]: https://github.com/amosyuen
