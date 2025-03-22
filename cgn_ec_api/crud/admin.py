from sqlmodel import Session, text, select

from cgn_ec_api.crud.base import CRUDBase
from cgn_ec_api.models import HyperTableChunk, HyperTableCompressionStats


class CRUDAdmin(CRUDBase[None, None, None]):
    async def check_hypertable_exist(self, db: Session, hypertable: str) -> bool:
        query = text(
            "SELECT EXISTS (SELECT 1 FROM timescaledb_information.hypertables WHERE hypertable_name = :hypertable_name)"
        )
        result = await db.exec(query, params={"hypertable_name": hypertable})
        return result.scalar()

    async def get_hypertable_chunks(
        self, db: Session, hypertable: str
    ) -> list[HyperTableChunk]:
        query = select(HyperTableChunk).where(
            HyperTableChunk.hypertable_name == hypertable
        )
        results = await db.exec(query)

        return results.all()

    async def get_hypertable_chunks_stats(
        self, db: Session, hypertable: str, limit: int = 100
    ) -> list[HyperTableCompressionStats]:
        query = text(
            "SELECT * FROM chunk_compression_stats(:hypertable) ORDER BY chunk_name LIMIT (:limit)"
        )

        result = await db.exec(query, params={"hypertable": hypertable, "limit": limit})
        rows = result.mappings().all()
        return [HyperTableCompressionStats(**stat) for stat in rows]

    async def get_hypertable_size(self, db: Session, hypertable: str) -> int:
        query = text("SELECT * FROM hypertable_size(:hypertable)")

        result = await db.exec(query, params={"hypertable": hypertable})
        test = result.one_or_none()
        if not test:
            return None

        return test[0]


admin = CRUDAdmin(None)
