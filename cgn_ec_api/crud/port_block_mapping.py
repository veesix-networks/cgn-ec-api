from cgn_ec_api.models.metrics import NATPortBlockMapping

from cgn_ec_api.crud.base import CRUDBase


class CRUDPortBlockMapping(CRUDBase[NATPortBlockMapping, None, None]):
    pass


port_block_mapping = CRUDPortBlockMapping(NATPortBlockMapping)
