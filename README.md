# Home Assistant Extra API

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![pre-commit][pre-commit-shield]][pre-commit]
[![Black][black-shield]][black]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Community Forum][forum-shield]][forum]

## Functionality

Supplemental APIs for home assistant to modify HA state programatically.

### Services

#### Update Entity

Updates all targeted entities to the specified vlaues

```yaml
service: ha_extra_api.update_entity
target:
  entity_id:
    - sensor.lux
    - binary_sensor.contact
data:
  alias:
    - Alias1
    - Alias2
  area_id: 1
  icon: mdi:home
  name: Display Name
  status: disabled
```

{% if not installed %}

## Installation

### HACS

1. Install [HACS](https://hacs.xyz/)
2. Go to HACS "Integrations >" section
3. Click 3 dots in top right
4. Click "Custom repositories"
5. Add repository https://github.com/amosyuen/ha-extra-api with category `Integration`
6. In the lower right click "+ Explore & Download repositories"
7. Search for "Home Assistant Extra API" and add it
   - HA Restart is not needed since it is configured in UI config flow
8. In the Home Assistant (HA) UI go to "Configuration"
9. Click "Integrations"
10. Click "+ Add Integration"
11. Search for "Home Assistant Extra API"

### Manual

1. Using the tool of choice open the directory (folder) for your [HA configuration](https://www.home-assistant.io/docs/configuration/) (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `ha_extra_api`.
4. Download _all_ the files from the `custom_components/ha_extra_api/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the Home Assistant (HA) UI go to "Configuration"
8. Click "Integrations"
9. Click "+ Add Integration"
10. Search for "Home Assistant Extra API"

{% endif %}

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](https://github.com/amosyuen/ha-extra-api/blob/master/CONTRIBUTING.md)

## Credits

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[black]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
[buymecoffee]: https://paypal.me/amosyuen
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/amosyuen/ha-extra-api.svg?style=for-the-badge
[commits]: https://github.com/amosyuen/ha-extra-api/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/amosyuen/ha-extra-api.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40amosyuen-blue.svg?style=for-the-badge
[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/amosyuen/ha-extra-api.svg?style=for-the-badge
[releases]: https://github.com/amosyuen/ha-extra-api/releases
[user_profile]: https://github.com/amosyuen
