import logging
from typing import Final

from zigpy.quirks.v2 import QuirkBuilder
import zigpy.types as t
from zigpy.zcl.foundation import ZCLAttributeDef
from zhaquirks.tuya.mcu import TuyaMCUCluster, DPToAttributeMapping

_LOGGER = logging.getLogger(__name__)

class PIRState(t.enum8):
    none = 0x00
    pir = 0x01

class SensitivityEnum(t.enum8):
    low = 0x00
    middle = 0x01
    high = 0x02

def convert_temperature(value):
    return value / 10

class TuyaPIRSensorCluster(TuyaMCUCluster):
    """Tuya PIR sensor for _TZE284_gnpflcoq."""
    cluster_id = 0xEF00

    class AttributeDefs(TuyaMCUCluster.AttributeDefs):
        pir_state: Final = ZCLAttributeDef(id=0x0001, type=t.uint8_t, access="rp", is_manufacturer_specific=True)
        battery: Final = ZCLAttributeDef(id=0x0004, type=t.uint8_t, access="rp", is_manufacturer_specific=True)
        temperature: Final = ZCLAttributeDef(id=0x0007, type=t.int16s, access="rp", is_manufacturer_specific=True)
        humidity: Final = ZCLAttributeDef(id=0x0008, type=t.uint16_t, access="rp", is_manufacturer_specific=True)
        pir_sensitivity: Final = ZCLAttributeDef(id=0x0009, type=t.uint8_t, access="rp", is_manufacturer_specific=True)
        illuminance: Final = ZCLAttributeDef(id=0x000B, type=t.uint32_t, access="rp", is_manufacturer_specific=True)
        pir_delay: Final = ZCLAttributeDef(id=0x000C, type=t.uint16_t, access="rp", is_manufacturer_specific=True)

    dp_to_attribute = {
        1: DPToAttributeMapping(TuyaMCUCluster.ep_attribute, "pir_state", converter=PIRState),
        4: DPToAttributeMapping(TuyaMCUCluster.ep_attribute, "battery"),
        7: DPToAttributeMapping(TuyaMCUCluster.ep_attribute, "temperature", converter=convert_temperature),
        8: DPToAttributeMapping(TuyaMCUCluster.ep_attribute, "humidity"),
        9: DPToAttributeMapping(TuyaMCUCluster.ep_attribute, "pir_sensitivity", converter=SensitivityEnum),
        11: DPToAttributeMapping(TuyaMCUCluster.ep_attribute, "illuminance"),
        12: DPToAttributeMapping(TuyaMCUCluster.ep_attribute, "pir_delay"),
    }

    data_point_handlers = {dp: "_dp_2_attr_update" for dp in dp_to_attribute.keys()}


(
    QuirkBuilder("_TZE284_gnpflcoq", "TS0601")
    .skip_configuration()
    .adds(TuyaPIRSensorCluster, endpoint_id=1)

    # PIR binary sensor
    .binary_sensor(
        "pir_state",
        TuyaPIRSensorCluster.cluster_id,
        endpoint_id=1,
        fallback_name="Motion",
        device_class="motion",
    )

    # Battery
    .sensor(
        "battery",
        TuyaPIRSensorCluster.cluster_id,
        endpoint_id=1,
        fallback_name="Battery",
        device_class="battery",
    )

    # Temperature
    .sensor(
        "temperature",
        TuyaPIRSensorCluster.cluster_id,
        endpoint_id=1,
        fallback_name="Temperature",
        device_class="temperature",
    )

    # Humidity
    .sensor(
        "humidity",
        TuyaPIRSensorCluster.cluster_id,
        endpoint_id=1,
        fallback_name="Humidity",
        device_class="humidity",
    )

    # Illuminance
    .sensor(
        "illuminance",
        TuyaPIRSensorCluster.cluster_id,
        endpoint_id=1,
        fallback_name="Illuminance",
        device_class="illuminance",
    )

    # PIR sensitivity (enum) — tuple obligatoire
    .enum(
        "pir_sensitivity",
        #("low", "middle", "high"),
        SensitivityEnum,
        TuyaPIRSensorCluster.cluster_id,
        endpoint_id=1,
        fallback_name="PIR Sensitivity",
        translation_key="pir_sensitivity",
    )

    # PIR delay (number)
    .number(
        "pir_delay",
        TuyaPIRSensorCluster.cluster_id,
        endpoint_id=1,
        min_value=10,
        max_value=180,
        step=1,
        fallback_name="PIR Delay",
        translation_key="pir_delay",
    )

    .add_to_registry()
)
