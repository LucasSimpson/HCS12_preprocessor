# HCS12_preprocessor
###### 2DP4


##Why?
Let's face it, assembly blows. Is it cool manipulating the data at a hardware level? Of course. Do we really need to define every absract command? No.

##How?
Load your pre-assembly code into intput.txt, run the python run.py file, and copy your output.txt file into CodeWarrior and witness the magic.

##Features
######All commands can be nested inside other commands' curly braces.

####start (hex=$400)
Sets up all the ROMstart and _entry and all the fluff you don't want to have to remember. Option paramter is the ROMstart location, defaults to $400.

####header (message)
Takes the single lined message and encloses it nicely in comment asterisks.

####delay (n)
Delays excecution for (n) milliseconds. Note that currently only delays up to 12800ms are supported.

####loop (n) {}
Anything enclosed inside the curly brackets will be looped n times. Note that currently only loops up to 12800 iterations are supported.


##Demo
input.txt currently has a small demo program, with the result in output.txt

##Notes
-Built in stack starts at $1500 and increments, so avoid using that memory