Welcome to PhilipPlay's documentation!
=======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   sourcedoc/index

Build Debian Package
--------------------

You can build the Debian package for *PhilipPlay* by typing the following command in the
root directory of the *PhilipPlay* project:

.. code-block:: bash

    debuild -us -uc

This will create the Debian package in the directory one level up from the projects root directory.

Installation
------------

To install *PhilipPlay* you first need to copy the Debian package to the *Raspberry Pi*.
Then you need to install the package dependecies and the package using the following commands:

.. code-block:: bash

    apt install python3-argparse python3-yaml
    dpkg -i philipplay_<version>_all.deb

The Debian package will install all the required files to the *Raspberry Pi*. This also includes
an entry in the systems autostart folder. Next time you boot your *Raspberry Pi*, the *PhilipPlay*
audio player will automatically start in fullscreen mode.


Keyboard Mapping
----------------

* "1-9" - Select Folders and Skip Songs
* "0,S" - Stop Playing
* "+." - Increase Volume
* "-," - Decrease Volume
* "Q" - Quit Player


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
