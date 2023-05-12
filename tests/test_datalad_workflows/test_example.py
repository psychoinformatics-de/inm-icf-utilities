from __future__ import annotations
from pathlib import Path

import pytest

from datalad.api import (
    credentials,
    download,
)
from datalad.support.exceptions import IncompleteResultsError
from datalad.utils import chpwd


protocol = 'http'


def _check_results(results: list[dict]):
    assert all(result['status'] == 'ok' for result in results)


def test_example_unauthorized():
    with pytest.raises(IncompleteResultsError):
        download(
            f'{protocol}://localhost/~appveyor/study_1/visit_1_dicom.tar')


def test_example_authorized(tmp_path: Path):
    with chpwd(tmp_path):
        results = download(
            f'{protocol}://localhost/~appveyor/study_1/visit_1_dicom.tar',
            credential='test_creds')
        _check_results(results)

    elements = [Path(e).parts[-1] for e in tmp_path.iterdir()]
    print(elements)
    assert 'visit_1_dicom.tar' in elements
