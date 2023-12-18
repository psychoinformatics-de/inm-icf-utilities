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
allow raw data versioning, and enable logical transformations of the
DICOM folder structure - see :ref:`dl-advanced` for examples of the
latter.

Obtain the tarball
^^^^^^^^^^^^^^^^^^

First, create an empty directory to be the local dataset store. The
last path component must be the ``project-ID`` used by the ICF store,
because following commands use project and visit IDs to determine
paths.

.. code-block:: bash

   mkdir -p local_dicomstore/<project-ID>

Download the visit tarball, keeping the same relative path:

.. code-block:: bash

   datalad download "https://data.inm-icf.de/<project-ID>/<visit-ID>_dicom.tar <project-ID>/<visit-ID>_dicom.tar"

Using ``datalad download`` for downloading the file has the benefit of
using DataLad's credential management. If this is the first time you
use DataLad to access the project directory, you will be asked to
provide your ICF credentials. See :ref:`dl-credentials` for details.

For the following examples, the *absolute path* to the local dicom
store will be represented by ``$STORE_DIR``:

.. code-block:: bash

   export STORE_DIR=$PWD/local_dicomstore


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

Deposit dataset alongside tarball
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

DataLad dataset is created based on the metadata extracted in the
previous step.  Additionally, you need to provide the base URL of the
ICF store, ``<ICF STORE URL>`` (this base URL should not contain study
or visit ID). The URL, combined with respective IDs, will be
registered in the dataset as the source of the DICOM tarball, and used
for retrieval by dataset clones.

.. code-block:: bash

   singularity run -B $STORE_DIR icf.sif deposit_visit_dataset \
     --store-dir $STORE_DIR --store-url <ICF STORE URL>

This will produce two files, ``<visit ID>_XDLA--refs`` and ``<visit
ID>_XDLA--repo-export`` (text file and zip archive
respectively). Together, they are a representation of a (lightweight)
DataLad dataset, and contain the information necessary to retrieve the
data content with DataLad (but do not contain the data content
itself).

Remove the tarball
^^^^^^^^^^^^^^^^^^

Finally, the DICOM tarball can be safely removed.

.. code-block:: bash

   rm local_dicomstore/<project-ID>/<visit ID>_dicom.tar

The local dicom store can be used as a DataLad entry point for
obtaining the dicom files.
