from __future__ import annotations

import requests
import www_authenticate


def get_restricted_realm(url: str) -> str | None:
    """A very simple function to get the realm for restricted access

    This will only work, if the server returns a 'www-authenticate'-
    header, and if the authentication method is 'basic'
    """

    r = requests.get(url)

    auth_header_name = 'WWW-Authenticate'
    auth_header = r.headers.get(auth_header_name, None)
    if auth_header:
        parsed = www_authenticate.parse(auth_header)
        if 'Basic' in parsed:
            return parsed['Basic']['realm']
    return None
