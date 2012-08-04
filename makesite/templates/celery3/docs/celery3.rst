Celery3
-------

Template has controled celery process at project with supervisor.

Requirements
^^^^^^^^^^^^
Installed `Supervisor <http://pypi.python.org/pypi/supervisor/>`_.

Variables
^^^^^^^^^

.. option:: celery_params

    Define params for run celery (celery $celery_params)

    Default: worker -A celery.celery -B -l info

.. option:: celery_svconf

    Define path for make link on generated supervisor config

    Default: /etc/supervisor/conf.d/%(project)s.%(safe_branch)s.celery


Install operation
^^^^^^^^^^^^^^^^^

Copy link on generated `supervisor.conf` to supervisor directory.
Update supervisor loaded programs.


Update operation
^^^^^^^^^^^^^^^^

Restart the supervisor celery program.


Remove operation
^^^^^^^^^^^^^^^^

Remove link on celery supervisor conf. Restart supervisor.
