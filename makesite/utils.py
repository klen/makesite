import sys
from argparse import ArgumentParser

from makesite import settings, core


actions = dict()


class MakesiteArgsParser(ArgumentParser):

    def error(self, message):
        self.print_usage(sys.stderr)
        print "\nInstalled templates:"
        print " ".join(core.get_base_templates())
        print "\nInstalled modules:"
        print " ".join(core.get_base_modules())
        print
        self.exit(2, '%s: error: %s\n' % (self.prog, message))


def action(*arguments):
    parser = MakesiteArgsParser(description = "'Makesite' easy create base project structure.")
    parser.add_argument('-v', '--version', action='version', version=settings.VERSION, help='Show makesite version')
    for (args, kwargs) in arguments:
        parser.add_argument(*args, **kwargs)

    def _inner(func):
        name = func.__name__
        parser.description = func.__doc__

        def _wrapper(args=None):
            args = parser.parse_args(args)
            return func(args)

        actions[name] = _wrapper
        if name != 'main':
            parser.prog = " ".join((parser.prog, name))
        return _wrapper

    return _inner


class OrderedSet(list):

    def __init__(self, sequence):
        result = []
        for o in sequence:
            if not o in result:
                result.append(o)
        super(OrderedSet, self).__init__(result)
