from datalad.conftest import setup_package

# fixture setup
from datalad_next.tests.fixtures import (
    # no test can leave global config modifications behind
    check_gitconfig_global,
    # no test can leave secrets behind
    check_plaintext_keyring,
    # function-scope credential manager
    credman,
    # function-scope config manager
    datalad_cfg,
    # function-scope temporary keyring
    tmp_keyring,
    # function-scope, Dataset instance
    dataset,
    #function-scope, Dataset instance with underlying repository
    existing_dataset,
    #function-scope, Dataset instance with underlying Git-only repository
    existing_noannex_dataset,
)

# local fixtures setup
from .fixtures import (
    dataaccess_credential,
    data_webserver,
    test_studies_dir,
    test_study_names,
)
