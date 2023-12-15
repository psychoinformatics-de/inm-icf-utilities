Administrator docs
==================

Archival workflow
-----------------

The main part of visit archival is the creation a TAR file.

Optionally, the DataLad dataset can be generated and placed alongside
the tarballs without affecting them. Placement in the study folder
guarantees the same access permissions (authenticated https). The
datasets are generated based on file metadata -- the TAR archive
remains the only data source -- so storage overhead is minimal.

Four scripts, executed in the given order, capture the archival
process. See :ref:`scripts` for usage details and :ref:`container` for
recommended deployment of the tools.

- ``make_studyvisit_archive``
- ``deposit_visit_metadata`` (optional)
- ``deposit_visit_dataset`` (optional)
- ``catalogify_studyvisit_from_meta`` (optional)

Creation of the TAR file needs to be done by the ICF. The remaining
three steps can be done by the ICF (with results deposited alongside
the TAR file), or by the ICF users who can access the data (on their
own infrastructure), and for this reason are marked as optional.
