from __future__ import annotations

import requests


def get_restricted_realm(url: str) -> str | None:
    """A very simple function to get the realm for restricted access

    This will only work, if the server returns a 'www-authenticate'-
    header, and if the authentication method is 'basic'
    """

    auth_header_name = 'www-authenticate'

    r = requests.get(url)
    if auth_header_name not in r.headers:
        return None

    words = r.headers[auth_header_name].split()
    if words[0].lower() != 'basic':
        return None

    if words[1].startswith('realm="'):
        return words[1][7:-1]
