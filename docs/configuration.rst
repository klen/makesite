.. highlight:: rst

Configuration
=============

Makesite deploy options are specified on the `command line`_ and `configuration files`_.


Configuration files
-------------------

Makesite configuration files in `INI format`_ and must have a ``makesite.ini`` name.
Each can contain two sections: *Main* and *Templates*.
Section *Main* contain project deploy options.
Section *Templates* contain custom templates paths.

The configuration files are loaded in the fololowing order:

#. Default configuration file: makesite.ini from makesite;

#. From user home directory if exists;

#. From base projects deploy dir :envvar:`SITES_HOME` if exists;

#. From path of :option:`-c` option if exists;

#. From project source after load, if exists.


Settings from each next configuration file owerwrites previous.


Command line
------------

.. program:: makesite

.. option:: -p <sites_path>, --path=<sites_path>

   Path to projects dir, required if not set $SITES_HOME.
   Saved in **sites_home** variable.

.. option:: -b <branch name>, --branch=<branch_name>

   Deployed branch of project, default is 'master'.
   Saved in **branch** variable.

.. option:: -t <templates>, --tempalte=<templates>

    One or more template names separated by commas.
    Saved in **template** variable.

.. option:: -a, --append

    Tell makesite append template from :option:`-t` to existed project.

.. option:: -c <path_to_config>, --config=<path_to_config>

    Path to custom config file.

.. option:: -m <module_name>, --module=<module_name>

    Deploy makesite built-in module.

.. option:: -s <source_path>, --source=<source_path>

    Source path. VCS address starts with prefix: git+git://github.com/...
    Saved in **src** variables.


Configuration options
---------------------

    .. note ::

        In options you can use variables from command line and deploy_dir: ::

            domain={{ branch + '.' if not branch == 'master' else ''}}{{ project }}.klen.xxx

.. option:: template

   *Default*: ``db-postgres,django,zeta,uwsgi``

   Define deploy templates, if not exist :option:`-t`

.. option:: site_user

   *Default*: ``www-data``

   Define deploy user. From him runned processes and deployed templates.

.. option:: site_group

   *Default*: ``www-data``

   Define deploy group.

.. option:: port

   *Default*: ``80``

   Define deploy port, used for servers configuration.

.. option:: domain

   *Default*: ``example.com``

   Define deploy domain name, used for servers configuration.

.. option:: mode

   *Default*: ``dev``

   Im use it to switch django settings files ex.


Default makesite configuration
------------------------------

.. literalinclude:: ../makesite/makesite.ini
   :language: ini

.. _INI format: http://en.wikipedia.org/wiki/INI_file
