from Assembler.Blocks.BlockFactory import bf

block_factory = bf ()
block_factory.parse_file ('input.txt', 'output.txt') # if no output file is passed, will output to stdout