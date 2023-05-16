from __future__ import annotations
from pathlib import Path

import pytest

from datalad.api import (
    download,
)
from datalad.support.exceptions import IncompleteResultsError
from datalad.utils import chpwd


def _check_results(results: list[dict]):
    assert all(result['status'] == 'ok' for result in results)


def test_example_unauthorized(dicom_server):
    print(dicom_server)
    with pytest.raises(IncompleteResultsError):
        download(
            f'{dicom_server["base_url"]}/study_1/visit_1_dicom.tar',
            result_renderer='disabled')


def test_example_authorized(
    dicom_server, tmp_path: Path, tmp_keyring,
    dataaccess_credential, credman,
):
    print(dicom_server)
    credman.set(**dataaccess_credential)

    with chpwd(tmp_path):
        results = download(
            f'{dicom_server["base_url"]}/study_1/visit_1_dicom.tar',
            credential=dataaccess_credential['name'],
            result_renderer='disabled')
        _check_results(results)

    elements = [Path(e).parts[-1] for e in tmp_path.iterdir()]
    assert 'visit_1_dicom.tar' in elements
