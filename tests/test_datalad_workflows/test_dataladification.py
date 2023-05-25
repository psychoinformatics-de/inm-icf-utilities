from __future__ import annotations

import os
from pathlib import Path

from datalad.api import create
from datalad.distribution.dataset import Dataset
from datalad.runner.runner import WitlessRunner
from datalad.tests.utils_pytest import on_appveyor


existing_studies = os.environ['STUDIES'].split()
existing_visits = ['visit_a', 'visit_b']


def run_script(name: str,
               working_directory: str | Path,
               study_id: str,
               visit_id: str,
               ):

    script_path = Path(*(Path(__file__).parts[:-3] + ('bin',))) / name
    runner = WitlessRunner(cwd=working_directory)
    runner.run(
        (['sudo'] if on_appveyor else []) + [
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
                '/data/archives',
                study, visit
            )


def clone_visit(dataset: Dataset, study: str, visit: str):
    dataset.clone(
        'datalad-annex::?type=external&externaltype=uncurl'
        f'&url=https://data.inm-icf.de/{study}/{visit}_{{annex_key}}'
        '&encryption=none')


def test_dataladification(tmp_path: Path):
    # Perform dataladification
    dataladify_visits(existing_studies, existing_visits)

    # Try to clone the datasets and fetch the dicom tarfile
    for study in existing_studies:
        for visit in existing_visits:
            dataset = create(tmp_path / f'ds_{study}_{visit}')
            clone_visit(dataset, study, visit)
            # Try to get the tar file and the dicoms
            dataset.get(f'icf/{visit}_dicom.tar')
            dataset.get(f'{study}_{visit}')
