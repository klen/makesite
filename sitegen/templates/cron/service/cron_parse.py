#!/usr/bin/env python

CRON_OUTPUTFILE = '{{ cron_outputfile }}'
CRON_PROJECTFILE = '{{ cron_projectfile }}'
CRON_RUNSCRIPT = 'sudo -u {{ user }} sh {{ deploy_dir }}/service/cron_run.sh'


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
        print "Parse project crontab file: '%s'." % CRON_PROJECTFILE
        output = open(CRON_OUTPUTFILE, 'w')
    except IOError:
        return

    print "Write to crontab file: '%s'" % CRON_OUTPUTFILE
    output.writelines(list(parse_crontab(content)))


if __name__ == '__main__':
    main()
