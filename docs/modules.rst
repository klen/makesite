Modules
=======

Makesite includes the basic modules for easy creation of a standart python projects: django, wsgi project and makesite wsgi project for view list installed sites.


Django
------

Standart django project. Session saved in memcache. Use sqlite. ::

    makesite install -m django <project_name>


Wsgi
----

WSGI project sceleton. ::

    makesite install -m wsgi <project_name>


Static
------

Static site project sceleton. ::

    makesite install -m static <project_name>

Simple serve from nginx source directory.


Makesite
--------

Makesite web page with list of deployed on current server projects. ::

    makesite install -m makesite <project_name>
