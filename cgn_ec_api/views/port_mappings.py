from typing import Annotated

from fastapi import APIRouter, Depends
from cgn_ec_models.sqlmodel import NATPortMapping

from cgn_ec_api.dependencies.database import DatabaseDep
from cgn_ec_api.crud import port_mapping as crud
from cgn_ec_api.dependencies.redis import RedisServiceDep
from cgn_ec_api.models.query import PortMappingParams as QueryParams
from cgn_ec_api.controllers.port_mapping import PortMappingControllerAPI

router = APIRouter()


@router.get("/", response_model=list[NATPortMapping])
async def get_port_mappings(
    db: DatabaseDep, redis: RedisServiceDep, q: Annotated[QueryParams, Depends()] = None
):
    controller = PortMappingControllerAPI(db=db, redis=redis, crud=crud)
    return await controller.get_objects(params=q)
