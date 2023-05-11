from pathlib import Path

from datalad_next.datasets import Dataset
from datalad.api import (
    create,
    download
)


protocol = 'http'


def test_example(tmp_path: Path):
    dataset_path = tmp_path / 'ds'
    dataset = Dataset(dataset_path).create()
    dataset.download(
        f'{protocol}://test.user:secret_1@localhost/'
        f'~appveyor/study_1/visit_1_dicom.tar')
    dataset.download(
        f'{protocol}://localhost/~appveyor/study_1/visit_1_dicom.tar.md5sum')
    elements = dataset_path.iterdir()
    print(elements)
