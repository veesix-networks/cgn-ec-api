from cgn_ec_api.models.generic import (
    NATSessionMappingRead,
    NATAddressMappingRead,
    NATPortMappingRead,
    NATPortBlockMappingRead,
    HookMetadata,
)
import secrets
import uuid


def session_mapping_hook(event: NATSessionMappingRead) -> NATSessionMappingRead:
    event.hook_metadata = HookMetadata(
        data={
            "subscriber": generate_random_subscriber_data(),
        }
    )


def address_mapping_hook(event: NATAddressMappingRead) -> NATAddressMappingRead:
    event.hook_metadata = HookMetadata(
        data={"subscriber": generate_random_subscriber_data()}
    )


def port_mapping_hook(event: NATPortMappingRead) -> NATPortMappingRead:
    event.hook_metadata = HookMetadata(
        data={"subscriber": generate_random_subscriber_data()}
    )


def port_block_mapping_hook(event: NATPortBlockMappingRead) -> NATPortBlockMappingRead:
    event.hook_metadata = HookMetadata(
        data={"subscriber": generate_random_subscriber_data()}
    )


def generate_random_subscriber_data() -> dict:
    return {
        "circuit_id": f"OLT-1.LT{secrets.choice(range(1, 16))}.PON{secrets.choice(range(1, 32))}.ONU{secrets.choice(range(0, 128))}.ETH.PHY.{secrets.choice(range(0, 2))}",
        "remote_id": str(uuid.uuid4()),
    }
