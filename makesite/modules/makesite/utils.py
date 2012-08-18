from os import path as op, listdir

from makesite.settings import CFGNAME
from makesite.core import MakesiteParser


DEPLOYDIR = op.dirname(op.dirname(__file__))


def read_config(folder):
    path = op.join(folder, CFGNAME)
    parser = MakesiteParser()
    parser.read(path)
    try:
        site = dict(parser.items('Main'))
    except Exception:
        return dict(project=None)

    git_head = op.join(folder, 'source', '.git', 'HEAD')
    if op.exists(git_head):
        try:
            head = open(git_head).read().split()[1]
            site['revision'] = open(
                op.join(folder, 'source', '.git', head)).read()
        except (IOError, IndexError):
            return site
    return site


def get_sites():
    config = read_config(DEPLOYDIR)
    sites = []
    root = config['makesite_home']
    for prj_name in listdir(root):
        prj = op.join(root, prj_name)
        if op.isdir(prj):
            for brn_name in listdir(prj):
                brn = op.join(prj, brn_name)
                if op.isdir(brn):
                    for f in listdir(brn):
                        if f == CFGNAME:
                            sites.append(read_config(brn))

    sites.sort(key=lambda x: x.get('project'))
    return sites
