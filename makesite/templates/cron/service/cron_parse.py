#!/usr/bin/env python

CRON_OUTPUTFILE = '{{ cron_outputfile }}'
CRON_PROJECTFILE = '{{ cron_projectfile }}'
CRON_RUNSCRIPT = '{{ site_user }} sh {{ project_servicedir }}/virtualenv_run.sh'


def parse_crontab( content ):
    for line in content:
        if line.startswith( '#' ):
            continue

        parts = line.split()
        if parts < 6:
            raise Exception( "Crontab format invalid '%s'" % line )
        time = ' '.join(parts[:5])
        command = CRON_RUNSCRIPT + ' ' + ' '.join(parts[5:])
        yield ' '.join( [ time, command ] )


def main():
    try:
        content = open(CRON_PROJECTFILE).readlines()
        output = open(CRON_OUTPUTFILE, 'w')
        print "  * Parse project crontab file: '%s'." % CRON_PROJECTFILE
    except IOError:
        return

    content = '\n'.join(list(parse_crontab(content)))
    print "  * Write to crontab file: '%s'" % CRON_OUTPUTFILE
    output.write(content)


if __name__ == '__main__':
    main()
