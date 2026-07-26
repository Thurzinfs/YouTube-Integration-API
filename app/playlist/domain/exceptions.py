from core.exceptions import BaseDomainException


class PlaylistNotFoundException(BaseDomainException):
    pass


class ConflictFieldException(BaseDomainException):
    pass


class FieldRequiredPlaylistException(BaseDomainException):
    pass


class PlaylistIsDeletedException(BaseDomainException):
    pass


class TrackNotFoundException(BaseDomainException):
    pass


class PlaylisTrackAlreadyExistsException(BaseDomainException):
    pass


class PlaylistTrackNotFoundException(BaseDomainException):
    pass
