from core.exceptions import BaseDomainException


class NotFoundMediaSourceException(BaseDomainException):
    ...


class ConflictMediaSourceFieldException(BaseDomainException):
    ...


class FieldMediaSourceRequiredException(BaseDomainException):
    ...


class FailedDownloadMusicException(BaseDomainException):
    pass
