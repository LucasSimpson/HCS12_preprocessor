from Assembler.Blocks.BlockFactory import bf


"""
to_parse = '{\n'
for line in open ('input.txt', 'r').readlines ():
    to_parse += line
to_parse += '\n}'


head = BlockFactory.create (raw=to_parse)


output = head [0].assembly ()

f = open ('output.txt', 'w')
f.write (output)
f.close ()
print output
print 'Done'


"""

block_factory = bf ()
block_factory.parse_file ('input.txt', 'output.txt')