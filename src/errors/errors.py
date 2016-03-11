from utils.exceptions import ErrorKeyDoesntExistError
from .artist import _response_errors as _artist_response_errors

_response_errors = {
    "NOT_LOGGED": "You need to login",
    "WRONG_EMAIL": "Wrong email or password",
    "EMAIL_ALREADY_REGISTERED": "This email is already registered",
    "NOT_AN_EMAIL": "Not an email",
    "CANT_BE_EMPTY": "Can't be empty"
}

# include artist response errors
_response_errors.update(_artist_response_errors)


def get_response_error(error_key):
    if error_key not in _response_errors:
        raise ErrorKeyDoesntExistError("The error_key {0} doesn't exist".format(error_key))

    return {
        "code": error_key,
        "message": _response_errors[error_key]
    }
