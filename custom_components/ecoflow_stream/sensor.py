"""EcoFlow STREAM sensors."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfPower, PERCENTAGE
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


SENSORS = {
    "powGetPvSum": ("PV Gesamt", UnitOfPower.WATT),
    "gridConnectionPower": ("Netz Leistung", UnitOfPower.WATT),
    "powGetSysLoad": ("Hausverbrauch", UnitOfPower.WATT),
    "cmsBattSoc": ("Akku", PERCENTAGE),
    "powGetBpCms": ("Akku Leistung", UnitOfPower.WATT),
    "backupReverseSoc": ("Backup Reserve", PERCENTAGE),
}


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up EcoFlow STREAM sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

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
        return self.coordinator.data.get(self._key)
