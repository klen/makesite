<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta name="Format-Detection" content="telephone=yes" />
        <meta name="Viewport" content="width=device-width" />
        <title>Makesite web</title>
        <link rel="home" href="/" />
        <link rel="stylesheet" type="text/css" href="/static/_main.css" />
        
    </head>

    <body>

        <div class="header">
            <h1 class="header_title">Makesite Sites Index</h1>
        </div>

        <div class="sites"><ul class="sites_content">
            <h1 class="sites_title">Summary</h1>
            <p>There are {{ len(sites) }} sites installed.</p>
            <p>
            %for site in sites:
                <a href="#{{ site['branch'] }}_{{ site['project'] }}">{{ site['branch'] }}.{{ site['project'] }}</a>
            %end
            </p>
            <h1 class="sites_title">Sites</h1>
            % counter = 0
            %for site in sites:
                % counter += 1
                <li class="sites_item" id="{{ site['branch'] }}_{{ site['project'] }}">
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
        </ul></div>
        <script language="javascript" type="text/javascript" src="/static/_main.js"></script>
    </body>
</html>


