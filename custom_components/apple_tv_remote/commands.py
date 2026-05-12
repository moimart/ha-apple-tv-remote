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
    ButtonSpec("control_center", "Control Center", "home_hold", "mdi:view-dashboard"),
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
    ButtonSpec("wakeup", "Wake", "wakeup", "mdi:power"),
    ButtonSpec("turn_off", "Turn Off", "turn_off", "mdi:power-sleep"),
)
"""All button entities we create per config entry.

Every entry maps 1:1 to ``remote.send_command``. There's no synthetic
state-introspection logic — power on and power off are two distinct
buttons because pyatv exposes them as two distinct commands (``wakeup``
and ``turn_off``).
"""
