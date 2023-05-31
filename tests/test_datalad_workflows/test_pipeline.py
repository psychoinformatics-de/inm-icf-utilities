from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Iterable
from urllib.parse import (
    urlparse,
    urlunparse,
    ParseResult,
)

from datalad.api import clone
from datalad.distribution.dataset import Dataset
from datalad.runner.runner import WitlessRunner
from datalad.tests.utils_pytest import on_appveyor
from datalad_catalog.webcatalog import WebCatalog
from datalad_next.credman import CredentialManager

from .utils import get_restricted_realm


existing_visits = ['visit_a', 'visit_b']


def run_script(name: str,
               working_directory: str | Path,
               study_id: str,
               visit_id: str,
               ):

    script_path = Path(*(Path(__file__).parts[:-3] + ('bin',))) / name
    runner = WitlessRunner(cwd=working_directory, env=dict(os.environ))
    runner.run(
        [
            str(script_path),
            '--id',
            study_id,
            visit_id
        ]
    )


def process_visits(studies_dir: Path,
                   studies: list[str],
                   visits: list[str]
                   ):
    for study in studies:
        for visit in visits:
            # run metadata generation script
            run_script(
                'deposit_visit_metadata',
                studies_dir,
                study, visit
            )
            # run dataladification script
            run_script(
                'deposit_visit_dataset',
                studies_dir,
                study, visit
            )
            # run catalogification script
            run_script(
                'catalogify_studyvisit_from_meta',
                studies_dir,
                study, visit
            )


def get_clone_annex_url(source_url: str,
                        study: str,
                        visit: str
                        ) -> tuple[str, str]:

    if source_url.endswith('/'):
        source_url = source_url[:-1]

    access_url = f'{source_url}/{study}'
    auth_realm = get_restricted_realm(access_url)

    parsed_url = urlparse(access_url)

    copy_attributes = ['scheme', 'netloc', 'path', 'params', 'query', 'fragment']
    realm_parsed_url = ParseResult(**{
        name: getattr(parsed_url, name) if name != 'path' else auth_realm
        for name in copy_attributes
    })

    return (
        'datalad-annex::?type=external&externaltype=uncurl'
        f'&url={source_url}/{study}/{visit}_{{{{annex_key}}}}'
        '&encryption=none',
        urlunparse(realm_parsed_url),
    )


def add_credentials(realms: Iterable[str],
                    credentials: dict,
                    credman: CredentialManager,
                    ):

    # Add credentials for all URLs to credential manager
    for index, realm in enumerate(realms):
        kwargs = {
            **credentials,
            'name': f'icf-test-credentials-{index}',
            'realm': realm
        }
        result = credman.set(**kwargs)
        assert result is not None


def clone_visit(path: Path,
                source_url: str,
                study: str,
                visit: str,
                credentials: dict,
                credman: CredentialManager,
                ) -> Dataset:

    # Get involved URLs and set credentials for `auth_url`
    clone_url, auth_realm = get_clone_annex_url(source_url, study, visit)
    add_credentials([auth_realm], credentials, credman)

    # Clone a visit from the clone URL
    return clone(source=clone_url, path=path)


def test_pipeline(tmp_path: Path,
                  test_studies_dir: str,
                  test_study_names: list[str],
                  data_webserver: str,
                  dataaccess_credential: dict,
                  credman: CredentialManager,
                ):

    # Perform metadata generation, dataladification, and catalogification
    process_visits(
        Path(test_studies_dir),
        test_study_names,
        existing_visits,
    )

    # 1. Test metadata generation
    # - assert generated metadata files exist and load their content
    metadata_types = ['tarball', 'dicoms']
    for study in test_study_names:
        for visit in existing_visits:
            for m in metadata_types:
                metadata_path = Path(test_studies_dir) /\
                    study / f'{visit}_metadata_{m}.json'
                assert metadata_path.exists()
                with open(metadata_path) as f:
                    json.load(f)

    # 2. Test dataset generation
    # - Try to clone the datasets and fetch the dicom tarfile
    for study in test_study_names:
        for visit in existing_visits:
            dataset = clone_visit(
                tmp_path / f'ds_{study}_{visit}',
                data_webserver,
                study,
                visit,
                dataaccess_credential,
                credman,
            )
            # TODO reenable once the server setup is actually compatible
            # TODO swap the order of gets, or actually drop the tar get
            # completely. Pulling individual files will do all that internally
            # Try to get the tar file and the DICOMs
            #dataset.get(f'icf/{visit}_dicom.tar')
            #dataset.get(f'{study}_{visit}')

    # 3. Test catalog generation
    # - assert that study catalogs have been created using webcatalog method
    for study in test_study_names:
        catalog_path = Path(test_studies_dir) / study / 'catalog'
        ctlg = WebCatalog(location=str(catalog_path))
        assert ctlg.is_created()
