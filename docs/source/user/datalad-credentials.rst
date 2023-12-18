.. _dl-credentials:

Manage DataLad credentials
--------------------------

The ICF store is not publicly available, and ICF administrators will
provide user names and passwords on a per-study basis.  DataLad will
store or retrieve these credentials using your operating system's
keyring service. In general, the first time you use DataLad to access
a project directory, you will be prompted for your credentials. If
content retrieval succeeds, you will have a possibility of saving the
credential, to be reused the next time you access a URL from the same
realm.

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
