import ConfigParser
import os

DEPLOYDIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))

def read_config(folder):
    path = os.path.join(folder, '.project.ini')
    parser = ConfigParser.RawConfigParser()
    parser.read(path)
    return dict(parser.items('Main'))

def get_sites():
    config = read_config(DEPLOYDIR)
    sites = []
    for root, dirs, files in os.walk(config['sitesdir']):
        if '.project.ini' in files:
            sites.append(read_config(root))
    sites.sort(key=lambda x: x['project'])
    return sites
