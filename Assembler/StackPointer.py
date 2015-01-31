from utils.hex import Hex

class StackPointer (object):
    def __init__ (self):
        self.sp = Hex ('$1500')

    def inc (self):
        self.sp.inc ()
        return self.index ()

    def dec (self):
        self.sp.dec ()
        return self.index ()

    def index (self):
        return self.sp.__str__ ()


instance = StackPointer ()

def sp ():
    return instance
