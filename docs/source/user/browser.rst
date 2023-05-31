Browser-based access
--------------------

Study directory listing can be viewed in a web browser, by navigating
to an address composed of: ``<store base URL>/<study identifier>``.
Users will be prompted for credentials. The listing will contain the
following:

* DICOM files in tar archives, one per visit, ``<visit ID>_dicom.tar``
* Checksums of the tar archives, allowing verification of data
  integrity, ``<visit ID>_dicom.tar.md5sum``
* (optional) a ``catalog`` directory containing a catalog of the study
  visits (which can be used to view e.g. available modalities and
  DICOM series for each visit)


.. code-block:: console

   data.inm-icf.de/my-study
   ├── P000123_dicom.tar
   ├── P000123_dicom.tar.md5sum
   └── datalad_catalog/

Catalog-based browsing
======================

By entering the ``datalad_catalog`` directory, users will be able to
browse through the directory tree with additional annotations
of available metadata, and search for acquisitions based on keywords
or name.

Downloads
=========

tar archives and checksums can be downloaded individually by clicking
on them in the plain directory listing of the store.
Alternatively, they can be downloaded in the catalog browser in the ``Content`` menue of each individual acquisition.
