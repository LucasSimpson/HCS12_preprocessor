class BlockFactory (object):
    def __init__ (self):
        pass

    def create (self, raw):
        result = []
        lines = raw.split ('\n')
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
                from Nested import get_nested_classes

                for class_ in get_nested_classes ():
                    match = re.search (class_.regex, command)
                    if match:
                        result += [class_ (match, inside)]
                        break
                                        
            else:
                if not lines [index].isspace () and lines [index] != '':

                    import re
                    from Static import get_static_classes

                    for class_ in get_static_classes ():
                        match = re.search (class_.regex, lines [index])
                        if match:
                            result += [class_ (match)]
                            break

                index += 1
        return result


    def parse_file (self, file_in, file_out=None):
        to_parse = '{\n'
        f = open (file_in, 'r')
        for line in f.readlines ():
            to_parse += line
        to_parse += '\n}'
        f.close ()

        head = self.create (to_parse)

        output = head [0].assembly ()

        if file_out:
            f = open (file_out, 'w')
            f.write (output)
            f.close ()

        #print output
        print 'Done'

    def nested_block (self, raw_):
        raw = '{\n' + raw_ + '\n}\n'
        return self.create (raw) [0]


instance = BlockFactory ()

def bf ():
    return instance