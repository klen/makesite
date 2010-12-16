import ConfigParser
import os

DEPLOYDIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))

def read_config(folder):
    path = os.path.join(folder, '.project.ini')
    parser = ConfigParser.RawConfigParser()
    parser.read(path)
    site = dict(parser.items('Main'))

    git_head = os.path.join(folder, 'source', '.git', 'HEAD')
    if os.path.exists(git_head):
        head = open(git_head).read().split()[1]
        site['revision'] = open(os.path.join(folder, 'source', '.git', head)).read()
    return site


def get_sites():
    config = read_config(DEPLOYDIR)
    sites = []
    for root, dirs, files in os.walk(config['sitesdir']):
        if '.project.ini' in files:
            sites.append(read_config(root))
    sites.sort(key=lambda x: x['project'])
    return sites
