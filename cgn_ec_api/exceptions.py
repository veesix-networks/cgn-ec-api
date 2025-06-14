from abc import ABC, abstractmethod
from fastapi import HTTPException, status


class CGNECBaseException(ABC, Exception):
    @abstractmethod
    def http(self) -> HTTPException: ...


class CGNECHookNotFoundError(CGNECBaseException):
    def __init__(self, hook_name: str):
        self.hook_name = hook_name
        self.message = f"Hook '{hook_name}' not found."
        super().__init__(self.message)

    def http(self) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=self.message
        )


class CGNECHookError(CGNECBaseException):
    def __init__(self, hook_name: str):
        self.hook_name = hook_name
        self.message = f"Hook '{hook_name}' is not configured properly. Please reference cgn-ec documentation on how to properly write a hook."
        super().__init__(self.message)

    def http(self) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=self.message
        )


class CGNECHookException(CGNECBaseException):
    def __init__(self, hook_name: str, exception: str):
        self.hook_name = hook_name
        self.exception = exception
        self.message = f"Hook '{hook_name}' encountered an exception: {exception}"
        super().__init__(self.message)

    def http(self) -> HTTPException:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=self.message)


class CGNECNATSessionMappingNotFoundError(CGNECBaseException):
    def __init__(self):
        self.message = "NAT Session Mapping not found."
        super().__init__(self.message)

    def http(self) -> HTTPException:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=self.message)


class CGNECNATAddressMappingNotFoundError(CGNECBaseException):
    def __init__(self):
        self.message = "NAT Address Mapping not found."
        super().__init__(self.message)

    def http(self) -> HTTPException:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=self.message)


class CGNECNATPortMappingNotFoundError(CGNECBaseException):
    def __init__(self):
        self.message = "NAT Port Mapping not found."
        super().__init__(self.message)

    def http(self) -> HTTPException:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=self.message)


class CGNECNATPortBlockMappingNotFoundError(CGNECBaseException):
    def __init__(self):
        self.message = "NAT Port Block Mapping not found."
        super().__init__(self.message)

    def http(self) -> HTTPException:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=self.message)


class CGNECInvalidOrderByFieldError(CGNECBaseException):
    def __init__(self, field_name: str):
        self.field_name = field_name
        self.message = f"Invalid order_by field: '{field_name}'"
        super().__init__(self.message)

    def http(self) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=self.message
        )
