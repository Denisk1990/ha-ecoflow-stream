"""EcoFlow STREAM sensors based on Developer API documentation."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfPower, PERCENTAGE
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

# Mapping der Keys von der EcoFlow Developer Seite
SENSORS = {
    # Erzeugte Energie und Netz
    "pvPwr": ("Solar Gesamtleistung", UnitOfPower.WATT, SensorDeviceClass.POWER),
    "gridPwr": ("Netzleistung", UnitOfPower.WATT, SensorDeviceClass.POWER),
    "loadPwr": ("Hausverbrauch", UnitOfPower.WATT, SensorDeviceClass.POWER),
    
    # Batterie Status
    "soc": ("Batteriestand", PERCENTAGE, SensorDeviceClass.BATTERY),
    "bpPwr": ("Batterie Leistung", UnitOfPower.WATT, SensorDeviceClass.POWER),
    "backupSoc": ("Backup Reserve", PERCENTAGE, SensorDeviceClass.BATTERY),
    
    # Ausgänge und PV-Strings
    "epsPwr": ("Notstrom Ausgang", UnitOfPower.WATT, SensorDeviceClass.POWER),
    "pv1Pwr": ("Solar String 1", UnitOfPower.WATT, SensorDeviceClass.POWER),
    "pv2Pwr": ("Solar String 2", UnitOfPower.WATT, SensorDeviceClass.POWER),
    "pv3Pwr": ("Solar String 3", UnitOfPower.WATT, SensorDeviceClass.POWER),
}

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up EcoFlow STREAM sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        EcoFlowStreamSensor(coordinator, key, name, unit, device_class)
        for key, (name, unit, device_class) in SENSORS.items()
    )

class EcoFlowStreamSensor(CoordinatorEntity, SensorEntity):
    """Representation of an EcoFlow STREAM sensor."""

    def __init__(self, coordinator, key, name, unit, device_class):
        super().__init__(coordinator)
        self._key = key
        self._attr_name = f"EcoFlow STREAM {name}"
        self._attr_unique_id = f"ecoflow_stream_{key}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        """Return the state of the sensor."""
        # Sicherstellen, dass Daten vorhanden sind
        if not self.coordinator.data or not isinstance(self.coordinator.data, dict):
            return None
            
        # Abruf des Wertes; falls der Key fehlt, wird None zurückgegeben (kein Absturz)
        return self.coordinator.data.get(self._key)
