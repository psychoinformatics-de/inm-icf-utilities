from __future__ import annotations
from pathlib import Path

import pytest

from datalad.api import (
    credentials,
    download,
)
from datalad.support.exceptions import IncompleteResultsError


protocol = 'http'


def _check_results(results: list[dict]):
    assert all(result['status'] == 'ok' for result in results)


def test_example_unauthorized():
    with pytest.raises(IncompleteResultsError):
        download(
            f'{protocol}://localhost/~appveyor/study_1/visit_1_dicom.tar')


def test_example_authorized(tmp_path: Path):
    results = credentials(
        'set',
        name='test_cred',
        spec={
            'type': 'user_password',
            'user': 'test.user',
            'password': 'secret_1'})
    _check_results(results)

    results = download(
        f'{protocol}://localhost/~appveyor/study_1/visit_1_dicom.tar',
        credential='test_cred')
    _check_results(results)

    elements = tuple(tmp_path.iterdir())
    print(elements)
    assert 'visit_1_dicom.tar' in elements
    assert 'visit_1_dicom.tar.md5sum' in elements
