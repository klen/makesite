<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta name="Format-Detection" content="telephone=yes" />
        <meta name="Viewport" content="width=device-width" />
        <title>Sitegen web</title>
        <link rel="home" href="/" />
        <link rel="stylesheet" type="text/css" href="/static/_main.css" />
        
    </head>

    <body>

        <h1>Sitegen sites:</h1>
        <ul class="sites">
            % counter = 0
            %for site in sites:
                % counter += 1
                <li class="sites_item">
                    <a class="sites_item_link" href="http://{{ site['domain'] }}:{{ site['port'] }}">{{ site['branch'] }}.{{ site['project'] }}</a>
                    %if site.get('revision'):
                        <span class="sites_item_revision">{{ site['revision'] }}</span>
                    %end
                    <br/>
                    <a class="toggle sites_item_info zeta" href="#" onclick="return { rel: '.sites_item_options_{{ counter }}' }">information</a>
                    <div class="sites_item_options sites_item_options_{{ counter }}">
                        %for k,v in site.items():
                            %if not 'password' in k:
                                <b>{{ k }}</b> = {{ v }}
                                <br/>
                            %end
                        %end
                    </div>
                </li>
            %end
        </ul>
        <script language="javascript" type="text/javascript" src="/static/_main.js"></script>
    </body>
</html>


