from core.exceptions import BaseDomainException


class PlaylistNotFoundException(BaseDomainException):
    pass


class ConflictFieldException(BaseDomainException):
    pass


class FieldRequiredPlaylistException(BaseDomainException):
    pass
