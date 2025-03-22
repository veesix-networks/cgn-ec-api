from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from cgn_ec_api.dependencies import DatabaseDep
from cgn_ec_api import crud
from cgn_ec_api.models import HyperTableChunk, HyperTableCompressionStats

router = APIRouter()


@router.get("/hypertable/{hyper_table}/chunks", response_model=list[HyperTableChunk])
async def get_hyper_table_chunks(db: DatabaseDep, hyper_table: str):
    hypertable_exist = await crud.admin.check_hypertable_exist(db, hyper_table)
    if not hypertable_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No hypertable named '{hyper_table}'.",
        )

    chunks = await crud.admin.get_hypertable_chunks(db, hyper_table)
    return chunks


@router.get(
    "/hypertable/{hyper_table}/chunks_stats",
    response_model=list[HyperTableCompressionStats],
)
async def get_hyper_table_chunks_stats(db: DatabaseDep, hyper_table: str):
    hypertable_exist = await crud.admin.check_hypertable_exist(db, hyper_table)
    if not hypertable_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No hypertable named '{hyper_table}'.",
        )

    chunks = await crud.admin.get_hypertable_chunks_stats(db, hyper_table)
    return chunks


@router.get("/hypertable/{hyper_table}/size", response_model=int)
async def get_hyper_table_size(db: DatabaseDep, hyper_table: str):
    hypertable_exist = await crud.admin.check_hypertable_exist(db, hyper_table)
    if not hypertable_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No hypertable named '{hyper_table}'.",
        )

    chunks = await crud.admin.get_hypertable_size(db, hyper_table)
    return chunks
