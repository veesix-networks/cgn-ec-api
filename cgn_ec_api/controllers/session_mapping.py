from datetime import datetime, timezone, timedelta

from cgn_ec_api.models.enums import NATEventEnum
from cgn_ec_api.models.generic import NATSessionMappingRead

from cgn_ec_api.config import settings
from cgn_ec_api.controllers.base import (
    BaseController,
    BaseUIController,
    BaseAPIController,
)
from cgn_ec_api.models.query import SessionMappingParams
from cgn_ec_api.crud.session_mapping import CRUDSessionMapping
from cgn_ec_api import exceptions


class SessionMappingControllerBase(BaseController):
    CRUDController = CRUDSessionMapping

    async def _get(self, src_ip: str) -> NATSessionMappingRead:
        """
        Get a Session Mapping by src_ip, with caching.

        Args:
            src_ip: The src_ip of the record.
            cache_timeout: Cache expiration time in seconds (default: 1 hour).

        Returns:
            NATSessionMapping object
        """
        record = await self.cache_get(
            cache_key=src_ip,
            fetch_data_func=self.crud.get,
            db=self.db,
            src_ip=src_ip,
        )

        if not record:
            raise exceptions.CGNECNATSessionMappingNotFoundError

        return NATSessionMappingRead.model_validate(record)

    async def _get_multi(
        self,
        params: SessionMappingParams | None = None,
    ) -> list[NATSessionMappingRead]:
        if not params.timestamp_ge:
            current_time_utc = datetime.now(tz=timezone.utc)
            timestamp_ge = current_time_utc - timedelta(
                hours=settings.DEFAULT_LOOKBACK_HOURS
            )
            params.timestamp_ge = timestamp_ge

        records = [
            NATSessionMappingRead.model_validate(record)
            for record in await self.crud.get_multi(self.db, params=params)
        ]
        if params.hook:
            for record in records:
                self.process_hook(params.hook, NATEventEnum.SESSION_MAPPING, record)

        return records


class SessionMappingControllerAPI(BaseAPIController, SessionMappingControllerBase):
    async def get_object(self, src_ip: str) -> NATSessionMappingRead:
        try:
            return await super()._get(src_ip=src_ip)
        except exceptions.CGNECBaseException as e:
            raise e.http()

    async def get_objects(
        self,
        params: SessionMappingParams | None = None,
    ) -> list[NATSessionMappingRead]:
        try:
            return await super()._get_multi(params=params)
        except exceptions.CGNECBaseException as e:
            raise e.http()


class SessionMappingControllerUI(BaseUIController, SessionMappingControllerBase):
    async def get_object(self, *args, **kwargs) -> NATSessionMappingRead:
        raise NotImplementedError

    async def get_objects(self, *args, **kwargs) -> list[NATSessionMappingRead]:
        raise NotImplementedError
