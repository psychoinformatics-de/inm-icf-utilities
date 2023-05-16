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


@pytest.fixture(autouse=False, scope='session')
def dicom_server(dataaccess_credential):
    if os.environ.get('APPVEYOR', None) == 'true':
        yield dict(
            base_url='http://localhost/~appveyor',
            studies=os.environ['STUDIES'].split(),
        )
    else:
        study_dir = os.environ.get(local_eny_key, None)
        if not study_dir:
            raise ValueError(
                'Cannot execute tests locally, because the environment '
                f'variable ``{local_eny_key}´´ is not defined. Set the '
                f'environment variable ``{local_eny_key}´´ in a startup '
                f'script, e.g. ~/.bashrc, to point to a local directory that '
                f'contains study data, as defined in RFD0034.')
        server = HTTPPath(
            study_dir,
            auth=(dataaccess_credential['user'],
                  dataaccess_credential['secret'])
        )
        with server:
            yield dict(
                base_url=server.url,
                studies=[],
            )
