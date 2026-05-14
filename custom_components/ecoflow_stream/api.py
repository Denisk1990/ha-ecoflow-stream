"""EcoFlow STREAM API client."""

from __future__ import annotations

import hashlib
import hmac
import logging
import time
from urllib.parse import urlencode

import aiohttp

_LOGGER = logging.getLogger(__name__)

BASE_URL = "https://api-e.ecoflow.com"


class EcoFlowStreamApi:
    """EcoFlow STREAM API client."""

    def __init__(self, access_key: str, secret_key: str, device_sn: str) -> None:
        self.access_key = access_key
        self.secret_key = secret_key
        self.device_sn = device_sn
        self.main_sn: str | None = None

    def _headers(self, params: dict | None = None) -> dict:
        """Create EcoFlow signed headers."""
        nonce = str(int(time.time() * 1000))
        timestamp = str(int(time.time() * 1000))

        sign_params = {
            "accessKey": self.access_key,
            "nonce": nonce,
            "timestamp": timestamp,
        }

        if params:
            sign_params.update(params)

        sign_str = urlencode(sorted(sign_params.items()))

        sign = hmac.new(
            self.secret_key.encode("utf-8"),
            sign_str.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        return {
            "accessKey": self.access_key,
            "nonce": nonce,
            "timestamp": timestamp,
            "sign": sign,
        }

    async def _get(self, session: aiohttp.ClientSession, path: str, params: dict) -> dict:
        """Send signed GET request."""
        url = f"{BASE_URL}{path}"

        async with session.get(
            url,
            params=params,
            headers=self._headers(params),
        ) as response:
            data = await response.json()

        _LOGGER.debug("EcoFlow GET %s response: %s", path, data)
        return data

    async def async_get_main_sn(self, session: aiohttp.ClientSession) -> str:
        """Get main device serial number."""
        data = await self._get(
            session,
            "/iot-open/sign/device/system/main/sn",
            {"sn": self.device_sn},
        )

        self.main_sn = data.get("data", {}).get("sn", self.device_sn)
        return self.main_sn

    async def async_get_all_quota(self, session: aiohttp.ClientSession) -> dict:
        """Get all quota values."""
        if self.main_sn is None:
            await self.async_get_main_sn(session)

        data = await self._get(
            session,
            "/iot-open/sign/device/quota/all",
            {"sn": self.main_sn},
        )

        return data.get("data", {})
