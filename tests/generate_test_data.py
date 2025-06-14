import ipaddress
import secrets
from datetime import datetime, timedelta

TCP = 6
UDP = 17


def random_ip_in_subnet(subnet: str) -> str:
    network = ipaddress.IPv4Network(subnet)
    random_ip_int = (
        secrets.randbelow(network.num_addresses - 2) + 1
    )  # Exclude .0 and .255
    random_ip = network.network_address + random_ip_int
    return str(random_ip)


def random_src_ip() -> str:
    """Random IP in 100.64.0.0/10 (CGNAT space)."""
    return random_ip_in_subnet("100.64.0.0/10")


def random_x_ip() -> str:
    """Random IP in 10.0.0.0/8 (Private LAN)."""
    return random_ip_in_subnet("10.0.0.0/8")


def random_x_port() -> int:
    """Random port (>1024 to 65535)."""
    return secrets.randbelow(65535 - 1024) + 1024


def random_dst_ip() -> str:
    """Random IP in 192.0.2.0/24 (TEST-NET-1 reserved for documentation)."""
    return random_ip_in_subnet("192.0.2.0/24")


def random_src_port() -> int:
    """Random source port (>1024 to 65535)."""
    return secrets.randbelow(65535 - 1024) + 1024


def random_dst_port() -> int:
    """Random destination port (>1024 to 65535)."""
    return secrets.randbelow(65535 - 1024) + 1024


def random_protocol() -> int:
    """Randomly pick TCP or UDP."""
    return secrets.choice([TCP, UDP])


def random_timestamp_past_month() -> int:
    """Generate a random timestamps between now an an hour ago"""
    now = datetime.now()
    hour_ago = now - timedelta(hours=1)
    random_seconds = secrets.randbelow(int((now - hour_ago).total_seconds()))
    random_time = hour_ago + timedelta(seconds=random_seconds)
    return random_time


def random_session_event_type() -> str:
    return secrets.choice([1, 2])


def random_nfware_event() -> str:
    return secrets.choice(["A", "D"])


def random_nfware_direction() -> str:
    return secrets.choice(["IN", "OUT"])
