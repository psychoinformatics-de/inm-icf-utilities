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

Download the visit tarball:

.. code-block:: bash

   cd local_dicomstore/<project-ID>
   datalad download ...
   cd ../..

Deposit visit metadata alongside tarball
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   singularity run -B $STORE_DIR icf.sif deposit_visit_metadata --store-dir $STORE_DIR --id <project-ID> <visit ID>

Deposit dataset alongside tarball
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

DataLad dataset is created based on the metadata extracted in the
previous step.  Additionally, you need to provide the base URL of the
ICF store, ``<ICF STORE URL>`` (this base URL should not contain study
or visit ID). The URL, combined with respective IDs, will be
registered in the dataset as the source of the DICOM tarball, and used
for retrieval by dataset clones.

.. code-block:: bash

   singularity run -B $STORE_DIR icf.sif deposit_visit_dataset --store-dir $STORE_DIR --store-url <ICF STORE URL>

This will produce two files, ...

Remove the tarball
^^^^^^^^^^^^^^^^^^

The DICOM tarball can be safely removed.
