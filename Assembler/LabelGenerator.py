class LabelGenerator (object):
    def __init__ (self):
        self.buckets = {}

    def new_label (self, type_):
        try:
            self.buckets [type_]
        except KeyError:
            self.buckets [type_] = -1
        self.buckets [type_] += 1
        num = str (self.buckets [type_])
        if len (num) == 1:
            num = '0' + num

        return type_ + '_' + num


instance = LabelGenerator ()

def lg ():
    return instance
        
