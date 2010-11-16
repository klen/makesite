import re


class TemplateException(Exception):
    pass

class Template( object ):
    tag_re = re.compile( '\{\{([^}]+)\}\}', re.M )

    def __init__( self, content=None, filename=None ):
        self.content = content
        self.filename = filename

        if not self.content and not self.filename:
            raise TemplateException( "Not found content or filename." )

    def __read__( self ):
        try:
            f = open( self.filename )
            return f.read()
        except IOError:
            raise TemplateException( "File read error: '%s" % self.filename )

    def __call__( self, **ctx ):
        if not self.content:
            self.content = self.__read__()

        return self.sub( self.content, **ctx )

    @classmethod
    def sub( cls, content, **ctx ):

        def replace( obj ):
            code = obj.group(1)
            try:
                return str(eval( code, {}, ctx ))
            except ( NameError, SyntaxError ):
                print 'Template error: %s' % code
                return ''
            except Exception, e:
                raise TemplateException(str(e))

        return cls.tag_re.sub( replace, content )
