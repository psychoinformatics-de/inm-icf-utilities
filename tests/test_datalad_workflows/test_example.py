from pathlib import Path

from datalad.api import download
from datalad.distribution.dataset import Dataset
from datalad_next.utils import chpwd


protocol = 'http'


def test_example(tmp_path: Path):
    dataset_path = tmp_path / 'ds'
    dataset = Dataset(dataset_path).create()

    res1 = download(
        f'{protocol}://test.user:secret_1@localhost/'
        f'~appveyor/study_1/visit_1_dicom.tar',
        dataset=dataset)
    res2 = download(
        f'{protocol}://test.user:secret_1@localhost/'
        f'~appveyor/study_1/visit_1_dicom.tar.md5sum',
        dataset=dataset)

    elements = dataset_path.iterdir()
    print(elements)
