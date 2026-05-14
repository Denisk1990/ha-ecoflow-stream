"""EcoFlow STREAM API client."""

import logging

import aiohttp

_LOGGER = logging.getLogger(__name__)


class EcoFlowStreamApi:
    """Simple EcoFlow STREAM API client."""

    def __init__(self, access_key: str, secret_key: str, device_sn: str) -> None:
        self.access_key = access_key
        self.secret_key = secret_key
        self.device_sn = device_sn
        self.main_sn: str | None = None

    async def async_get_main_sn(self, session: aiohttp.ClientSession) -> str:
        """Get main device serial number."""
        url = (
            "https://api-e.ecoflow.com/iot-open/sign/device/system/main/sn"
            f"?sn={self.device_sn}"
        )

        async with session.get(url) as response:
            data = await response.json()

        _LOGGER.debug("Main SN response: %s", data)

        self.main_sn = data.get("data", {}).get("sn", self.device_sn)
        return self.main_sn

    async def async_get_all_quota(self, session: aiohttp.ClientSession) -> dict:
        """Get all quota values."""
        if self.main_sn is None:
            await self.async_get_main_sn(session)

        url = (
            "https://api-e.ecoflow.com/iot-open/sign/device/quota/all"
            f"?sn={self.main_sn}"
        )

        async with session.get(url) as response:
            data = await response.json()

        _LOGGER.debug("Quota response: %s", data)

        return data.get("data", {})
