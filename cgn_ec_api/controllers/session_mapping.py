from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status

from cgn_ec_models.sqlmodel import NATSessionMapping

from cgn_ec_api.config import settings
from cgn_ec_api.controllers.base import (
    BaseController,
    BaseUIController,
    BaseAPIController,
)
from cgn_ec_api.models.query import SessionMappingParams
from cgn_ec_api.crud.session_mapping import CRUDSessionMapping


class SessionMappingControllerBase(BaseController):
    CRUDController = CRUDSessionMapping

    async def _get(self, src_ip: str) -> NATSessionMapping:
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
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, detail="NAT Session Mapping not found."
            )

        return record

    async def _get_multi(
        self,
        params: SessionMappingParams | None = None,
    ) -> list[NATSessionMapping]:
        if not params.timestamp_ge:
            current_time_utc = datetime.now(tz=timezone.utc)
            timestamp_ge = current_time_utc - timedelta(
                hours=settings.DEFAULT_LOOKBACK_HOURS
            )
            params.timestamp_ge = timestamp_ge

        records = await self.crud.get_multi(self.db, params=params)

        return records


class SessionMappingControllerAPI(BaseAPIController, SessionMappingControllerBase):
    async def get_object(self, src_ip: str) -> NATSessionMapping:
        return await super()._get(src_ip=src_ip)

    async def get_objects(
        self,
        params: SessionMappingParams | None = None,
    ) -> list[NATSessionMapping]:
        return await super()._get_multi(params=params)


class SessionMappingControllerUI(BaseUIController, SessionMappingControllerBase):
    async def get_object(self, *args, **kwargs) -> NATSessionMapping:
        raise NotImplementedError

    async def get_objects(self, *args, **kwargs) -> list[NATSessionMapping]:
        raise NotImplementedError
