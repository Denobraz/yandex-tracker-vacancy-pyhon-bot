import validators
from validators import ValidationError

def var_dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))

def normalize_url(url_string: str) -> str:
    if not url_string.startswith(("http://", "https://")):
        url_string = "https://" + url_string
    return url_string

def is_string_an_url(url_string: str) -> bool:
    result = validators.url(url_string)

    if isinstance(result, ValidationError):
        return False

    return result