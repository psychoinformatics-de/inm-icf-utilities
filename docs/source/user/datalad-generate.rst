.. _dl-generate:

Generate DataLad datasets
-------------------------

The ICF archive for a given project contains DICOM files packaged in
tar archives (DICOM tarballs). In this section we describe creating
DataLad datasets, which index content and location of these tarballs,
for DataLad-based access on institute-local infrastructure.

In principle, such datasets are *lightweight*, meaning that they only
index the content that can be retrieved from the ICF archive (all
access restrictions apply). Using DataLad can simplify local access,
allow raw data versioning, integrate with existing workflows, and
enable logical transformations of the DICOM folder structure - see
:ref:`dl-advanced` for examples of the latter.

The workflow described below uses DataLad with DataLad-Next extension
for initial DICOM download and the INM-ICF tools packaged as a
Singularity container for subsequent steps (see
:ref:`dl-requirements`). ICF access credentials are required (see
:ref:`dl-credentials`).

Obtain the tarball
^^^^^^^^^^^^^^^^^^

First, create an empty directory to be the local dataset store. The
last path component must be the ``project-ID`` used by the ICF store,
because following commands use project and visit IDs to determine
paths.

.. code-block:: bash

   mkdir -p local_dicom_store/<project-ID>

Download the visit tarball, keeping the same relative path:

.. code-block:: bash

   datalad download "https://data.inm-icf.de/<project-ID>/<visit-ID>_dicom.tar local_dicom_store/<project-ID>/<visit-ID>_dicom.tar"

The local copy of the tarball is required to index its contents. It
can be removed afterwards -- datasets will use the ICF store as the
content source.

Using ``datalad download`` for downloading the file has the benefit of
using DataLad's credential management. If this is the first time you
use DataLad to access the project directory, you will be asked to
provide your ICF credentials. See :ref:`dl-credentials` for details.

For the following steps, the ICF utility scripts packaged as a
Singularity container will be used, and executed with ``singularity
run`` (see :ref:`container` for download and usage details). The
*absolute path* to the local DICOM store will be represented by
``$STORE_DIR``:

.. code-block:: bash

   export STORE_DIR=$PWD/local_dicom_store

Deposit visit metadata alongside tarball
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Information required to create a DataLad dataset needs to be extracted
from the tarball:

.. code-block:: bash

   singularity run -B $STORE_DIR icf.sif deposit_visit_metadata \
     --store-dir $STORE_DIR --id <project-ID> <visit ID>

This will generate two files, ``<visit ID>_metadata_dicoms.json`` and
``<visit ID>_metadata_tarball.json``, and place them alongside the
tarball. The former contains metadata describing individual files
within the tarball (relative path, MD5 checksum, size, and a small
subset of DICOM headers describing acquisition type), and the latter
describes the tarball itself.

Deposit dataset representation alongside tarball
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The next step is to create a lightweight, clone-able representation of
a dataset in the local dataset store. This step relies on the metadata
extracted with the previous command. Additionally, the base URL of the
ICF store needs to be provided (here represented by ``<ICF STORE
URL>``, this base URL should not contain study or visit ID). The URL,
combined with respective IDs, will be registered in the dataset as the
source of the DICOM tarball, and used for retrieval by dataset clones.

.. code-block:: bash

   singularity run -B $STORE_DIR icf.sif deposit_visit_dataset \
     --store-dir $STORE_DIR --store-url <ICF STORE URL> --id <project-ID> <visit ID>

This will produce two files, ``<visit ID>_XDLA--refs`` and ``<visit
ID>_XDLA--repo-export`` (text file and zip archive
respectively). Together, they are a representation of a (lightweight)
DataLad dataset, and contain the information necessary to retrieve the
data content with DataLad (but do not contain the data content
itself).

Create a catalog view (optional)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A catalog page (html+JS rendering of dataset contents generated with
`DataLad catalog`_) can be created for the visit dataset. This is
mostly useful when providing (internal) https access to the datasets.

The following command will create the catalog (or update its content)
and place it in the ``catalog`` folder in the study directory.

.. _DataLad catalog: https://docs.datalad.org/projects/catalog

.. code-block:: bash

   singularity run -B $STORE_DIR icf.sif catalogify_studyvisit_from_meta \
     --store-dir $STORE_DIR --id <project-ID> <visit ID>

This catalog needs to be subsequently served; a simple (possibly
local) http server is enough. See the generated README file in the
``catalog`` folder for details.

Remove the tarball
^^^^^^^^^^^^^^^^^^

Finally, the DICOM tarball can be safely removed.

.. code-block:: bash

   rm $STORE_DIR/<project-ID>/<visit ID>_dicom.tar

Metadata files can be removed, too, leaving only the dataset
representation in ``*XDLRA*`` files.

.. code-block:: bash

   rm $STORE_DIR/<project-ID>/<visit ID>_metadata_*.json


The local store can be used as a DataLad entry point for obtaining the
DICOM files from the ICF store (which would serve as the data source
for dataset clones); see :ref:`dl-access`.
