Introduction
============

Welcome to **Makesite**! I really hope this system will be helpfull for you.


Ideology
--------

It automates the configuration of your server. Makesite does not do except copy the structure of selected templates into your project folder with the specified variables and run the generated scripts. It just sets shell scripts patterns and programm config files.


Project deploy process
----------------------

When deploying ``makesite`` make operation in next order.

#. Parse options from :doc:`command line and config files <configuration>`;

#. Copy :term:`base` template to ``deploy dir``.

#. Load project source;

#. Parse makesite options from source if exists;

#. Copy all project templates in ``deploy dir``;

#. Run templates service install files.
