Package for the 2nd phase of the exoplanet imaging data challenge

This package provides the tools required for:

* injecting fake companion spectra;
* reading participants submitted results;
* evaluate and analyze the results (in particular distance metrics).


Jupyter notebook tutorials
--------------------------
Two Jupyter notebook tutorials are available in the tutorials folder:

* ``planet_injection_example`` shows how fake companions with given spectra are injected in a test IFU dataset - this may be useful for participants wishing to replicate the injection procedure in order to train their algorithm;
* ``preprocessing_example`` shows how to perform a better preprocessing of the provided data cubes (bad pixel correction, bad frame rejection). We did not run the latter for 2 reasons: i) we wished to provide the participants with the data cubes as they come out of their respective official pipelines, and ii) different retrieval methods may suffer/benefit in different ways from softer/harder bad frame trimming or the presence of residual bad pixels.


Installation and dependencies
-----------------------------

Using the setup.py file
^^^^^^^^^^^^^^^^^^^^^^^
You can download ``eidc2`` (for exoplanet imaging data challenge phase 2) from its GitHub repository as a zip file. A ``setup.py``
file (setuptools) is included in the root folder of phase2. Enter the package's
root folder and run:

.. code-block:: bash

  $ python setup.py install


Using Git
^^^^^^^^^
If you plan to contribute or experiment with the code you need to make a 
fork of the repository (click on the fork button in the top right corner) and 
clone it:

.. code-block:: bash

  $ git clone https://github.com/<replace-by-your-username>/phase2.git

If you do not create a fork, you can still benefit from the ``git`` syncing
functionalities by cloning the repository (but will not be able to contribute):

.. code-block:: bash

  $ git clone https://github.com/VChristiaens/phase2.git

Before installing the package, it is highly recommended to create a dedicated
conda environment to not mess up with the package versions in your base 
environment. This can be done easily with (replace spec_env by the name you want
for your environment):

.. code-block:: bash

  $ conda create -n eidc2_env python=3.9 ipython

To install ``eidc2``, simply cd into the phase2 directory and run the setup file 
in 'develop' mode:

.. code-block:: bash

  $ cd eidc2
  $ python setup.py develop

If cloned from your fork, make sure to link your phase2 directory to the upstream 
source, to be able to easily update your local copy when a new version comes 
out or a bug is fixed:

.. code-block:: bash

  $ git add remote upstream https://github.com/exoplanet-imaging-challenge/phase2


Loading `eidc2`
^^^^^^^^^^^^^^^
Finally, start Python or IPython and check that you are able to import ``eidc2``:

.. code-block:: python

  import eidc2
