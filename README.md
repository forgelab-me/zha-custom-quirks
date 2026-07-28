# Zigbee Custom Quirks

Personal Zigbee quirks for [Home Assistant ZHA](https://www.home-assistant.io/integrations/zha/).

- **TS0601 PIR** (`_TZE284_gnpflcoq`) — Tuya motion sensor with temperature, humidity, illuminance, battery, sensitivity and PIR delay.

## Installation

ZHA loads custom quirks from a local folder via the `custom_quirks_path` option.

1. Copy this repo's [`zha_custom_quirks/`](zha_custom_quirks) folder into your Home Assistant configuration, e.g. `/config/zha_custom_quirks/`.
2. Add (or update) in `configuration.yaml`:

   ```yaml
   zha:
     custom_quirks_path: /config/zha_custom_quirks/
   ```

3. Restart Home Assistant.
4. Check the ZHA logs (search for `Loaded custom quirks`) to confirm the files were picked up.

## Included quirks

### TS0601 PIR
- Motion detection (binary_sensor)
- Temperature (with conversion)
- Humidity
- Illuminance
- Battery
- PIR sensitivity (configurable)
- PIR delay (configurable)

See [`docs/ts0601.md`](docs/ts0601.md) for datapoint details, mapping, and recommended `customize.yaml` settings (units, statistics).

## Contributing

Feedback and PRs for other Tuya/Zigbee devices are welcome — open an issue on [this repo](https://github.com/forgelab-me/zha-custom-quirks).

## License

[MIT](LICENSE)
