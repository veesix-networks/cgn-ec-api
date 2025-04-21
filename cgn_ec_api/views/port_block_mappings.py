from typing import Annotated

from fastapi import APIRouter, Depends

from cgn_ec_api.dependencies.database import DatabaseDep
from cgn_ec_api.crud import port_block_mapping as crud
from cgn_ec_api.dependencies.redis import RedisServiceDep
from cgn_ec_api.models.generic import NATPortBlockMappingRead
from cgn_ec_api.models.query import PortBlockMappingParams as QueryParams
from cgn_ec_api.controllers.port_block_mapping import PortBlockMappingControllerAPI

router = APIRouter()


@router.get("/", response_model=list[NATPortBlockMappingRead])
async def get_port_block_mappings(
    db: DatabaseDep, redis: RedisServiceDep, q: Annotated[QueryParams, Depends()] = None
):
    controller = PortBlockMappingControllerAPI(db=db, redis=redis, crud=crud)
    return await controller.get_objects(params=q)
