from cgn_ec_models.sqlmodel import NATAddressMapping

from cgn_ec_api.crud.base import CRUDBase


class CRUDAddressMapping(CRUDBase[NATAddressMapping, None, None]):
    pass


address_mapping = CRUDAddressMapping(NATAddressMapping)
