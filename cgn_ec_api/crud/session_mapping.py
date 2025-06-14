from cgn_ec_api.models.metrics import NATSessionMapping

from cgn_ec_api.crud.base import CRUDBase


class CRUDSessionMapping(CRUDBase[NATSessionMapping, None, None]):
    pass


session_mapping = CRUDSessionMapping(NATSessionMapping)
