[program:%(branch)s.%(project_name)s]
command=/usr/bin/uwsgi
  --socket %(deploy_dir)s/uwsgi.sock
  --home %(deploy_dir)s/virtualenv
  --pythonpath %(deploy_dir)s
  --module deploy
  --processes 5
  --master
  --harakiri 120
  --max-requests 5000
directory=%(deploy_dir)s
environment=DJANGO_SETTINGS_MODULE='project.settings.dev'
user=%(user)s
autostart=true
autorestart=true
stdout_logfile=%(deploy_dir)s/logs/uwsgi.log
redirect_stderr=true
stopsignal=QUIT

