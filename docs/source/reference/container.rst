.. _container:

Containerized execution
-----------------------

To simplify deployment, ICF utilities scripts and all their
dependencies are packaged as a `Singularity`_ v3 container
(`download`_).

.. _singularity: https://docs.sylabs.io/guides/main/user-guide/
.. _download: https://ci.appveyor.com/api/projects/mih/inm-icf-utilities/artifacts/icf.sif

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
