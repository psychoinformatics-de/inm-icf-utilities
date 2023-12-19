.. _dl-access:

Access data with DataLad
------------------------

This section describes accessing the ICF data by cloning DataLad
datasets which have already been created and made available, most
likely on local infrastructure. Dataset generation is described in
the previous section, :ref:`dl-generate`.

This workflow uses DataLad with DataLad-Next extension (see
:ref:`dl-requirements`). DataLad datasets index data in their original
(ICF) location. Obtaining data hosted in the ICF store requires access
credentials for a given study, issued by the ICF. DataLad acts only as
a client software. See :ref:`dl-credentials` for details.

Clone & get
^^^^^^^^^^^

If a visit dataset has been prepared and placed in an accessible
location, it can be cloned with DataLad from a URL containing the
following components:

* a set of configuration parameters, always constant
* store base URL (e.g., ``file:///data/group/groupname/local_dicom_store``) [1]_
* study ID (e.g., ``my-study``)
* visit ID (e.g., ``P000123``)
* a file name suffix / template, ``_annex{{annex_key}}`` (verbatim), always constant

The pattern for the URL is::

    'datalad-annex::?type=external&externaltype=uncurl&encryption=none&url=<store base URL>/<study ID>/<visit ID>_{{annex_key}}'

Given the exemplary values above, the pattern would expand to

.. code-block::

    'datalad-annex::?type=external&externaltype=uncurl&encryption=none&url=file:///data/group/groupname/local_dicom_store/my-study/P000123_{{annex_key}}'

.. note:: The URL is arguably a bit clunky. A convenience short cut can be provided via configuration item ``datalad.clone.url-substitute.<label>`` and a substitution rule based on regular expressions. For example, clone URLs can be shortened to require only an identifier (here, ``file:///data/group/groupname/local_dicom_store``), study ID, and visit ID (``inm-icf/<study-ID>/<visit-ID>``) with the following configuration:

   .. code-block::

      git config --global datalad.clone.url-substitute.inm-icf ',^file:///data/group/groupname/local_dicom_store/([^/]+)/(.*)$,datalad-annex::?type=external&externaltype=uncurl&encryption=none&url=file:///data/group/groupname/local_dicom_store/\1/\2_{{annex_key}}'

   This configuration allows DataLad to take any URL of the form ``file:///data/group/groupname/local_dicom_store/<study-ID>/<visit-ID>`` and assemble the required ``datalad-annex::...`` URL on its own, and a clone call shortens into ``datalad clone file:///data/group/groupname/local_dicom_store/my-study/P000123``.
   You are free to adjust this configuration custom to your needs and preferences.
   Further documentation on it can be found in the `DataLad Docs`_.

.. _DataLad Docs: http://docs.datalad.org/en/stable/design/url_substitution.html

Cloning will retrieve a lightweight dataset, which does not (yet)
contain file content. File content can be retrieved with ``datalad
get``. DataLad will handle download and unpacking of the tar file.
Take a look at the section :ref:`dl-advanced` to learn about useful
convenience features DataLad adds on top of this.


.. rubric:: Footnotes

.. [1] Examples use ``file://`` URLs, given that the datasets are most
       likely to be generated on institute-local infrastructure. Other
       protocoles (e.g. ``https://`` or ``ssh://``) can be substituted
       depending on the particular setup, without affecting the URL
       structure.
