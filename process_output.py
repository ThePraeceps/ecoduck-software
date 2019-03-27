import io
output_reader = open("first_byte.output", "r", encoding="utf-8")
lines = output_reader.readlines()
output_reader.close()
for idx, line in enumerate(lines):
	line = line.rstrip("\n\r")
	if(idx % 2 == 1):
		line=line.strip(" ")
		if(len(line) != 4):
			print(line)

	