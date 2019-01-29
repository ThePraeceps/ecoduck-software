binarystring = ""

RGUI = False;
RALT = False;
RSHIFT = True;
RCTRL = False;
LGUI = False;
LALT = True;
LSHIFT = False;
LCTRL = False;



def bitwise(modifier, binarystring):
	if modifier == True:
		binarystring = binarystring + "1"
	else:
		binarystring = binarystring + "0"
	return binarystring

binarystring = bitwise(RGUI,binarystring) + bitwise(RALT,binarystring) + bitwise(RSHIFT, binarystring) + bitwise(RCTRL, binarystring) + bitwise(LGUI, binarystring) + bitwise(LALT, binarystring) + bitwise(LSHIFT, binarystring) + bitwise(LCTRL, binarystring) 

binarystring = hex(int(binarystring,2))

a,b,c,d = binarystring

binarystring = "\\" + b + c + d
	

print(binarystring)
print(a)
print(b)
print(c)
print(d)


