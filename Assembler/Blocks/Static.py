import templates

from BlockFactory import bf
from ..LabelGenerator import lg
from ..utils.factor import long_delay_factor

class BaseBlock (object):
    regex = r'\.*'

    def __init__ (self, match):
        def safe_get_kwarg (kwarg):
            result = self.match.group (kwarg)
            if result == None:
                print 'RE parsing failed, kwarg not found.'
                print 'kwarg: ' + kwarg
                print 'group: ' + self.match.group ()
            return result

        self.match = match
        for kwarg in match.groupdict ():
            setattr (self, kwarg, safe_get_kwarg (kwarg))

    def assembly (self):
        return self.match.group ()



class AssemblyBlock (BaseBlock):
    regex = r'(?P<label>[^\s;]*)[\s]*(?P<op_code>([\w,\'\.\$#\+]* ?)*)[^;]*;?[\w]*(?P<comment>.*)'
    def __init__ (self, match):
        super (AssemblyBlock, self).__init__ (match)

        if not self.comment.isspace () and self.comment != '':
            self.comment = '; ' + self.comment

    def assembly (self):
        if not self.op_code and not self.label:
            return self.comment

        result = self.label
        result += ' ' * (12 - len (self.label))
        result += self.op_code
        result += ' ' * (32 - len (self.op_code))
        result += self.comment
        return result

class DelayBlock (BaseBlock):
    regex = r'delay[\s]*\((?P<delay>[0123456]?[012345])\)'

    def assembly (self):
        label = lg ().new_label ('delay')
        dic = {
            'label':label,
            'delay': str (int (self.delay) * 1000),
            'delay_human': self.delay,
        }
        raw = templates.delay_block ().format (**dic)
        return bf ().nested_block (raw).assembly ()

class LongDelayBlock (BaseBlock):
    regex = r'delay[\s]*\((?P<delay>[\d]*)\)'

    def assembly (self):
        iterations = long_delay_factor (self.delay)
        dic = {
            'delay_human': self.delay,
            'outer_num': str (iterations [0]),
            'inner_num': str (iterations [1] * 1000),
            'offset': str (iterations [2] * 1000 + 1),
            'label_1': lg ().new_label ('delay'),
            'label_2': lg ().new_label ('delay'),
            'label_3': lg ().new_label ('delay'),
            'label_4': lg ().new_label ('delay'),
        }
        raw = templates.long_delay_block ().format (**dic)
        return bf ().nested_block (raw).assembly ()

class StartBlock (BaseBlock):
    regex = r'start[\s]*\((?P<rom_start>\$?[\d]*)\)'

    def assembly (self):
        if not self.rom_start :
            self.rom_start = '$400'
        dic = {'rom_start': self.rom_start}
        raw = templates.start_block ().format (**dic)
        return bf ().nested_block (raw).assembly ()


class HeaderBlock (BaseBlock):
    regex = r'header[\s]*\((?P<header>[^\)]*)\)'

    def assembly (self):
        dic = {'header': self.header}
        raw = templates.header_block ().format (**dic)
        return bf ().nested_block (raw).assembly ()

class LEDBlock (BaseBlock):
    regex = r'LED[\s]*\((?P<state>(on|off))\)'

    def assembly (self):
        data = {'on':'#$01', 'off':'#$00'} [self.state]
        dic = {'state':data, 'state_human':self.state}
        raw = templates.LED_block ().format (**dic)
        return bf ().nested_block (raw).assembly ()

class InterruptBlock (BaseBlock):
    regex = r'interrupt[\s]*\([\s]*\)'

    def assembly (self):
        raw = templates.interrupt_block ()
        return bf ().nested_block (raw).assembly ()



def get_static_classes ():
    return [
        InterruptBlock,
        LEDBlock,
        DelayBlock,
        LongDelayBlock,
        StartBlock,
        HeaderBlock,
        AssemblyBlock,
    ]
