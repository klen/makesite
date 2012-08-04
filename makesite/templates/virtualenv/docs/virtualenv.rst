Virtualenv
----------

Template has created virtualenv and watching `requirements.txt` for changes and updates.

Requirements
^^^^^^^^^^^^
Installed `pip` and `virtualenv` python packages

Variables
^^^^^^^^^

.. option:: virtualenv_dir

    Define directory for create virtualenv

    Default: %(deploy_dir)s/.virtualenv

.. option:: pip_projectfile

    Define path to `requirements.txt` file. In project source by default.

    Default: %(deploy_dir)s/source/requirements.txt

.. option:: pip_options

    Define command line options for run PIP

    Default: -IM -download-cache=/tmp/.pip-cache


Install operation
^^^^^^^^^^^^^^^^^

Create virtualenv in :option:`virtualenv_dir`.
Install requirements from :option:`pip_projectfile`.


Update operation
^^^^^^^^^^^^^^^^

Update requirements from  :option:`pip_projectfile` if it changes.
