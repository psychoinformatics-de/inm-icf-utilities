DataLad-based access
--------------------

Software requirements
^^^^^^^^^^^^^^^^^^^^^

Accessing the ICF store requires `DataLad`_ with `Datalad-Next`_
extension installed.
You can find instructions for installing DataLad on your operating
system in the `DataLad Handbook`_.
`Datalad-Next`_ can be installed with `pip`_ [1]_.

.. _datalad: https://www.datalad.org/
.. _datalad-next: https://docs.datalad.org/projects/next
.. _datalad handbook: https://handbook.datalad.org/intro/installation.html
.. _pip: https://pip.pypa.io/en/stable/

Credentials
^^^^^^^^^^^

The ICF store is not publicly available, and ICF administrators will provide user names and passwords on a per-study basis.
DataLad will store or retrieve these credentials using your
operating system's keyring service. In general, the first time you use
DataLad to access a project directory, you will be prompted for your
credentials. If content retrieval succeeds, the credential will be
saved, and reused the next time you access a URL from the same realm.

If you have access to multiple projects, you can have different sets
of credentials. You can use the `datalad credentials`_ command from
DataLad Next to manage (e.g. query, set or remove) credentials known
to DataLad.

.. admonition:: DataLad usage in the context of GDPR

   DataLad is a client-side software. Usage of DataLad with ICF store
   is technically equivalent to downloading tar archives with ``wget``
   or with a web browser click-to-download: in either case, data
   access happens over https, and the authorisation is performed by
   the ICF server, not by the clients.

.. _datalad credentials: http://docs.datalad.org/projects/next/en/latest/generated/man/datalad-credentials.html


Clone & get
^^^^^^^^^^^

A visit dataset can be cloned with DataLad from a URL containing the
following components:

* store base URL (e.g., ``https://data.inm-icf.de``)
* study ID (e.g., ``my-study``)
* visit ID (e.g., ``P000123``)
* a set of additional parameters, always constant

The pattern for the URL is::

    'datalad-annex::?type=external&externaltype=uncurl&url=<store base URL>/<study ID>/<visit ID>_{{annex_key}}&encryption=none'

Given the exemplary values above, the pattern would expand to

.. code-block::

    'datalad-annex::?type=external&externaltype=uncurl&url=https://data.inm-icf.de/my-study/P000123_{{annex_key}}&encryption=none'

.. note:: The URL is arguably a bit clunky. A convenience short cut can be provided via configuration item ``datalad.clone.url-substitute.<label>`` and a substitution rule based on regular expressions. For example, clone URLs can be shortened to require only an identifier (here, ``https://data.inm-icf.de``), study ID, and visit ID (``inm-icf/<study-ID>/<visit-ID>``) with the following configuration:

   .. code-block::

      git config --global datalad.clone.url-substitute.inm-icf ',^https://data.inm-icf.de/([^/]+)/(.*)$,datalad-annex::?type=external&externaltype=uncurl&url=https://data.inm-icf.de/\1/\2_{{annex_key}}&encryption=none'

   This configuration allows DataLad to take any URL of the form ``https://data.inm-icf.de/<study-ID>/<visit-ID>`` and assemble the required ``datalad-annex::...`` URL on its own, and a clone call shortens into ``datalad clone https://data.inm-icf.de/my-study/P000123``.
   You are free to adjust this configuration custom to your needs and preferences.
   Further documentation on it can be found in the `DataLad Docs`_.

.. _DataLad Docs: http://docs.datalad.org/en/stable/design/url_substitution.html

Cloning will retrieve a lightweight dataset, which does not (yet)
contain file content. File content can be retrieved with `datalad
get`. DataLad will handle download and unpacking of the tar file.
Take a look at the section :ref:`dl-advanced` to learn about
useful convenience features DataLad adds on top of this.

Catalog-based clone URLs
^^^^^^^^^^^^^^^^^^^^^^^^

Instead of crafting clone URLs by hand, the ``datalad_catalog``
directory in the data store displays a copy-paste URL for cloning when
clicking the "Download with DataLad" button on each individual visit ID.


.. rubric:: Footnotes

.. [1] To install software with pip, run a call such as the one below
       in your favourite `virtual environment <https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/>`_::

              python -m pip install datalad-next
