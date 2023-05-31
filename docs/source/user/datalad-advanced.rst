DataLad datasets: Advanced features
-----------------------------------

Dicom sorting
^^^^^^^^^^^^^

A visit dataset will have a structure similar to the following:

.. code-block:: console

   $ datalad tree
   [DS~0]
   ├── P001234_P001234/
   │   └── incoming/
   │       └── 3T/
   │           └── 2_ABC_DEF/
   │               └── P001234/
   └── icf/

where the ``P001234`` directory contains DICOM files in a flat
hierarchy, and the ``icf`` directory contains the original tar
archive.

The dataset exposes a few select DICOM header fields (with information
describing its corresponding DICOM series) as `git-annex metadata`_.
You can preview metadata for a selected file with ``git annex
metadata`` (subset shown):

.. code-block:: console

   $ git annex metadata <file name>
   metadata <file name>
   Modality=MR
   ProtocolName=ep2d_diff_dir98_AP
   PulseSequenceName=*epse2d1_140
   SeriesDescription=ep2d_diff_dir98_AP
   SeriesNumber=10

These metadata can be used to organize DICOM files according to a
logical structure. For example, grouping by protocol name and series
number:

.. code-block:: console

  $ git annex view "protocolname=*" "seriesnumber=*"
  view (searching...) 
  Switched to branch 'views/protocolname=_;seriesnumber=_'
  ok

  ❱ datalad tree
  [DS~0]
  (...)
  ├── t1_mprage_0.9mm/
  │   └── 6/
  ├── t2w_space_0.9mm/
  │   └── 7/
  └── tfMRI_tapping
      └── 4/
      └── 5/
      
The view can be filtered, e.g. to only show anatomical (T1 or T2) sequences:

.. code-block:: console

   $ git annex vfilter "ProtocolName=t[12]*"
   
   $ datalad tree
   [DS~0]
   ├── t1_mprage_0.9mm/
   │   └── 6/
   └── t2w_space_0.9mm/
       └── 7/

Order of the components can be inverted:
   
.. code-block:: console

   $ git annex vcycle
   
   $ datalad tree
   [DS~0]
   ├── 6/
   │   └── t1_mprage_0.9mm/
   └── 7/
       └── t2w_space_0.9mm/

Previous views, and the starting branch, can be restored with

.. code-block:: console

  $ git annex vpop

As the operations only create views (and the annexed data organization
remains the same), these operations are very fast.
   
For more information, refer to the `git-annex-view`_ documentation.

.. _git-annex metadata: https://git-annex.branchable.com/metadata/
.. _git-annex-view: https://git-annex.branchable.com/git-annex-view/
