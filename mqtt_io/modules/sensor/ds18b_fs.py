"""
DS18S20/DS1822/DS18B20/DS1825/DS28EA00/MAX31850K temperature sensors
make sure w1_therm and w1_gpio modules are loaded to use this sensor
"""
import os
import os.path

from ...types import ConfigType, SensorValueType
from . import GenericSensor

REQUIREMENTS = ()
ALLOWED_TYPES = ["DS18S20", "DS1822", "DS18B20", "DS1825", "DS28EA00", "MAX31850K"]
CONFIG_SCHEMA = {
    "file": dict(type="string", required=True, empty=False),
    # "type": dict(
    #     type="string",
    #     required=True,
    #     empty=False,
    #     allowed=ALLOWED_TYPES + [x.lower() for x in ALLOWED_TYPES],
    # ),
}


class Sensor(GenericSensor):
    """
    Implementation of Sensor class for the one wire temperature sensors. DS18B etc.
    """

    def setup_module(self) -> None:

        # sensor_types: Dict[str, SensorType] = {s.name: s for s in list(SensorType)}
        # self.sensor_type = sensor_types[self.config["type"].upper()]
        # self.sensor = W1ThermSensor(self.sensor_type, self.config["address"].lower())
        self.file_path = f"/sys/bus/w1/devices/{self.config['file']}/temperature"
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(
                f"unable to locate 1wire temperate file under {self.file_path}")

    def get_value(self, sens_conf: ConfigType) -> SensorValueType:
        """
        Get the temperature value from the sensor
        """
        with os.open(self.file_path, 'r') as raw_file:
            raw_value = os.read(raw_file)
        return float(raw_value) / 1000
