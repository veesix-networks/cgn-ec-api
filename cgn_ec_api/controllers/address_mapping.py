from datetime import datetime, timezone, timedelta

from cgn_ec_api.models.enums import NATEventEnum
from cgn_ec_api.models.generic import NATAddressMappingRead

from cgn_ec_api.config import settings
from cgn_ec_api.controllers.base import (
    BaseController,
    BaseUIController,
    BaseAPIController,
)
from cgn_ec_api.models.query import AddressMappingParams
from cgn_ec_api.crud.address_mapping import CRUDAddressMapping
from cgn_ec_api import exceptions


class AddressMappingControllerBase(BaseController):
    CRUDController = CRUDAddressMapping

    async def _get(self, src_ip: str) -> NATAddressMappingRead:
        """
        Get a Address Mapping record by src_ip, with caching.

        Args:
            src_ip: The src_ip of the record.
            cache_timeout: Cache expiration time in seconds (default: 1 hour).

        Returns:
            NATAddressMapping object
        """
        record = await self.cache_get(
            cache_key=src_ip,
            fetch_data_func=self.crud.get,
            db=self.db,
            src_ip=src_ip,
        )

        if not record:
            raise exceptions.CGNECNATAddressMappingNotFoundError

        return NATAddressMappingRead.model_validate(record)

    async def _get_multi(
        self,
        params: AddressMappingParams | None = None,
    ) -> list[NATAddressMappingRead]:
        if not params.timestamp_ge:
            current_time_utc = datetime.now(tz=timezone.utc)
            timestamp_ge = current_time_utc - timedelta(
                hours=settings.DEFAULT_LOOKBACK_HOURS
            )
            params.timestamp_ge = timestamp_ge

        records = [
            NATAddressMappingRead.model_validate(record)
            for record in await self.crud.get_multi(self.db, params=params)
        ]
        if params.hook:
            for record in records:
                self.process_hook(params.hook, NATEventEnum.ADDRESS_MAPPING, record)

        return records


class AddressMappingControllerAPI(BaseAPIController, AddressMappingControllerBase):
    async def get_object(self, src_ip: str) -> NATAddressMappingRead:
        return await super()._get(src_ip=src_ip)

    async def get_objects(
        self,
        params: AddressMappingParams | None = None,
    ) -> list[NATAddressMappingRead]:
        return await super()._get_multi(params=params)


class AddressMappingControllerUI(BaseUIController, AddressMappingControllerBase):
    async def get_object(self, *args, **kwargs) -> NATAddressMappingRead:
        raise NotImplementedError

    async def get_objects(self, *args, **kwargs) -> list[NATAddressMappingRead]:
        raise NotImplementedError
