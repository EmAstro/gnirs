================
Installing gnirs
================

Installing Dependencies
=======================

We highly recommend that you use Anaconda for the majority of these installations.

python and dependencies
-----------------------

gnirs runs with  `python <http://www.python.org/>`_ 3.9 and with the following dependencies:

* `python <http://www.python.org/>`_ -- version 3.9 or later
* `astropy <https://www.astropy.org/>`_ -- version 5.0 or later


git clone
---------

To install the package via GitHub run::

    git clone https://github.com/EmAstro/gnirs.git

And, given that the packages is still work in progress and you may want to updated on-the-fly, we then recommend to install it with the `develop` option::

    cd gnirs
    python setup.py develop
