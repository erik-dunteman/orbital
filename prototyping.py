import sys, getopt

'''
s : statespace	 	options: ["Tiny"]
m : mode			options: ["NoAstroids"]
c : controller	 	options: ["Self", "Agent"]
d : screen/display	options: ["ScreenOn", "ScreenOff"]
a : alpha			options: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
g : gamma			options: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
e : epsilon			options: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
l : session length	options: Any int
'''	

args = sys.argv[1:]

opts,args = getopt.getopt(args, 's:m:c:a:g:e:d:')

print(opts)
for opt in opts:
	print (opt[0],opt[1])