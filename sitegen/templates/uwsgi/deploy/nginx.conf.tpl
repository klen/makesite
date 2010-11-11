upstream %(branch)s.%(project_name)s.proxy {
    ip_hash;
    server unix://%(deploy_dir)s/uwsgi.sock;
}

server {

    listen      %(port)s;
    server_name %(branch)s.%(project_name)s;
    access_log  %(deploy_dir)s/logs/nginx_access.log;
    error_log   %(deploy_dir)s/logs/nginx_error.log;

    location / {
        uwsgi_pass  %(branch)s.%(project_name)s.proxy;
        include     uwsgi_params;
    }

    location /static/ {
        root %(deploy_dir)s;
    }

}
