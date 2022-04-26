This is the package associated to the 2nd phase of the exoplanet imaging data challenge. It provides the tools required for:

* injecting fake companion spectra;
* reading participants submitted results;
* evaluate and analyze the results.


Jupyter notebook tutorials
--------------------------
Three Jupyter notebooks are available in the tutorials folder:

* ``planet_injection_trainingset`` shows how fake companions with given spectra are injected in a test IFU dataset - this may be useful for participants wishing to replicate the injection procedure in order to train their algorithm;
* ``preprocessing_example`` shows how to perform a better preprocessing of the provided data cubes (bad pixel correction, bad frame rejection). We did not run the latter for 2 reasons: i) we wished to provide the participants with the data cubes as they come out of their respective official pipelines, and ii) different retrieval methods may suffer/benefit in different ways from softer/harder bad frame trimming or the presence of residual bad pixels.
* ``MEF_creation_example`` shows how to write your results in Multi-Extension Fits file format, the requested format for submission of your results to the data challenge.

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
First, clone the repository:

.. code-block:: bash

  $ git clone https://github.com/exoplanet-imaging-challenge/phase2.git

Before installing the package, it is highly recommended to create a dedicated
conda environment to not mess up with the package versions in your base 
environment. This can be done easily with (replace eidc2_env by the name you want
for your environment):

.. code-block:: bash

  $ conda create -n eidc2_env python=3.9 ipython

Then, to install ``eidc2``, simply cd into the phase2 directory 
(in your local clone of the repository), and run the setup file 
to install the package:

.. code-block:: bash

  $ cd eidc2
  $ python setup.py install


Using Git (data challenge organizers only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Organisers wishing to contribute or experiment with the code first need to make a 
fork of the repository (click on the fork button in the top right corner). Then it 
is a matter of cloning your fork with:

.. code-block:: bash

  $ git clone https://github.com/<replace-by-your-username>/phase2.git

And follow the same steps as highlighted in the previous section. The only
2 exceptions are: 1) to run the setup file using the 'develop' mode, instead of 'install':

.. code-block:: bash

  $ cd eidc2
  $ python setup.py develop

2) make sure to link your phase2 directory to the upstream source, 
to be able to easily update your local copy after modifications by 
other organizers:

.. code-block:: bash

  $ git add remote upstream https://github.com/exoplanet-imaging-challenge/phase2


Loading `eidc2`
^^^^^^^^^^^^^^^
Finally, start Python or IPython and check that you are able to import ``eidc2``:

.. code-block:: python

  import eidc2
