from datetime import datetime, timezone

from fastapi import APIRouter
from cgn_ec_models.sqlmodel import NATSessionMapping

from cgn_ec_api.dependencies import DatabaseDep

router = APIRouter()


@router.get("/", response_model=list[NATSessionMapping])
async def get_deterministic_nat_mapping(
    db: DatabaseDep,
    x_ip: str = None,
    x_port: int = None,
    timestamp_gt: datetime = None,
    timestamp_lt: datetime = datetime.now(tz=timezone.utc),
    limit: int = 100,
    skip: int = 0,
):
    return
