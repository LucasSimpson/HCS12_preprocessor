# HCS12_preprocessor
###### 2DP4


##Why?
Let's face it, assembly blows. Is it cool manipulating the data at a hardware level? Of course. Do we really need to define every absract command? No.

##Usage
Load your pre-assembly code into intput.txt, run the python run.py file, and copy your output.txt file into CodeWarrior and witness the magic.

Even if you don't want to use the any of the custom tags, it will still align your code so that every thing lines up nicely.

##Features

####start (hex=$400)
Sets up all the ROMstart and _entry and all the fluff you don't want to have to remember. Option paramter is the ROMstart location, defaults to $400.

####header (message)
Takes the single lined message and encloses it nicely in comment asterisks.

####LED (on/off)
Turns the LED on the esduino board either on or off, depending on the argument.

####delay (n)
Delays excecution for (n) milliseconds. Note that currently only delays up to 12800ms are supported.

####interrupt ()
Puts in the required interrupt vectors into your code.


####loop (n) {}
Anything enclosed inside the curly brackets will be looped n times. Note that currently only loops up to 12800 iterations are supported.

####loopinf {}
Anything inside the curly brackets will be looped forever.


##Demo
input.txt currently has a small demo program, with the result in output.txt

##Notes
- If there's a problem with whatever the code will print out 1 semi-informative line and crash. This shouldn't happen, hopefully. :)
- Due to hardware limitations and my laziness, loops have a max of 12800 iterations and delays go up too 2500s.
- Built in stack starts at $1500 and increments, so avoid using that memory