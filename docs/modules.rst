Modules
=======

Makesite includes the basic modules for easy creation of a standart python projects: django, wsgi project and makesite wsgi project for view list installed sites.


Django
------

Standart django project. Session saved in memcache. Use sqlite. ::

    makesite -m django <project_name>


Dummy
-----

Dummy project sceleton. ::

    makesite -m dummy <project_name>

Wsgi
----

WSGI project sceleton. ::

    makesite -m wsgi <project_name>

Makesite
--------

Makesite web page with list of deployed on current server projects. ::

    makesite -m makesite <project_name>
