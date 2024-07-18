
import sys
import tarfile
from pathlib import Path

from .modules.make_studyvisit_archive import main


def test_path_handling(tmp_path):
    base_dir = tmp_path / 'input' / 'd_1' / 'd_1_1' / 'd_1_1_1'
    base_dir.mkdir(parents=True)
    (base_dir / 'file1.txt').write_text('content 1')
    (base_dir / 'file2.txt').write_text('content 2')

    output_base_dir = tmp_path / 'output'

    study_id, visit_id = 'study_1', 'visit_1'
    main(str(base_dir), str(output_base_dir), study_id, visit_id)

    tar_file = tarfile.open(output_base_dir / study_id / f'{visit_id}_dicom.tar')
    assert tar_file.getnames() == [
        f'{study_id}_{visit_id}/file1.txt',
        f'{study_id}_{visit_id}/file2.txt',
    ]
