from pathlib import Path

import pytest

from datalad.api import (
    credentials,
    download,
)
from datalad.support.exceptions import IncompleteResultsError


protocol = 'http'


def test_example_unauthorized():
    with pytest.raises(IncompleteResultsError):
        download(
            f'{protocol}://localhost/~appveyor/study_1/visit_1_dicom.tar')


def test_example_authorized(tmp_path: Path):
    res = credentials(
        'set',
        name='test_cred',
        spec={
            'type': 'user_password',
            'user': 'test.user',
            'password': 'secret_1'})
    assert res['status'] == 'ok'

    res = download(
        f'{protocol}://localhost/~appveyor/study_1/visit_1_dicom.tar',
        credential='test_cred')
    assert res['status'] == 'ok'

    elements = tuple(tmp_path.iterdir())
    print(elements)
    assert 'visit_1_dicom.tar' in elements
    assert 'visit_1_dicom.tar.md5sum' in elements
