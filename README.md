# Apple TV Remote — Home Assistant integration

Per-button `button.*` entities for the Apple TVs already paired in Home
Assistant's native `apple_tv` integration. Drop them into automations,
dashboards, and scripts without writing `remote.send_command` boilerplate.

This integration is the **back-end half** of the project. If you want a
visual remote card for dashboards, see the companion repo:
[`ha-apple-tv-card`](https://github.com/moimart/ha-apple-tv-card).

## What you get per Apple TV

One device with 12 buttons:

| Entity | Action |
|---|---|
| `button.<name>_home` | Top menu / Home |
| `button.<name>_back` | Menu / Back |
| `button.<name>_up` | Click pad up |
| `button.<name>_down` | Click pad down |
| `button.<name>_left` | Click pad left |
| `button.<name>_right` | Click pad right |
| `button.<name>_select` | Click pad center |
| `button.<name>_play_pause` | Toggle play / pause |
| `button.<name>_volume_up` | Volume up |
| `button.<name>_volume_down` | Volume down |
| `button.<name>_siri` | Invoke Siri (tvOS-dependent) |
| `button.<name>_power_toggle` | `turn_on` or `turn_off` depending on state |

## Requirements

- Home Assistant Core ≥ 2024.1
- The native [`apple_tv` integration](https://www.home-assistant.io/integrations/apple_tv/)
  paired with at least one Apple TV — this integration uses its
  `remote.send_command` service under the hood.

## Install via HACS

1. HACS → ⋮ → **Custom repositories** → URL: `https://github.com/moimart/ha-apple-tv-remote`,
   Type: **Integration** → **Add**.
2. Click the new card → **Download** → pick the latest tag.
3. **Settings → System → Restart Home Assistant**.
4. **Settings → Devices & Services → + Add Integration → "Apple TV Remote (button entities)"**.
5. Name the bundle, pick which Apple TV `remote.*` entity to drive,
   submit. Repeat for each Apple TV.

## License

MIT.
