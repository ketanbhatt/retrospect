import redis

# Colors
ESC_SEQ = "\x1b["
COL_RESET = ESC_SEQ+"39;49;00m"
COL_RED = ESC_SEQ+"31;01m"
COL_GREEN = ESC_SEQ+"32;01m"
COL_YELLOW = ESC_SEQ+"33;01m"
COL_BLUE = ESC_SEQ+"34;01m"
COL_MAGENTA = ESC_SEQ+"35;01m"
COL_CYAN = ESC_SEQ+"36;01m"

DB = redis.Redis('localhost')
myDB = {}
allKeys = DB.scan(0)[1]

import redis
print COL_GREEN+"##############################"
print "##### Time to Retrospect #####"
print "##############################"+COL_RESET

# Taking data from redis and arranging nicely in a dictionary
for key in allKeys:
	if(DB.type(key) == 'set'):
		windows = DB.smembers(key)
		myDB[key] = {} 
		for window in windows:
			myDB[key][window] = DB.get(window)

# Adding and printing stuff
for myClass in myDB:
	class_sum = 0
	print "----", myClass, "----" 
	for window in myDB[myClass]:
		class_sum += int(myDB[myClass][window])
		print window, ":", myDB[myClass][window]

	print "Total time in", myClass, ":", class_sum, "\n"


print COL_GREEN+"#################################"
print "#### Half Your Battle is Won ####"
print "#################################"+COL_RESET