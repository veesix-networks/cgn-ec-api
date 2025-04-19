from abc import ABC, abstractmethod
from typing import TypeVar, Callable, Awaitable

from cgn_ec_api.config import settings
from cgn_ec_api.dependencies.database import DatabaseDep
from cgn_ec_api.dependencies.redis import RedisServiceDep
from cgn_ec_api.crud.base import CRUDBase

from structlog import get_logger

logger = get_logger("cgn_ec_api.controllers.base")


T = TypeVar("T")


class BaseController(ABC):
    CRUDController = CRUDBase

    def __init__(self, db: DatabaseDep, redis: RedisServiceDep, crud: CRUDController):
        self.db = db
        self.redis = redis
        self.crud = crud

    @abstractmethod
    def get_object():
        pass

    @abstractmethod
    def get_objects():
        pass

    async def cache_get(
        self,
        cache_key: str,
        fetch_data_func: Callable[..., Awaitable[T]],
        timeout: int = settings.CACHE_EXPIRE,
        **kwargs,
    ) -> T:
        """
        Generic method to get data from cache or fetch it if not cached.

        Args:
            cache_key: The key to use for caching
            fetch_data_func: Async function to call if data not in cache
            timeout: Cache expiration time in seconds (default: 1 hour)
            **kwargs: Arguments to pass to the fetch_data_func

        Returns:
            The cached or freshly fetched data
        """
        cached_data = await self.redis.get(cache_key)
        if cached_data:
            logger.debug("Cache hit", cache_key=cache_key)
            return self.crud.model.model_validate_json(cached_data)

        logger.debug("Cache miss", cache_key=cache_key)
        data = await fetch_data_func(**kwargs)

        if not data:
            return None

        await self.redis.set(cache_key, data.model_dump_json(), timeout=timeout)
        return data


class BaseUIController(BaseController):
    pass


class BaseAPIController(BaseController):
    pass
