import templates
from Static import BaseBlock
from BlockFactory import bf
from ..utils.hex import Hex
from ..utils.factor import factor
from ..StackPointer import sp
from ..LabelGenerator import lg

class NestedBlock (BaseBlock):
    def __init__ (self, match, inside_):
        super (NestedBlock, self).__init__ (match)
        pos_l = inside_.index ('{')
        pos_r = inside_.rindex ('}')

        self.inside_raw = inside_ [pos_l+1: pos_r]
        self.inside = self.compile_inside ()

    def compile_inside (self):
        inside = self.pre_blocks ()
        inside += bf ().create (self.inside_raw)
        inside += self.post_blocks ()
        return inside

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
    regex = r'loop[\s]*\((?P<num_loops>(1(2[01234567]|[01][\d])|[\d]{1,2}))\)'

    def pre_blocks (self):
        sp ().inc ()

        num_loops = Hex (int (self.num_loops))
        self.label = lg ().new_label ('loop')
        dic = {
            'num_loops': num_loops, 
            'num_loops_human': int (num_loops),
            'label': self.label, 
            'sp': sp ().index (),
        }

        raw = templates.loop_pre_block ().format (**dic)
        return bf ().create (raw)

    def post_blocks (self):
        dic = {'sp':sp().index (), 'label':self.label}
        sp ().dec ()

        raw = templates.loop_post_block ().format (**dic)
        return bf ().create (raw)
        
    def assembly (self):
        return super (LoopBlock, self).assembly ()

class LongLoopBlock (NestedBlock):
    regex = r'loop[\s]*\((?P<num_loops>[\d]*)\)'

    def compile_inside (self):
        if int (self.num_loops) > 12800:
            print 'WARNING: program will not excecute as desired.'
            print 'Too many loops, cannot loop more then 12800 times'

        iterations = factor (self.num_loops, 128)

        dic = {
            'inside_raw': self.inside_raw,
            'outer_num': str (iterations [0]),
            'inner_num': str (iterations [1]),
            'offset': str (iterations [2]),
        }

        raw = templates.long_loop_block ().format (**dic)
        return bf ().create (raw)

class LoopInfBlock (NestedBlock):
    regex = r'loopinf'

    def pre_blocks (self):
        self.label = lg ().new_label ('inf')
        dic = {'label': self.label}
        raw = templates.loop_inf_pre_block ().format (**dic)
        return bf ().create (raw)

    def post_blocks (self):
        dic = {'label': self.label}
        raw = templates.loop_inf_post_block ().format (**dic)
        return bf ().create (raw)

def get_nested_classes ():
    return [
        LoopBlock,
        LongLoopBlock,
        LoopInfBlock,
        NestedBlock,
    ]
