from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status
from cgn_ec_api.models.generic import NATSessionMappingRead

from cgn_ec_api.dependencies.database import DatabaseDep

router = APIRouter()


@router.get("/", response_model=list[NATSessionMappingRead])
async def get_deterministic_nat_mapping(
    db: DatabaseDep,
    x_ip: str = None,
    x_port: int = None,
    timestamp_gt: datetime = None,
    timestamp_lt: datetime = datetime.now(tz=timezone.utc),
    limit: int = 100,
    skip: int = 0,
):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Not currently implemented."
    )
