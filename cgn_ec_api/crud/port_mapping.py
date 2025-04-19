from cgn_ec_models.sqlmodel import NATPortMapping

from cgn_ec_api.crud.base import CRUDBase


class CRUDPortMapping(CRUDBase[NATPortMapping, None, None]):
    pass


port_mapping = CRUDPortMapping(NATPortMapping)
