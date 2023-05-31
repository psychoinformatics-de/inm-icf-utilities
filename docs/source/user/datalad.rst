DataLad-based access
--------------------

Software requirements
^^^^^^^^^^^^^^^^^^^^^

Accessing the ICF store requires `DataLad`_ with `Datalad-Next`_
extension installed.

.. _datalad: https://www.datalad.org/
.. _datalad-next: https://docs.datalad.org/projects/next

Credentials
^^^^^^^^^^^

The ICF store is not publicly available, and ICF administrators will provide user names and passwords on a per-study basis.

DataLad will store or retrieve your username and password using your
operating system's keyring service. In general, the first time you use
DataLad to access a project directory, you will be prompted for your
credentials. If content retrieval succeeds, the credential will be
saved, and reused the next time you access a URL from the same realm.

If you have access to multiple projects, you can have different sets
of credentials. You can use the `datalad credentials`_ command from
DataLad Next to manage (e.g. query, set or remove) credentials known
to DataLad.

.. note::

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

* store base URL
* study ID
* visit ID
* a set of additional parameters, always constant

The pattern for the URL is::

    'datalad-annex::?type=external&externaltype=uncurl&url=<store base URL>/<study ID>/<visit ID>_{{annex_key}}&encryption=none'
  
.. note:: A convenience short cut can be provided via configuration
   item ``datalad.clone.url-substitute...``

Cloning will retrieve a lightweight dataset, which does not (yet)
contain file content. File content can be retrieved with `datalad
get`. DataLad will handle download and unpacking of the tar file.
