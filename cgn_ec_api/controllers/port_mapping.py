from datetime import datetime, timezone, timedelta

from cgn_ec_models.enums import NATEventEnum
from cgn_ec_api.models.generic import NATPortMappingRead

from cgn_ec_api.config import settings
from cgn_ec_api.controllers.base import (
    BaseController,
    BaseUIController,
    BaseAPIController,
)
from cgn_ec_api.models.query import PortMappingParams
from cgn_ec_api.crud.port_mapping import CRUDPortMapping
from cgn_ec_api import exceptions


class PortMappingControllerBase(BaseController):
    CRUDController = CRUDPortMapping

    async def _get(self, src_ip: str) -> NATPortMappingRead:
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
            raise exceptions.CGNECNATPortMappingNotFoundError

        return NATPortMappingRead.model_validate(record)

    async def _get_multi(
        self,
        params: PortMappingParams | None = None,
    ) -> list[NATPortMappingRead]:
        if not params.timestamp_ge:
            current_time_utc = datetime.now(tz=timezone.utc)
            timestamp_ge = current_time_utc - timedelta(
                hours=settings.DEFAULT_LOOKBACK_HOURS
            )
            params.timestamp_ge = timestamp_ge

        records = [
            NATPortMappingRead.model_validate(record)
            for record in await self.crud.get_multi(self.db, params=params)
        ]
        if params.hook:
            for record in records:
                self.process_hook(params.hook, NATEventEnum.PORT_MAPPING, record)

        return records


class PortMappingControllerAPI(BaseAPIController, PortMappingControllerBase):
    async def get_object(self, src_ip: str) -> NATPortMappingRead:
        return await super()._get(src_ip=src_ip)

    async def get_objects(
        self,
        params: PortMappingParams | None = None,
    ) -> list[NATPortMappingRead]:
        return await super()._get_multi(params=params)


class PortMappingControllerUI(BaseUIController, PortMappingControllerBase):
    async def get_object(self, *args, **kwargs) -> NATPortMappingRead:
        raise NotImplementedError

    async def get_objects(self, *args, **kwargs) -> list[NATPortMappingRead]:
        raise NotImplementedError
