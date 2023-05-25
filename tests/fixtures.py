from __future__ import annotations
import os

import pytest

from datalad_next.tests.utils import HTTPPath


local_eny_key = 'INM_ICF_TEST_STUDIES'


@pytest.fixture(autouse=False, scope="session")
def dataaccess_credential():
    yield dict(
        name='icf-credential',
        user='test.user',
        secret='secret_1',
        type='user_password',
    )


@pytest.fixture(autouse=False, scope="session")
def test_study_names():
    studies = []
    if os.environ.get('APPVEYOR', None) == 'true':
        studies = os.environ['STUDIES'].split()
    yield studies


@pytest.fixture(autouse=False, scope='session')
def data_webserver(dataaccess_credential):
    """Yields a URL to a webserver providing data access"""
    if os.environ.get('APPVEYOR', None) == 'true':
        yield 'http://data.inm-icf.de/~appveyor'
    else:
        study_dir = os.environ.get(local_eny_key, None)
        if not study_dir:
            raise ValueError(
                'Cannot execute tests locally, because the environment '
                f'variable ``{local_eny_key}´´ is not defined. Set the '
                f'environment variable ``{local_eny_key}´´ to point to '
                f'a local directory that contains study data, as defined '
                f'in RFD0034.')
        server = HTTPPath(
            study_dir,
            auth=(dataaccess_credential['user'],
                  dataaccess_credential['secret'])
        )
        with server:
            yield server.url
