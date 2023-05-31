ICF Personnel guide
===================

The INM-ICF Utilities Github repository provides a set of executable
Python scripts which automate generation of deposits in the ICF
archive. To simplify deployment, these scripts and all their
dependencies are packaged as a Singularity container.

Archive generation
------------------

Containerized execution
^^^^^^^^^^^^^^^^^^^^^^^

With the Singilarity image, ``icf.sif``, all scripts are made directly
available, either through ``singularity run``:

.. code-block:: console

   $ singularity run icf.sif make_studyvisit_archive ...

or, after making the image file executable:

.. code-block:: console

   $ ./icf.sif make_studyvisit_archive ...

Archive generation
^^^^^^^^^^^^^^^^^^

A TAR archive containing files from a single study visit can be
generated and deposited in the study directory with
``make_studyvisit_archive``.

.. code-block:: console

   $ ./icf.sif make_studyvisit_archive --help
   usage: make_studyvisit_archive [-h] [-o PATH] --id STUDY-ID VISIT-ID <input-dir>

DataLad dataset generation
^^^^^^^^^^^^^^^^^^^^^^^^^^

The DataLad dataset can be generated and placed alongside the tarballs
without affecting them. Placement in the study folder guarantees the
same access permissions (authenticated https). This provides users
with DataLad-based access and related additional features. The
datasets are generated based on file metadata -- the TAR archive
remains the only data source -- so storage overhead is minimal.

All scripts have the same set of arguments.

Required metadata can be prepared with ``getmeta_studyvisit``:

.. code-block:: console

  $ ./icf.sif getmeta_studyvisit -h
  usage: getmeta_studyvisit [-h] [-o PATH] --id STUDY-ID VISIT-ID

A dataset can be created with ``dataladify_studyvisit_from_meta``:

.. code-block:: console

   $ ./icf.sif dataladify_studyvisit_from_meta -h
   usage: dataladify_studyvisit_from_meta [-h] [-o PATH] --id STUDY-ID VISIT-ID

DataLad catalog can be created or updated with ``catalogify_studyvisit_from_meta``:

.. code-block:: console

  $ ./icf.sif dataladify_studyvisit_from_meta --help
  usage: dataladify_studyvisit_from_meta [-h] [-o PATH] --id STUDY-ID VISIT-ID
