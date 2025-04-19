from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status

from cgn_ec_models.sqlmodel import NATPortBlockMapping

from cgn_ec_api.config import settings
from cgn_ec_api.controllers.base import (
    BaseController,
    BaseUIController,
    BaseAPIController,
)
from cgn_ec_api.models.query import PortBlockMappingParams
from cgn_ec_api.crud.port_block_mapping import CRUDPortBlockMapping


class PortBlockMappingControllerBase(BaseController):
    CRUDController = CRUDPortBlockMapping

    async def _get(self, x_ip: str) -> NATPortBlockMapping:
        """
        Get a Port Block Mapping by x_ip, with caching.

        Args:
            x_ip: The translated IP.
            cache_timeout: Cache expiration time in seconds (default: 1 hour).

        Returns:
            NATPortBlockMapping object
        """
        record = await self.cache_get(
            cache_key=x_ip, fetch_data_func=self.crud.get, db=self.db, x_ip=x_ip
        )

        if not record:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, detail="NAT Port Block Mapping not found."
            )

        return record

    async def _get_multi(
        self,
        params: PortBlockMappingParams | None = None,
    ) -> list[NATPortBlockMapping]:
        if not params.timestamp_ge:
            current_time_utc = datetime.now(tz=timezone.utc)
            timestamp_ge = current_time_utc - timedelta(
                hours=settings.DEFAULT_LOOKBACK_HOURS
            )
            params.timestamp_ge = timestamp_ge

        records = await self.crud.get_multi(self.db, params=params)

        return records


class PortBlockMappingControllerAPI(BaseAPIController, PortBlockMappingControllerBase):
    async def get_object(self, src_ip: str) -> NATPortBlockMapping:
        return await super()._get(src_ip=src_ip)

    async def get_objects(
        self,
        params: PortBlockMappingParams | None = None,
    ) -> list[NATPortBlockMapping]:
        return await super()._get_multi(params=params)


class PortBlockMappingControllerUI(BaseUIController, PortBlockMappingControllerBase):
    async def get_object(self, *args, **kwargs) -> NATPortBlockMapping:
        raise NotImplementedError

    async def get_objects(self, *args, **kwargs) -> list[NATPortBlockMapping]:
        raise NotImplementedError
