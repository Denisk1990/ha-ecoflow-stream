"""EcoFlow STREAM sensors."""

from __future__ import annotations

import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfPower, PERCENTAGE
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Definition der Sensoren für das STREAM Ultra System
SENSORS = {
    "powGetPvSum": ("PV Gesamt", UnitOfPower.WATT),
    "gridConnectionPower": ("Netz Leistung", UnitOfPower.WATT),
    "powGetSysLoad": ("Hausverbrauch", UnitOfPower.WATT),
    "soc": ("Akku", PERCENTAGE),  # 'soc' ist der Standard-Key für Ultra
    "powGetBpCms": ("Akku Leistung", UnitOfPower.WATT),
    "backupReverseSoc": ("Backup Reserve", PERCENTAGE),
}


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up EcoFlow STREAM sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    # Wir erstellen die Entitäten basierend auf der SENSORS-Liste
    async_add_entities(
        EcoFlowStreamSensor(coordinator, key, name, unit)
        for key, (name, unit) in SENSORS.items()
    )


class EcoFlowStreamSensor(CoordinatorEntity, SensorEntity):
    """EcoFlow STREAM sensor."""

    def __init__(self, coordinator, key, name, unit):
        super().__init__(coordinator)
        self._key = key
        self._attr_name = f"EcoFlow STREAM {name}"
        self._attr_unique_id = f"ecoflow_stream_{key}"
        self._attr_native_unit_of_measurement = unit

    @property
    def native_value(self):
        """Return sensor value."""
        # Sicherheitsprüfung: Falls der Coordinator noch keine Daten hat
        if self.coordinator.data is None or not isinstance(self.coordinator.data, dict):
            return None

        # Versuche den Wert aus den Daten zu lesen
        value = self.coordinator.data.get(self._key)

        # Spezieller Fallback für den Akku-Stand bei der Ultra-Serie
        if value is None and self._key == "soc":
            # Falls 'soc' nicht da ist, versuche 'cmsBattSoc'
            value = self.coordinator.data.get("cmsBattSoc")

        return value
