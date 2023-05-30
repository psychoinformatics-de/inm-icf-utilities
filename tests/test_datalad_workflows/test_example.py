from __future__ import annotations
from pathlib import Path

import pytest

from datalad.api import download
from datalad_next.exceptions import IncompleteResultsError
from datalad_next.tests.utils import assert_status

from ..fixtures import (
    dataaccess_credential,
    data_webserver,
    test_studies_dir,
    test_study_names,
)


def test_example_unauthorized(data_webserver):
    with pytest.raises(IncompleteResultsError):
        download(
            f'{data_webserver}/study_1/visit_a_dicom.tar',
            result_renderer='disabled')


def test_example_authorized(
    data_webserver, tmp_path: Path, tmp_keyring,
    dataaccess_credential, credman,
):
    credman.set(**dataaccess_credential)

    target_file = tmp_path / 'visit_a_dicom.tar'

    results = download(
        {f'{data_webserver}/study_1/visit_a_dicom.tar': target_file},
        credential=dataaccess_credential['name'],
        result_renderer='disabled',
        on_failure='ignore',
    )
    assert_status('ok', results)
    assert target_file.exists()
