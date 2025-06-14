from abc import ABC, abstractmethod
import importlib.util
from typing import TypeVar, Callable, Awaitable

from cgn_ec_api.models.enums import NATEventEnum

from cgn_ec_api.config import settings
from cgn_ec_api.dependencies.database import DatabaseDep
from cgn_ec_api.dependencies.redis import RedisServiceDep
from cgn_ec_api.crud.base import CRUDBase
from cgn_ec_api.models.generic import MetricBaseRead, HookMetadata
from cgn_ec_api import exceptions

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

    def process_hook(
        self, hook: str, event_type: NATEventEnum, metric: MetricBaseRead
    ) -> None:
        try:
            if not isinstance(event_type, NATEventEnum):
                raise exceptions.CGNECHookError(hook)

            hook_file = settings.HOOKS_DIRECTORY.joinpath(f"{hook}.py")

            if not hook_file.exists():
                raise exceptions.CGNECHookNotFoundError(hook)

            spec = importlib.util.spec_from_file_location(hook, str(hook_file))
            if spec is None or spec.loader is None:
                raise exceptions.CGNECHookError(hook)

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            event_type_normalized = event_type.lower().replace("-", "_")
            module_attr = getattr(module, f"{event_type_normalized}_hook", None)

            if not module_attr:
                return

            module_attr(metric)

            # Validate we can serialize the data after user has added their fields
            metric.model_dump_json()
        except Exception as e:
            if settings.RAISE_ERROR_FROM_HOOK:
                raise exceptions.CGNECHookException(hook, e)

            metric.hook_metadata = HookMetadata(error=f"({e.__class__.__name__}) {e}")


class BaseUIController(BaseController):
    pass


class BaseAPIController(BaseController):
    pass
