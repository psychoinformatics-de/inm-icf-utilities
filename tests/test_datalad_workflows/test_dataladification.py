from __future__ import annotations

import os
from pathlib import Path

from datalad.api import clone
from datalad.distribution.dataset import Dataset
from datalad.runner.runner import WitlessRunner
from datalad.tests.utils_pytest import on_appveyor

from ..fixtures import (
    dataaccess_credential,
    data_webserver,
    test_study_names,
)

existing_visits = ['visit_a', 'visit_b']
studies_dir = os.environ['STUDIES_DIR']


def run_script(name: str,
               working_directory: str | Path,
               study_id: str,
               visit_id: str,
               ):

    script_path = Path(*(Path(__file__).parts[:-3] + ('bin',))) / name
    runner = WitlessRunner(cwd=working_directory, env=dict(os.environ))
    runner.run(
        (['sudo', '-E', '--preserve-env=PATH'] if on_appveyor else []) + [
            str(script_path),
            '--id',
            study_id,
            visit_id
        ]
    )


def dataladify_visits(studies: list[str], visits: list[str]):
    for study in studies:
        for visit in visits:
            run_script(
                'dataladify_studyvisit',
                studies_dir,
                study, visit
            )


def clone_visit(path: Path, url: str, study: str, visit: str) -> Dataset:
    return clone(
        source='datalad-annex::?type=external&externaltype=uncurl'
               f'&url={url}/{study}/{visit}_{{{{annex_key}}}}'
               '&encryption=none',
        path=path
    )


def test_dataladification(tmp_path: Path,
                          test_study_names,
                          data_webserver,
                          dataaccess_credential,
                          credman):

    # Set credentials for the realm
    credman.set(**{
        **dataaccess_credential,
        'realm': 'http://data.inm-icf.de/Restricted'
    })

    # Perform dataladification
    dataladify_visits(test_study_names, existing_visits)

    # Try to clone the datasets and fetch the dicom tarfile
    for study in test_study_names:
        for visit in existing_visits:
            dataset = clone_visit(
                tmp_path / f'ds_{study}_{visit}',
                data_webserver,
                study,
                visit
            )
            # Try to get the tar file and the DICOMs
            dataset.get(f'icf/{visit}_dicom.tar')
            dataset.get(f'{study}_{visit}')
