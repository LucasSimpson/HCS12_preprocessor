class BaseBlock (object):
    def __init__ (self, match):
        self.match = match

    def assembly (self):
        return self.match.group ()

    def safe_get_kwarg (self, kwarg):
        result = self.match.group (kwarg)
        if result == None:
            print 'RE parsing failed, kwarg not found.'
            print 'kwarg: ' + kwarg
            print 'group: ' + self.match.group ()
        return result
    
    @classmethod
    def get_regex (*args):
        return r'\.*'


class AssemblyBlock (BaseBlock):
    def __init__ (self, match):
        super (AssemblyBlock, self).__init__ (match)

        self.label = self.safe_get_kwarg ('label')
        self.op_code = self.safe_get_kwarg ('op_code')
        self.comment = self.safe_get_kwarg ('comment')

        if not self.comment.isspace () and self.comment != '':
            self.comment = '; ' + self.comment

    @classmethod
    def get_regex (*args):
        return r'(?P<label>[^\s;]*)[\s]*(?P<op_code>([\w,\'\.\$#\+]* ?)*)[^;]*;?[\w]*(?P<comment>.*)'

    def assembly (self):
        if not self.op_code and not self.label:
            return self.comment

        result = self.label
        result += ' ' * (12 - len (self.label))
        result += self.op_code
        result += ' ' * (32 - len (self.op_code))
        result += self.comment
        return result

class StackDirective (BaseBlock):
    pass


def get_static_classes ():
    return [
        AssemblyBlock,
    ]
