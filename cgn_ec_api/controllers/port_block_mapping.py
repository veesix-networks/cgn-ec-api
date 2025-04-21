from datetime import datetime, timezone, timedelta

from cgn_ec_models.enums import NATEventEnum
from cgn_ec_api.models.generic import NATPortBlockMappingRead

from cgn_ec_api.config import settings
from cgn_ec_api.controllers.base import (
    BaseController,
    BaseUIController,
    BaseAPIController,
)
from cgn_ec_api.models.query import PortBlockMappingParams
from cgn_ec_api.crud.port_block_mapping import CRUDPortBlockMapping
from cgn_ec_api import exceptions


class PortBlockMappingControllerBase(BaseController):
    CRUDController = CRUDPortBlockMapping

    async def _get(self, x_ip: str) -> NATPortBlockMappingRead:
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
            raise exceptions.CGNECNATPortBlockMappingNotFoundError

        return NATPortBlockMappingRead.model_validate(record)

    async def _get_multi(
        self,
        params: PortBlockMappingParams | None = None,
    ) -> list[NATPortBlockMappingRead]:
        if not params.timestamp_ge:
            current_time_utc = datetime.now(tz=timezone.utc)
            timestamp_ge = current_time_utc - timedelta(
                hours=settings.DEFAULT_LOOKBACK_HOURS
            )
            params.timestamp_ge = timestamp_ge

        records = [
            NATPortBlockMappingRead.model_validate(record)
            for record in await self.crud.get_multi(self.db, params=params)
        ]
        if params.hook:
            for record in records:
                self.process_hook(params.hook, NATEventEnum.PORT_BLOCK_MAPPING, record)

        return records


class PortBlockMappingControllerAPI(BaseAPIController, PortBlockMappingControllerBase):
    async def get_object(self, src_ip: str) -> NATPortBlockMappingRead:
        return await super()._get(src_ip=src_ip)

    async def get_objects(
        self,
        params: PortBlockMappingParams | None = None,
    ) -> list[NATPortBlockMappingRead]:
        return await super()._get_multi(params=params)


class PortBlockMappingControllerUI(BaseUIController, PortBlockMappingControllerBase):
    async def get_object(self, *args, **kwargs) -> NATPortBlockMappingRead:
        raise NotImplementedError

    async def get_objects(self, *args, **kwargs) -> list[NATPortBlockMappingRead]:
        raise NotImplementedError
