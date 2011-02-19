import ConfigParser
import os

from makesite import INI_FILENAME


DEPLOYDIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))


def read_config(folder):
    path = os.path.join(folder, INI_FILENAME)
    parser = ConfigParser.RawConfigParser()
    parser.read(path)
    try:
        site = dict(parser.items('Main'))
    except Exception:
        return dict(project=None)

    git_head = os.path.join(folder, 'source', '.git', 'HEAD')
    if os.path.exists(git_head):
        head = open(git_head).read().split()[1]
        site['revision'] = open(os.path.join(folder, 'source', '.git', head)).read()
    return site


def get_sites():
    config = read_config(DEPLOYDIR)
    sites = []
    root = config['sites_home']
    for prj_name in os.listdir(root):
        prj = os.path.join(root, prj_name)
        if os.path.isdir(prj):
            for brn_name in os.listdir(prj):
                brn = os.path.join(prj, brn_name)
                if os.path.isdir(brn):
                    for f in os.listdir(brn):
                        if f == INI_FILENAME:
                            sites.append(read_config(brn))

    sites.sort(key=lambda x: x['project'])
    return sites
