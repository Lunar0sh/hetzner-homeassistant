from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import UnitOfInformation, UnitOfDataRate

from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    entities = []
    
    # Server Sensoren
    for server in coordinator.data.get("servers", []):
        entities.append(HetznerServerStatusSensor(coordinator, server["id"], server["name"]))
        entities.append(HetznerServerCoresSensor(coordinator, server["id"], server["name"]))
        entities.append(HetznerServerCPUUsageSensor(coordinator, server["id"], server["name"]))
        entities.append(HetznerServerTrafficInSensor(coordinator, server["id"], server["name"]))
        entities.append(HetznerServerTrafficOutSensor(coordinator, server["id"], server["name"]))
        entities.append(HetznerServerDiskIOPSSensor(coordinator, server["id"], server["name"]))
        entities.append(HetznerServerDiskThroughputSensor(coordinator, server["id"], server["name"]))
        entities.append(HetznerServerNetworkPPSSensor(coordinator, server["id"], server["name"]))
        entities.append(HetznerServerNetworkBandwidthSensor(coordinator, server["id"], server["name"]))

    # Storage Box Sensoren
    for box in coordinator.data.get("storage_boxes", []):
        entities.append(HetznerStorageBoxUsageSensor(coordinator, box["id"], box["name"]))
        entities.append(HetznerStorageBoxQuotaSensor(coordinator, box["id"], box["name"]))

    async_add_entities(entities)

# --- CLOUD SERVER SENSOREN ---

class HetznerBaseSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, server_id, server_name):
        super().__init__(coordinator)
        self.server_id = server_id
        self.server_name = server_name

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"server_{self.server_id}")},
            "name": self.server_name,
            "manufacturer": "Hetzner Cloud",
            "model": "Cloud Server",
        }

    def get_server_data(self, key):
        for server in self.coordinator.data.get("servers", []):
            if server["id"] == self.server_id:
                return server.get(key)
        return None

class HetznerServerStatusSensor(HetznerBaseSensor):
    def __init__(self, coordinator, server_id, server_name):
        super().__init__(coordinator, server_id, server_name)
        self._attr_name = f"{server_name} Status"
        self._id = f"hetzner_server_status_{server_id}"
        self._attr_icon = "mdi:server-network"

    @property
    def unique_id(self): return self._id

    @property
    def native_value(self): return self.get_server_data("status")

class HetznerServerCoresSensor(HetznerBaseSensor):
    def __init__(self, coordinator, server_id, server_name):
        super().__init__(coordinator, server_id, server_name)
        self._attr_name = f"{server_name} CPU Kerne"
        self._id = f"hetzner_server_cores_{server_id}"
        self._attr_icon = "mdi:cpu-64-bit"

    @property
    def unique_id(self): return self._id

    @property
    def native_value(self): return self.get_server_data("cores")

class HetznerServerCPUUsageSensor(HetznerBaseSensor):
    def __init__(self, coordinator, server_id, server_name):
        super().__init__(coordinator, server_id, server_name)
        self._attr_name = f"{server_name} CPU Auslastung"
        self._id = f"hetzner_server_cpu_usage_{server_id}"
        self._attr_native_unit_of_measurement = "%"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:chart-line"

    @property
    def unique_id(self): return self._id

    @property
    def native_value(self): return self.get_server_data("cpu_usage")

class HetznerServerTrafficInSensor(HetznerBaseSensor):
    def __init__(self, coordinator, server_id, server_name):
        super().__init__(coordinator, server_id, server_name)
        self._attr_name = f"{server_name} Traffic In"
        self._id = f"hetzner_server_traffic_in_{server_id}"
        self._attr_native_unit_of_measurement = UnitOfInformation.GIGABYTES
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_icon = "mdi:download-network"

    @property
    def unique_id(self): return self._id

    @property
    def native_value(self): return self.get_server_data("ingoing_traffic_gib")

class HetznerServerTrafficOutSensor(HetznerBaseSensor):
    def __init__(self, coordinator, server_id, server_name):
        super().__init__(coordinator, server_id, server_name)
        self._attr_name = f"{server_name} Traffic Out"
        self._id = f"hetzner_server_traffic_out_{server_id}"
        self._attr_native_unit_of_measurement = UnitOfInformation.GIGABYTES
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_icon = "mdi:upload-network"

    @property
    def unique_id(self): return self._id

    @property
    def native_value(self): return self.get_server_data("outgoing_traffic_gib")

