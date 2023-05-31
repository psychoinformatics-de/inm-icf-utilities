Developer docs
==============

Contributions in the form of bug reports or code are warmly welcomed.
You can find the source code as well as an issue tracker on `GitHub`_.

Development environment
^^^^^^^^^^^^^^^^^^^^^^^

Clone the source repository::

    git clone git@github.com:psychoinformatics-de/inm-icf-utilities.git
    cd inm-icf-utilities

Install development software requirements in a virtual environment::

    # create and enter a new virtual environment (optional)
    $ virtualenv --python=python3 ~/env/icf
    $ . ~/env/icf/bin/activate
    pip install -r requirements-devel.txt
    pip install -r docs/requirements.txt

Running tests
^^^^^^^^^^^^^

This package uses pytest for integration testing, and a CI test suite runs in
the source repository on GitHub automatically.
As the tooling are meant to run on specific systems only, executing tests locally
requires additional setup steps that likely make it infeasible unless your system
are the ICF servers.

The requirements are local DICOM data (not distributed alongside this software)
that matches the layout, naming scheme, and permission set that the ICF uses.
In addition, it requires the icf-utils Singularity image (see :ref:`singularity`),
which needs to be installed as ``icf-utils`` in ``/usr/bin``.
Code that achieves this setup can be found in `.appveyor.yml <https://github.com/psychoinformatics-de/inm-icf-utilities/blob/main/.appveyor.yml>`_.

If this is in place, set the environment variable ``INM_ICF_TEST_STUDIES``
to point to the directory with DICOM data, and execute integrations tests with::

   pytest -s -v .

.. _singularity:

Bundled utilities
^^^^^^^^^^^^^^^^^

The INM-ICF utilities are distributed as a bundle in the form of a
Singularity software container. This container is updated regularly
and can be downloaded from `ci.appveyor.com/api/projects/mih/inm-icf-utilities/artifacts/icf.sif <https://ci.appveyor.com/api/projects/mih/inm-icf-utilities/artifacts/icf.sif>`_.
When testing changes to the INM-ICF-utilities, the Singularity image needs to be
rebuilt with the changes included.
Its recipe can be found under ``singularity/icf.def``.
The image can be rebuild automatically using the Appveyor-based CI testsuite.
If only software dependencies change, an update is **not** triggered automatically
but requires that the `build cache is wiped <https://www.appveyor.com/docs/build-cache/#cleaning-up-cache>`_.


.. _GitHub: https://github.com/psychoinformatics-de/inm-icf-utilities