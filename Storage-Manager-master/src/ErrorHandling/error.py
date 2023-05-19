"""Code written by Jacquesne Jones unless otherwise specified."""


class Error(Exception):
    """Simple error handling, if an exception is thrown the output will indicate the issue."""
    pass


class NoWindowObject(Error):
    pass


class DuplicateAlternateInfo(Error):
    pass


class NoDatabaseLoaded(Error):
    pass


class BadDataTypePassed(Error):
    pass