class HetznerServerDiskIOPSSensor(HetznerBaseSensor):
    def __init__(self, coordinator, server_id, server_name):
        super().__init__(coordinator, server_id, server_name)
        self._attr_name = f"{server_name} Disk IOPS"
        self._id = f"hetzner_server_disk_iops_{server_id}"
        self._attr_native_unit_of_measurement = "IOPS"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:harddisk"

    @property
    def unique_id(self): return self._id

    @property
    def native_value(self): return self.get_server_data("disk_iops")

class HetznerServerDiskThroughputSensor(HetznerBaseSensor):
    def __init__(self, coordinator, server_id, server_name):
        super().__init__(coordinator, server_id, server_name)
        self._attr_name = f"{server_name} Disk Durchsatz"
        self._id = f"hetzner_server_disk_throughput_{server_id}"
        self._attr_device_class = SensorDeviceClass.DATA_RATE
        self._attr_native_unit_of_measurement = UnitOfDataRate.BYTES_PER_SECOND
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:swap-vertical"

    @property
    def unique_id(self): return self._id

    @property
    def native_value(self): return self.get_server_data("disk_throughput")

class HetznerServerNetworkPPSSensor(HetznerBaseSensor):
    def __init__(self, coordinator, server_id, server_name):
        super().__init__(coordinator, server_id, server_name)
        self._attr_name = f"{server_name} Network PPS"
        self._id = f"hetzner_server_network_pps_{server_id}"
        self._attr_native_unit_of_measurement = "pps"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:lan"

    @property
    def unique_id(self): return self._id

    @property
    def native_value(self): return self.get_server_data("network_pps")

class HetznerServerNetworkBandwidthSensor(HetznerBaseSensor):
    def __init__(self, coordinator, server_id, server_name):
        super().__init__(coordinator, server_id, server_name)
        self._attr_name = f"{server_name} Network Bandbreite"
        self._id = f"hetzner_server_network_bandwidth_{server_id}"
        self._attr_device_class = SensorDeviceClass.DATA_RATE
        self._attr_native_unit_of_measurement = UnitOfDataRate.BYTES_PER_SECOND
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:speedometer"

    @property
    def unique_id(self): return self._id

    @property
    def native_value(self): return self.get_server_data("network_bandwidth")


# --- STORAGE BOX SENSOREN ---

class HetznerStorageBaseSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, box_id, box_name):
        super().__init__(coordinator)
        self.box_id = box_id
        self.box_name = box_name

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"storagebox_{self.box_id}")},
            "name": self.box_name,
            "manufacturer": "Hetzner",
            "model": "Storage Box",
        }

    def get_box_data(self, key):
        for box in self.coordinator.data.get("storage_boxes", []):
            if box["id"] == self.box_id:
                return box.get(key)
        return None

class HetznerStorageBoxUsageSensor(HetznerStorageBaseSensor):
    def __init__(self, coordinator, box_id, box_name):
        super().__init__(coordinator, box_id, box_name)
        self._attr_name = f"{box_name} Belegt"
        self._id = f"hetzner_storage_box_usage_{box_id}"
        self._attr_device_class = SensorDeviceClass.DATA_SIZE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfInformation.GIGABYTES
        self._attr_icon = "mdi:harddisk"

    @property
    def unique_id(self): return self._id

    @property
    def native_value(self): return self.get_box_data("disk_usage")

class HetznerStorageBoxQuotaSensor(HetznerStorageBaseSensor):
    def __init__(self, coordinator, box_id, box_name):
        super().__init__(coordinator, box_id, box_name)
        self._attr_name = f"{box_name} Kapazität"
        self._id = f"hetzner_storage_box_quota_{box_id}"
        self._attr_device_class = SensorDeviceClass.DATA_SIZE
        self._attr_native_unit_of_measurement = UnitOfInformation.GIGABYTES
        self._attr_icon = "mdi:harddisk-plus"

    @property
    def unique_id(self): return self._id

    @property
    def native_value(self): return self.get_box_data("disk_quota")
