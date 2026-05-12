"""The catalogue of Apple TV button presses we surface as `button.*` entities.

Each tuple is ``(key, friendly name, remote.send_command argument, mdi icon)``.
Keys are stable — used in entity unique_ids — so don't rename without a
migration story.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ButtonSpec:
    """Description of one button entity bound to one Apple TV command."""

    key: str
    friendly_name: str
    remote_command: str
    icon: str


BUTTONS: tuple[ButtonSpec, ...] = (
    ButtonSpec("home", "Home", "top_menu", "mdi:apple"),
    ButtonSpec("back", "Back", "menu", "mdi:arrow-u-left-top"),
    ButtonSpec("up", "Up", "up", "mdi:chevron-up"),
    ButtonSpec("down", "Down", "down", "mdi:chevron-down"),
    ButtonSpec("left", "Left", "left", "mdi:chevron-left"),
    ButtonSpec("right", "Right", "right", "mdi:chevron-right"),
    ButtonSpec("select", "Select", "select", "mdi:circle"),
    ButtonSpec("play_pause", "Play / Pause", "play_pause", "mdi:play-pause"),
    ButtonSpec("volume_up", "Volume Up", "volume_up", "mdi:volume-plus"),
    ButtonSpec("volume_down", "Volume Down", "volume_down", "mdi:volume-minus"),
    ButtonSpec("siri", "Siri", "siri", "mdi:microphone"),
    ButtonSpec("power_toggle", "Power Toggle", "_power_toggle", "mdi:power"),
)
"""All button entities we create per config entry.

``power_toggle`` is a synthetic command — the button entity inspects the
target remote's state and sends `turn_on` or `turn_off` accordingly. All
others map 1:1 to ``remote.send_command``.
"""
