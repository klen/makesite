import re


class TemplateException(Exception):
    pass


class Template(object):
    tag_re = re.compile('\{\{([^}]+)\}\}', re.M)

    def __init__(self, content=None, filename=None, context=None):
        self.content = content
        self.filename = filename
        self.context = context or dict()

        if not self.content and not self.filename:
            raise TemplateException("Not found content or filename.")

    def __open__(self, mode='r'):
        try:
            return open(self.filename, mode)
        except IOError:
            raise TemplateException("File read error: '%s" % self.filename)

    def parse_file(self, **ctx):
        context = ctx or self.context
        with self.__open__() as f:
            src = self.sub(f.read(), **context)
        with self.__open__('w') as f:
            f.write(src)
        return True

    def __call__(self, **ctx):
        if not self.content:
            self.content = self.__open__().read()
        return self.sub(self.content, **ctx)

    @classmethod
    def sub(cls, content, **ctx):

        def replace(obj):
            code = obj.group(1)
            try:
                return str(eval(code, {}, ctx))
            except Exception, e:
                raise TemplateException(str(e))

        return cls.tag_re.sub(replace, content)
