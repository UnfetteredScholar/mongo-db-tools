from enum import StrEnum
from logging import getLogger
from typing import Literal

import httpx
from core.authentication.auth_middleware import get_current_token
from core.config import settings
from fastapi import Depends
from schemas.token import TokenData


class PlatformIntegrationClient:
    def __init__(self, auth_token: str):
        """Creates a PlatformIntegrationClient object"""
        self.auth_token = auth_token

    def get_power_automate_flow(self, flow_name_or_objId: str) -> dict[str, str]:
        """Get the details for a user flow"""
        logger = getLogger(__name__ + ".get_power_automate_flow")

        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            url = f"{settings.PLATFRORM_INT_URL}/api/v1/power_automate/flows/{flow_name_or_objId}"

            response = httpx.get(url=url, headers=headers, timeout=60)

            if response.is_success:
                res = response.json()
                return res
            else:
                logger.error(f"({response.status_code}) {response.content}")
                raise Exception("Unable to get flow details")
        except Exception as ex:
            logger.exception(ex)
            raise ex

    def get_graph_token(self, scope: Literal["graph:mail", "graph:people"]) -> str:
        """Gets a microsoft graph token for the selected scope set"""
        logger = getLogger(__name__ + ".get_graph_token")

        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            url = f"{settings.PLATFRORM_INT_URL}/api/v1/ms-graph/token"
            params = {"scope": scope}

            response = httpx.get(url=url, headers=headers, timeout=60, params=params)

            if response.is_success:
                res = response.json()

                access_token = res.get("access_token")
                return access_token
            else:
                logger.error(f"({response.status_code}) {response.content}")
                raise Exception(f"Unable to get graph token: {response.content}")
        except Exception as ex:
            logger.exception(ex)
            raise ex

    def get_mongodb_details(self, mongo_project: str) -> dict[str, str]:
        """Gets the details for a mongodb database"""
        logger = getLogger(__name__ + ".get_mongodb_details")

        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            url = f"{settings.PLATFRORM_INT_URL}/api/v1/mongodb_connections/{mongo_project}"

            response = httpx.get(url=url, headers=headers, timeout=60)

            if response.is_success:
                res = response.json()
                return res
            else:
                logger.error(f"({response.status_code}) {response.content}")
                raise Exception(f"Unable to get mongodb details: {response.content}")
        except Exception as ex:
            logger.exception(ex)
            raise ex


def get_platform_client(
    current_token: TokenData = Depends(get_current_token),
) -> PlatformIntegrationClient:
    """Gets platform integration client for user"""

    client = PlatformIntegrationClient(current_token.access_token)

    return client
