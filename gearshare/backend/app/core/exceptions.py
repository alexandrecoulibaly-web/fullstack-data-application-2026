class BusinessError(Exception):
    """Base exception for errors raised by the domain layer."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class ResourceNotFound(BusinessError):
    """Raised when a requested resource does not exist."""


class BusinessConflict(BusinessError):
    """Raised when a business rule prevents an operation."""


class AccessDenied(BusinessError):
    """Raised when a caller cannot access a resource."""