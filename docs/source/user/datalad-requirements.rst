.. _dl-requirements:

DataLad requirements
--------------------

Accessing the ICF store contents and cloning datasets generated with
the ICF tooling requires `DataLad`_ with `Datalad-Next`_ extension
installed.  You can find instructions for installing DataLad on your
operating system in the `DataLad Handbook`_.  `Datalad-Next`_ can be
installed with `pip`_ [1]_.

Generating DataLad datasets based on the DICOMS in the ICF store
additionally requires the INM-ICF tools, which are packaged as a
`Singularity`_ container; see :ref:`container`. The tools are not
required for accessing already existing DataLad datasets.

Obtaining data hosted in the ICF store requires access credentials for
a given study, issued by the ICF. DataLad acts only as a client
software. See :ref:`dl-credentials` for details.

.. rubric:: Footnotes

.. [1] To install software with pip, run a call such as the one below
       in your favourite `virtual environment`_:

       .. code-block:: bash

          python -m pip install datalad-next

.. _datalad: https://www.datalad.org/
.. _datalad-next: https://docs.datalad.org/projects/next
.. _datalad handbook: https://handbook.datalad.org/intro/installation.html
.. _pip: https://pip.pypa.io/en/stable/
.. _virtual environment: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
.. _singularity: https://docs.sylabs.io/guides/main/user-guide/
