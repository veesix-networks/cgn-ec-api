from datetime import datetime

from sqlmodel import SQLModel, Field


class HyperTableCompressionStats(SQLModel):
    chunk_schema: str
    chunk_name: str
    compression_status: str
    before_compression_table_bytes: int
    before_compression_index_bytes: int
    before_compression_toast_bytes: int
    before_compression_total_bytes: int
    after_compression_table_bytes: int
    after_compression_index_bytes: int
    after_compression_toast_bytes: int
    after_compression_total_bytes: int
    node_name: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "chunk_schema": "_timescaledb_internal",
                "chunk_name": "_hyper_1_1_chunk",
                "compression_status": "Compressed",
                "before_compression_table_bytes": 8192,
                "before_compression_index_bytes": 16384,
                "before_compression_toast_bytes": 8192,
                "before_compression_total_bytes": 32768,
                "after_compression_table_bytes": 16384,
                "after_compression_index_bytes": 16384,
                "after_compression_toast_bytes": 8192,
                "after_compression_total_bytes": 40960,
                "node_name": None,
            }
        }


class HyperTableChunk(SQLModel, table=True):
    __tablename__ = "timescaledb_information.chunks"
    __table_args__ = {"quote": False}

    hypertable_schema: str = Field(primary_key=True)
    hypertable_name: str = Field(primary_key=True)
    chunk_schema: str
    chunk_name: str = Field(primary_key=True)
    primary_dimension: str
    primary_dimension_type: str
    range_start: datetime
    range_end: datetime
    range_start_integer: int | None = None
    range_end_integer: int | None = None
    is_compressed: bool
    chunk_tablespace: str | None = None
    chunk_creation_time: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "primary_dimension_type": "timestamp with time zone",
                "range_end": "2025-03-20T08:00:00Z",
                "range_end_integer": None,
                "chunk_tablespace": None,
                "chunk_schema": "_timescaledb_internal",
                "hypertable_name": "session_mapping",
                "hypertable_schema": "public",
                "chunk_name": "_hyper_1_3_chunk",
                "primary_dimension": "timestamp",
                "range_start": "2025-03-20T07:00:00Z",
                "range_start_integer": None,
                "is_compressed": True,
                "chunk_creation_time": "2025-03-20T07:22:54.684684Z",
            }
        }
