from typing import Literal
from urllib.parse import urlparse as parse_url, ParseResult

from django.conf import settings


def get_domain_and_url(url_type: Literal['FRONTEND_URL', 'BACKEND_URL']) -> ParseResult:
    if hasattr(settings, url_type) and settings.FRONTEND_URL:
        url_string = settings.FRONTEND_URL
    else:
        url_string = 'http://localhost'
    parsed_url = parse_url(url_string)
    return parsed_url


PARSED_FRONTEND_RESULT = get_domain_and_url('FRONTEND_URL')
PARSED_BACKEND_RESULT = get_domain_and_url('BACKEND_URL')
FRONTEND_URL = PARSED_FRONTEND_RESULT.geturl()
BACKEND_URL = PARSED_BACKEND_RESULT.geturl()
