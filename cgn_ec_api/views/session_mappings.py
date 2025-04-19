from typing import Annotated

from fastapi import APIRouter, Depends
from cgn_ec_models.sqlmodel import NATSessionMapping

from cgn_ec_api.dependencies.database import DatabaseDep
from cgn_ec_api.crud import session_mapping as crud
from cgn_ec_api.dependencies.redis import RedisServiceDep
from cgn_ec_api.models.query import SessionMappingParams as QueryParams
from cgn_ec_api.controllers.session_mapping import SessionMappingControllerAPI

router = APIRouter()


@router.get("/", response_model=list[NATSessionMapping])
async def get_session_mappings(
    db: DatabaseDep, redis: RedisServiceDep, q: Annotated[QueryParams, Depends()] = None
):
    controller = SessionMappingControllerAPI(db=db, redis=redis, crud=crud)
    return await controller.get_objects(params=q)
