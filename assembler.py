from Assembler.Blocks.Nested import *



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


