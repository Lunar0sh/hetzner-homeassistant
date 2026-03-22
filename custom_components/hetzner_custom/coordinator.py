import logging
from datetime import timedelta, datetime, timezone

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class HetznerDataCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, api_token: str):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=60),
        )
        self.api_token = api_token

    async def _async_update_data(self):
        data = {"servers": [], "storage_boxes": []}
        session = async_get_clientsession(self.hass)
        headers = {"Authorization": f"Bearer {self.api_token}"}

        try:
            # 1. Server-Liste abrufen
            async with session.get("https://api.hetzner.cloud/v1/servers", headers=headers) as response:
                if response.status != 200:
                    _LOGGER.warning("Cloud API Fehler: %s", response.status)
                    servers_json = {"servers": []}
                else:
                    servers_json = await response.json()

            now = datetime.now(timezone.utc)
            start = (now - timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
            end = now.strftime("%Y-%m-%dT%H:%M:%SZ")

            # 2. Metriken für JEDEN Server abrufen
            for server in servers_json.get("servers", []):
                srv_id = server["id"]
                
                srv_data = {
                    "id": srv_id,
                    "name": server["name"],
                    "status": server["status"],
                    "cores": server.get("server_type", {}).get("cores", 0),
                    "ingoing_traffic_gib": round(server.get("ingoing_traffic", 0) / (1024**3), 2),
                    "outgoing_traffic_gib": round(server.get("outgoing_traffic", 0) / (1024**3), 2),
                    "cpu_usage": 0.0,
                    "disk_iops": 0.0,
                    "disk_throughput": 0.0,
                    "network_pps": 0.0,
                    "network_bandwidth": 0.0
                }

                metrics_url = f"https://api.hetzner.cloud/v1/servers/{srv_id}/metrics?type=cpu,disk,network&start={start}&end={end}&step=60"
                async with session.get(metrics_url, headers=headers) as met_resp:
                    if met_resp.status == 200:
                        met_json = await met_resp.json()
                        ts = met_json.get("metrics", {}).get("time_series", {})
                        
                        def get_last_valid_val(key):
                            try:
                                vals = ts.get(key, {}).get("values", [])
                                for v in reversed(vals):
                                    if v[1] is not None and str(v[1]).lower() not in ("nan", "null", ""):
                                        return float(v[1])
                            except Exception:
                                pass
                            return 0.0

                        # Metriken auslesen (jetzt mit den korrekten Punkten im JSON-Key)
                        srv_data["cpu_usage"] = round(get_last_valid_val("cpu"), 2)
                        srv_data["disk_iops"] = round(get_last_valid_val("disk.0.iops.read") + get_last_valid_val("disk.0.iops.write"), 1)
                        srv_data["disk_throughput"] = round(get_last_valid_val("disk.0.bandwidth.read") + get_last_valid_val("disk.0.bandwidth.write"), 1)
                        srv_data["network_pps"] = round(get_last_valid_val("network.0.pps.in") + get_last_valid_val("network.0.pps.out"), 1)
                        srv_data["network_bandwidth"] = round(get_last_valid_val("network.0.bandwidth.in") + get_last_valid_val("network.0.bandwidth.out"), 1)
                    else:
                        _LOGGER.warning(f"Fehler bei Metriken für {server['name']}: {met_resp.status}")

                data["servers"].append(srv_data)

            # 3. Storage Box Daten abrufen (mit Umrechnung in GiB)
            async with session.get("https://api.hetzner.com/v1/storage_boxes", headers=headers) as response:
                if response.status == 200:
                    json_data = await response.json()
                    
                    for box in json_data.get("storage_boxes", []):
                        raw_quota = box.get("storage_box_type", {}).get("size", 0)
                        raw_usage = box.get("stats", {}).get("size", 0)
                        
                        data["storage_boxes"].append({
                            "id": box.get("id"),
                            "name": box.get("name"),
                            "disk_quota": round(raw_quota / (1024**3), 2),
                            "disk_usage": round(raw_usage / (1024**3), 2),
                        })
                else:
                    _LOGGER.warning(f"Fehler beim Abruf der Storage Boxen: Status {response.status}")

            return data

        except Exception as err:
            raise UpdateFailed(f"Kommunikationsfehler: {err}")
