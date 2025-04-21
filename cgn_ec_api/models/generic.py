from pydantic import BaseModel, ConfigDict
from datetime import datetime
from ipaddress import IPv4Address


class HookMetadata(BaseModel):
    data: dict = {}
    error: str | None = None


class MetricBaseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    timestamp: datetime
    hook_metadata: HookMetadata | None = None


class NATSessionMappingRead(MetricBaseRead):
    host: IPv4Address
    event: int
    vrf_id: int | None = None
    protocol: int
    src_ip: IPv4Address
    src_port: int
    x_ip: IPv4Address
    x_port: int
    dst_ip: IPv4Address
    dst_port: int


class NATAddressMappingRead(MetricBaseRead):
    host: IPv4Address
    event: int
    vrf_id: int | None = None
    src_ip: IPv4Address
    x_ip: IPv4Address


class NATPortMappingRead(MetricBaseRead):
    host: IPv4Address
    event: int
    vrf_id: int | None = None
    protocol: int
    src_ip: IPv4Address
    src_port: int
    x_ip: IPv4Address
    x_port: int


class NATPortBlockMappingRead(MetricBaseRead):
    host: IPv4Address
    event: int
    vrf_id: int | None = None
    src_ip: IPv4Address
    x_ip: IPv4Address
    start_port: int
    end_port: int
