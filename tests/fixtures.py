from __future__ import annotations
import os

import pytest

from datalad_next.tests.utils import HTTPPath


_studies_dir_env_key = 'INM_ICF_TEST_STUDIES'


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
    studies = ['study_1', 'study_2']
    if os.environ.get('APPVEYOR', None) == 'true':
        studies = os.environ['STUDIES'].split()
    yield studies


@pytest.fixture(autouse=False, scope='session')
def test_studies_dir():
    if os.environ.get('APPVEYOR', None) == 'true':
        yield os.environ['STUDIES_DIR']
    else:
        study_dir = os.environ.get(_studies_dir_env_key, None)
        if not study_dir:
            raise ValueError(
                'Cannot execute tests locally, because the environment '
                f'variable ``{_studies_dir_env_key}´´ is not defined. '
                f'Set the environment variable ``{_studies_dir_env_key}´´'
                f' to point to a local directory that contains study '
                f'data, as defined in RFD0034.')
        yield study_dir


@pytest.fixture(autouse=False, scope='session')
def data_webserver(test_studies_dir, dataaccess_credential):
    """Yields a URL to a webserver providing data access"""
    if os.environ.get('APPVEYOR', None) == 'true':
        yield 'http://data.inm-icf.de/~appveyor'
    else:
        server = HTTPPath(
            test_studies_dir,
            auth=(
                dataaccess_credential['user'],
                dataaccess_credential['secret']
            )
        )
        with server:
            yield server.url
