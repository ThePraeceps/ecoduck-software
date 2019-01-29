import os,signal,io
from subprocess import Popen, PIPE, check_output

binarystring = "\x21"

hex1 = b'\x00'

binarystring = binarystring.encode()

hex2 = b'\x07'



hex3 = binarystring + hex1 + hex2 + hex1 + hex1 + hex1 + hex1 + hex1

print(hex3)






