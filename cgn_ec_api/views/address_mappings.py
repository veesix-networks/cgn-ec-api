from typing import Annotated

from fastapi import APIRouter, Depends
from cgn_ec_models.sqlmodel import NATAddressMapping

from cgn_ec_api.dependencies.database import DatabaseDep
from cgn_ec_api.crud import address_mapping as crud
from cgn_ec_api.dependencies.redis import RedisServiceDep
from cgn_ec_api.models.query import AddressMappingParams as QueryParams
from cgn_ec_api.controllers.address_mapping import AddressMappingControllerAPI

router = APIRouter()


@router.get("/", response_model=list[NATAddressMapping])
async def get_address_mappings(
    db: DatabaseDep, redis: RedisServiceDep, q: Annotated[QueryParams, Depends()] = None
):
    controller = AddressMappingControllerAPI(db=db, redis=redis, crud=crud)
    return await controller.get_objects(params=q)
