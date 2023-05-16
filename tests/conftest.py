from datalad.conftest import setup_package

# fixture setup
from datalad_next.tests.fixtures import (
    # no test can leave global config modifications behind
    # TODO: We cannot use this right now. It requires Git >= 2.32, but the
    # deployment target only has 2.30
    #check_gitconfig_global,
    # no test can leave secrets behind
    check_plaintext_keyring,
    # function-scope credential manager
    credman,
    # function-scope config manager
    # TODO: We cannot use this right now. It requires Git >= 2.32, but the
    # deployment target only has 2.30
    #datalad_cfg,
    # function-scope temporary keyring
    tmp_keyring,
    # function-scope, Dataset instance
    dataset,
    #function-scope, Dataset instance with underlying repository
    existing_dataset,
    #function-scope, Dataset instance with underlying Git-only repository
    existing_noannex_dataset,
)

from .fixtures import (
    dicom_server,
)
