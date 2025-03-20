from datetime import datetime, timedelta, timezone

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from cgn_ec_models.sqlmodel import NATPortBlockMapping

from cgn_ec_api.config import settings
from cgn_ec_api.dependencies import DatabaseDep
from cgn_ec_api import crud

router = APIRouter()


@router.get("/", response_model=list[NATPortBlockMapping])
async def get_port_block_mappings(
    db: DatabaseDep,
    x_ip: str = None,
    start_port: int = None,
    end_port: int = None,
    timestamp_gt: datetime = None,
    timestamp_lt: datetime = datetime.now(tz=timezone.utc),
    limit: int = 100,
    skip: int = 0,
):
    current_time_utc = datetime.now(tz=timezone.utc)

    if not timestamp_gt:
        timestamp_gt = current_time_utc - timedelta(
            hours=settings.DEFAULT_LOOKBACK_HOURS
        )

    # Validation: timestamp_lt must be less than now
    if timestamp_lt >= current_time_utc:
        raise HTTPException(
            status_code=400, detail="timestamp_lt must be less than the current time."
        )

    # Validation: timestamp_lt must be greater than timestamp_gt
    if timestamp_lt <= timestamp_gt:
        raise HTTPException(
            status_code=400, detail="timestamp_lt must be greater than timestamp_gt."
        )

    results = await crud.port_block_mapping.get_by_x_ip_and_port(
        db, timestamp_lt, timestamp_gt, x_ip, start_port, end_port, limit, skip
    )

    return results
