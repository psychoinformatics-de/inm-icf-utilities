Administrator docs
==================

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

   $ singularity run <singularity options> icf.sif <script name> <script options>

or by making the image file executable.

The singularity image can also be installed as if it was a system
package. For this, fill in the placeholders in the following script,
and save it as ``icf-utils``:

.. code-block:: sh

   #!/bin/sh
   set -e -u
   singularity run -B <absolute-path-to-data> <absolute-path-to-icf.sif-file> "$@" > icf-utils

The ``-B`` defines a bind path, making it accessible from within the
container.

Afterwards, install it under ``/usr/bin`` to make all functionality
available under an ``icf-utils`` command.

.. code-block::

   $ sudo install -t /usr/bin icf-utils

Archival workflow
^^^^^^^^^^^^^^^^^

The main part of visit archival is the creation a TAR file.

The DataLad dataset can be generated and placed alongside the tarballs
without affecting them. Placement in the study folder guarantees the
same access permissions (authenticated https). The datasets are
generated based on file metadata -- the TAR archive remains the only
data source -- so storage overhead is minimal.

Four scripts, executed in the given order, capture the archival
process.

Script listing
^^^^^^^^^^^^^^

``make_studyvisit_archive``
"""""""""""""""""""""""""""

This utility generates a TAR archive from a directory containing DICOM files.

The input directory can have any number of files, with any organization or
naming. However, the DICOM files are assumed to come from a single "visit"
(i.e., the time between a person or sample entering and then leaving a
scanner). The input directory's content is copied into a TAR archive verbatim,
with no changes to filenames or organization.

In order to generate reproducible TAR archives, the file order, recorded
permissions and ownership, and modification times are standardized. All files
in the TAR archive are declared to be owned by root/root (uid/gid: 0/0) with
0644 permissions. The modification time of any DICOM file is determined
by its contained DICOM `StudyDate/StudyTime` timestamps. The modification time
for any non-DICOM file is set to the latest timestamp across all DICOM files.

.. code-block:: console

   $ icf-utils make_studyvisit_archive --help
   usage: make_studyvisit_archive [-h] [-o PATH] --id STUDY-ID VISIT-ID <input-dir>

``deposit_visit_metadata``
""""""""""""""""""""""""""

This command locates the DICOM tarball for a particular visit in a
study (given by their respective identifiers) in the data store, and
extracts a minimal set of metadata tags for each DICOM image, and the
TAR archive as a whole. These metadata are then deposited in two
files, in JSON format, in the study directory:

- ``{visit_id}_metadata_tarball.json``

  JSON object with basic properties of the archive, such as 'size', and
  'md5'.

- ``{visit_id}_metadata_dicoms.json``

  JSON array with essential properties for each DICOM image file, such as
  'path' (relative path inside the TAR archive), 'md5' (MD5 checksum of
  the DICOM file), 'size' (in bytes), and select standard DICOM tags,
  such as "SeriesDescription", "SeriesNumber", "Modality",
  "MRAcquisitionType", "ProtocolName", "PulseSequenceName". The latter
  enable a rough, technical characterization of the images in the TAR
  archive.

.. code-block:: console

  $ icf-utils getmeta_studyvisit -h
  usage: getmeta_studyvisit [-h] [-o PATH] --id STUDY-ID VISIT-ID

``deposit_visit_dataset``
"""""""""""""""""""""""""

This command reads the metadata deposit from
``deposit_visit_metadata`` for a visit in a study (given by their
respective identifiers) from the data store, and generates a DataLad
dataset from it. This DataLad dataset provides versioned access to the
visit's DICOM data, up to single-image granularity.  Moreover, all
DICOM files are annotated with basic DICOM tags that enable on-demand
dataset views for particular applications (e.g., DICOMs sorted by
image series and protocol name). The DataLad dataset is deposited in
two files in the study directory:

- ``{visit_id}_XDLRA--refs``
- ``{visit_id}_XDLRA--repo-export``

where the former enables `datalad/git clone` operations, and the latter
represents the actual dataset as a compressed archive.

.. code-block:: console

   $ icf-utils dataladify_studyvisit_from_meta -h
   usage: dataladify_studyvisit_from_meta [-h] [-o PATH] --id STUDY-ID VISIT-ID

``catalogify_studyvisit_from_meta``
"""""""""""""""""""""""""""""""""""

This command creates or updates a DataLad catalog -- a user-facing
html rendering of dataset contents. It is placed in the ``catalog``
folder in the study directory.

.. code-block:: console

  $ icf-utils dataladify_studyvisit_from_meta --help
  usage: dataladify_studyvisit_from_meta [-h] [-o PATH] --id STUDY-ID VISIT-ID
