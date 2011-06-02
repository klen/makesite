" Get base dirs and parse makesite.ini if exists. "
import os.path


PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DEVZONE_ROOT = os.path.dirname(PROJECT_ROOT)
CONFIG_FILE = os.path.join(DEVZONE_ROOT, 'makesite.ini')


# Load configs from project ini file (sitegen generated)
if os.path.exists(CONFIG_FILE):
    import ConfigParser
    parser = ConfigParser.RawConfigParser()
    parser.read(CONFIG_FILE)
    V = dict(parser.items('Main'))

else:
    V = dict()


PROJECT_NAME = "%s.%s" % (V.get('project', 'undefined'), V.get('branch', 'master'))
