import sys

filein = sys.argv[1]

fileout = sys.argv[2]

interval = sys.argv[3]

infile = open(filein, "r")
for line in infile:
	print (line)