from Static import *
from ..utils.hex import Hex
from ..StackPointer import sp
from ..LabelGenerator import lg

class BlockFactory ():
    @classmethod
    def create (*args, **kwargs):
        result = []
        lines = kwargs ['raw'].split ('\n')
        index = 0
        while (True):
            try:
                lines [index]
            except IndexError:
                break

            if lines [index].find ('{') != -1:
                raw = ''
                depth = 0
                while (True):
                    try:
                        lines [index]
                    except IndexError:
                        print ("Missing right bracket  ('}')")
                        print 1/0 # crash
                    
                    raw += lines [index] + '\n'
                    if lines [index].find ('{') != -1:
                        depth += 1

                    if lines [index].find ('}') != -1:
                        depth -= 1

                    if depth == 0:
                        index += 1
                        break

                    index += 1

                command = raw [:raw.find ('{')]
                inside = raw [raw.find ('{'): raw.rfind ('}')+1]
                import re
                for class_ in get_nested_classes ():
                    match = re.search (class_.get_regex (), command)
                    if match:
                        result += [class_ (match, inside)]
                        
                        break
                                        
            else:
                if not lines [index].isspace () and lines [index] != '':
                    command = lines [index]
                    import re
                    for class_ in get_static_classes ():
                        match = re.search (class_.get_regex (), lines [index])
                        if match:
                            result += [class_ (match)]
                    
                index += 1
        return result

class NestedBlock (BaseBlock):
    def __init__ (self, match, inside_):
        super (NestedBlock, self).__init__ (match)
        pos_l = inside_.index ('{')
        pos_r = inside_.rindex ('}')
  
        self.inside = []
        self.inside += self.pre_blocks ()
        self.inside += BlockFactory.create (raw=inside_ [pos_l+1: pos_r])
        self.inside += self.post_blocks ()

    def pre_blocks (self):
        return []

    def post_blocks (self):
        return []

    def assembly (self):
        result = ''
        for block in self.inside:
            result += block.assembly () + '\n'
        return result

class LoopBlock (NestedBlock):
    def __init__ (self, match, inside):
        super (LoopBlock, self).__init__ (match, inside)

    @classmethod
    def get_regex (*args):
        return r'loop \((?P<num_loops>[\d]*)\)'

    def pre_blocks (self):
        num_loops = Hex (int (self.safe_get_kwarg ('num_loops')) - 1).__str__ ()
        self.label = lg ().new_label ('loop')

        raw = ''
        raw += '  LDAA #' + num_loops + ' ; Set up loop counter\n'
        raw += '  DECA ' + ' ; Decrement loop counter\n'
        raw += '  STAA ' + sp ().inc () + '\n'
        raw += self.label + '  NOP ;Loop start\n'

        return BlockFactory.create (raw=raw)


    def post_blocks (self):
        raw = ''
        raw += '  LDAA ' + sp ().index () + '\n'
        raw += '  BGE  ' + self.label + ' ; jump to start of loop\n'
        sp ().dec ()
        return BlockFactory.create (raw=raw)
        

    def assembly (self):
        return super (LoopBlock, self).assembly ()


def get_nested_classes ():
    return [
        LoopBlock,
        NestedBlock,
    ]
