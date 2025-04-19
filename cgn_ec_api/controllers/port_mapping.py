from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status

from cgn_ec_models.sqlmodel import NATPortMapping

from cgn_ec_api.config import settings
from cgn_ec_api.controllers.base import (
    BaseController,
    BaseUIController,
    BaseAPIController,
)
from cgn_ec_api.models.query import PortMappingParams
from cgn_ec_api.crud.port_mapping import CRUDPortMapping


class PortMappingControllerBase(BaseController):
    CRUDController = CRUDPortMapping

    async def _get(self, src_ip: str) -> NATPortMapping:
        """
        Get a Port Mapping by src_ip, with caching.

        Args:
            src_ip: The src_ip of the record.
            cache_timeout: Cache expiration time in seconds (default: 1 hour).

        Returns:
            NATPortMapping object
        """
        record = await self.cache_get(
            cache_key=src_ip,
            fetch_data_func=self.crud.get,
            db=self.db,
            src_ip=src_ip,
        )

        if not record:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, detail="NAT Port Mapping not found."
            )

        return record

    async def _get_multi(
        self,
        params: PortMappingParams | None = None,
    ) -> list[NATPortMapping]:
        if not params.timestamp_ge:
            current_time_utc = datetime.now(tz=timezone.utc)
            timestamp_ge = current_time_utc - timedelta(
                hours=settings.DEFAULT_LOOKBACK_HOURS
            )
            params.timestamp_ge = timestamp_ge

        records = await self.crud.get_multi(self.db, params=params)

        return records


class PortMappingControllerAPI(BaseAPIController, PortMappingControllerBase):
    async def get_object(self, src_ip: str) -> NATPortMapping:
        return await super()._get(src_ip=src_ip)

    async def get_objects(
        self,
        params: PortMappingParams | None = None,
    ) -> list[NATPortMapping]:
        return await super()._get_multi(params=params)


class PortMappingControllerUI(BaseUIController, PortMappingControllerBase):
    async def get_object(self, *args, **kwargs) -> NATPortMapping:
        raise NotImplementedError

    async def get_objects(self, *args, **kwargs) -> list[NATPortMapping]:
        raise NotImplementedError
