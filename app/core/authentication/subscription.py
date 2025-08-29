import time
from logging import getLogger
from typing import Literal

import httpx
from core.authentication.auth_middleware import get_current_token
from core.config import settings
from fastapi import Depends, HTTPException
from schemas.token import TokenData

SubscriptionTier = Literal["FREE", "BASIC", "STANDARD", "PRO", "ENTERPRISE"]


class TimedCache:
    def __init__(self, ttl: int = 60, maxsize: int = 128):
        self.ttl = ttl
        self.maxsize = maxsize
        self._cache: tuple[str, tuple[str, float]] = {}

    async def get_subscription_info(self, headers: dict | None = None) -> SubscriptionTier:
        logger = getLogger(__name__ + ".get_subscription_info")
        MARKETPLACE_URL = settings.MARKETPLACE_URL.strip("/") + "/api/v1/subscription"
        headers = headers or {}
        key = (MARKETPLACE_URL, tuple(sorted(headers.items())))
        now = time.time()

        # Check if cached
        if key in self._cache:
            value, timestamp = self._cache[key]
            if now - timestamp < self.ttl:
                return value
            else:
                # expired
                self._cache.pop(key)

        # Fetch fresh
        async with httpx.AsyncClient() as client:

            response = await client.get(MARKETPLACE_URL, headers=headers)
            try:
                response.raise_for_status()
                body = response.json().get("subscription_package", {}).get("tier", "FREE").upper()
                logger.info(f"Subscription tier: {body}")
            except Exception as ex:
                body = "FREE"

        # Store
        if len(self._cache) >= self.maxsize:
            # drop oldest
            oldest_key = min(self._cache, key=lambda k: self._cache[k][1])
            self._cache.pop(oldest_key)

        self._cache[key] = (body, now)
        return body


timed_cache = TimedCache(ttl=500, maxsize=256)


async def validate_subscription(current_token: TokenData = Depends(get_current_token)) -> SubscriptionTier:
    TIER_VALUE = {
        "FREE": 0,
        "BASIC": 1,
        "STANDARD": 2,
        "PRO": 3,
        "ENTERPRISE": 4,
    }
    subscription_info = await timed_cache.get_subscription_info(
        headers={"Authorization": f"Bearer {current_token.access_token}"}
    )
    if TIER_VALUE[subscription_info] < TIER_VALUE[settings.SERVICE_TIER.upper()]:
        raise HTTPException(
            status_code=403,
            detail=f"Forbidden: You need a {settings.SERVICE_TIER} tier or higher subscription to access this resource",
        )

    return subscription_info
