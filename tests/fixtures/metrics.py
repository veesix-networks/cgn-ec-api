import pytest

from cgn_ec_api.models.metrics import (
    NATSessionMapping,
    NATAddressMapping,
    NATPortMapping,
    NATPortBlockMapping,
)
from tests import generate_test_data


@pytest.fixture(scope="session", autouse=True)
def generate_session_mapping_metrics(amount: int = 1000):
    metrics = []
    for _ in range(amount):
        metric = NATSessionMapping(
            timestamp=generate_test_data.random_timestamp_past_month(),
            host=generate_test_data.random_x_ip(),
            event=generate_test_data.random_session_event_type(),
            protocol=generate_test_data.random_protocol(),
            src_ip=generate_test_data.random_src_ip(),
            src_port=generate_test_data.random_src_port(),
            x_ip=generate_test_data.random_x_ip(),
            x_port=generate_test_data.random_src_port(),
            dst_ip=generate_test_data.random_dst_ip(),
            dst_port=generate_test_data.random_dst_port(),
        )
        metrics.append(metric)
    return metrics


@pytest.fixture(scope="session", autouse=True)
def generate_address_mapping_metrics(amount: int = 1000):
    metrics = []
    for _ in range(amount):
        metric = NATAddressMapping(
            timestamp=generate_test_data.random_timestamp_past_month(),
            host=generate_test_data.random_x_ip(),
            event=generate_test_data.random_session_event_type(),
            src_ip=generate_test_data.random_src_ip(),
            x_ip=generate_test_data.random_x_ip(),
        )
        metrics.append(metric)
    return metrics


@pytest.fixture(scope="session", autouse=True)
def generate_port_mapping_metrics(amount: int = 1000):
    metrics = []
    for _ in range(amount):
        metric = NATPortMapping(
            timestamp=generate_test_data.random_timestamp_past_month(),
            host=generate_test_data.random_x_ip(),
            event=generate_test_data.random_session_event_type(),
            protocol=generate_test_data.random_protocol(),
            src_ip=generate_test_data.random_src_ip(),
            src_port=generate_test_data.random_src_port(),
            x_ip=generate_test_data.random_x_ip(),
            x_port=generate_test_data.random_src_port(),
        )
        metrics.append(metric)
    return metrics


@pytest.fixture(scope="session", autouse=True)
def generate_port_block_mapping_metrics(amount: int = 1000):
    metrics = []
    for _ in range(amount):
        start_port = generate_test_data.random_src_port()
        if (start_port + 100) >= 65535:
            start_port -= 100

        metric = NATPortBlockMapping(
            timestamp=generate_test_data.random_timestamp_past_month(),
            host=generate_test_data.random_x_ip(),
            event=generate_test_data.random_session_event_type(),
            src_ip=generate_test_data.random_src_ip(),
            x_ip=generate_test_data.random_x_ip(),
            start_port=start_port,
            end_port=start_port + 100,
        )
        metrics.append(metric)
    return metrics
