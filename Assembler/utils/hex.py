class Hex (object):
    # stores internally as INT
    def __init__ (self, num):
        self.num = num
        if isinstance (self.num, str):
            if self.num [0] == '$':
                self.num = int ('0x' + self.num.strip ('$'), 16)
            else:
                self.num = int (self.num)

    def __int__ (self):
        return self.num

    def __str__ (self):
        result = hex (self.num) [2:]
        if len (result) == 1 or len (result) == 3:
            result = '0' + result
        return '$' + result

    def inc (self):
        self.num += 1

    def dec (self):
        self.num -= 1

