from __future__ import annotations

from datalad_next.url_operations.http import HttpUrlOperations


def get_restricted_realm(url: str) -> str | None:
    """Get the realm for basic auth-restricted access

    Parameters
    ----------
    url: str
      URL to probe

    Returns
    -------
    str | None
      The name of the realm for basic authentication
      or None, if either no authentication is required,
      or if the authentication type is not "basic"
    """

    http_url_ops = HttpUrlOperations()
    _, url_properties = http_url_ops.probe_url(url)
    return url_properties.get('auth', {}).get('basic', {}).get('realm')
