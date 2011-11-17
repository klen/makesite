import sys
from ConfigParser import ConfigParser, DEFAULTSECT, MissingSectionHeaderError, ParsingError
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


class MakesiteConfigParser(ConfigParser):

    def read(self, filenames, replace=True):
        if isinstance(filenames, basestring):
            filenames = [filenames]
        read_ok = []
        for filename in filenames:
            try:
                fp = open(filename)
            except IOError:
                continue
            self._read(fp, filename, replace=replace)
            fp.close()
            read_ok.append(filename)
        return read_ok

    def _read(self, fp, fpname, replace=True):
        cursect = None                        # None, or a dictionary
        optname = None
        lineno = 0
        e = None                              # None, or an exception
        while True:
            line = fp.readline()
            if not line:
                break
            lineno = lineno + 1
            # comment or blank line?
            if line.strip() == '' or line[0] in '#;':
                continue
            if line.split(None, 1)[0].lower() == 'rem' and line[0] in "rR":
                # no leading whitespace
                continue
            # continuation line?
            if line[0].isspace() and cursect is not None and optname:
                value = line.strip()
                if value:
                    cursect[optname].append(value)
            # a section header or option header?
            else:
                # is it a section header?
                mo = self.SECTCRE.match(line)
                if mo:
                    sectname = mo.group('header')
                    if sectname in self._sections:
                        cursect = self._sections[sectname]
                    elif sectname == DEFAULTSECT:
                        cursect = self._defaults
                    else:
                        cursect = self._dict()
                        cursect['__name__'] = sectname
                        self._sections[sectname] = cursect
                    # So sections can't start with a continuation line
                    optname = None
                # no section header in the file?
                elif cursect is None:
                    raise MissingSectionHeaderError(fpname, lineno, line)
                # an option line?
                else:
                    mo = self._optcre.match(line)
                    if mo:
                        optname, vi, optval = mo.group('option', 'vi', 'value')
                        optname = self.optionxform(optname.rstrip())
                        if cursect.has_key(optname) and not replace:
                            continue
                        # This check is fine because the OPTCRE cannot
                        # match if it would set optval to None
                        if optval is not None:
                            if vi in ('=', ':') and ';' in optval:
                                # ';' is a comment delimiter only if it follows
                                # a spacing character
                                pos = optval.find(';')
                                if pos != -1 and optval[pos-1].isspace():
                                    optval = optval[:pos]
                            optval = optval.strip()
                            # allow empty values
                            if optval == '""':
                                optval = ''
                            cursect[optname] = [optval]
                        else:
                            # valueless option handling
                            cursect[optname] = optval
                    else:
                        # a non-fatal parsing error occurred.  set up the
                        # exception but keep going. the exception will be
                        # raised at the end of the file and will contain a
                        # list of all bogus lines
                        if not e:
                            e = ParsingError(fpname)
                        e.append(lineno, repr(line))
        # if any parsing errors occurred, raise an exception
        if e:
            raise e

        # join the multi-line values collected while reading
        all_sections = [self._defaults]
        all_sections.extend(self._sections.values())
        for options in all_sections:
            for name, val in options.items():
                if isinstance(val, list):
                    options[name] = '\n'.join(val)
