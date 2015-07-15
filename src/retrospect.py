#!/usr/bin/env python
import time
import redis


# Colors
ESC_SEQ = "\x1b["
COL_RESET = ESC_SEQ+"39;49;00m"
COL_CYAN = ESC_SEQ+"36;01m"
COL_BLUE = ESC_SEQ+"34;01m"
COL_GREEN = ESC_SEQ+"32;01m"
COL_YELLOW = ESC_SEQ+"33;01m"
COL_WHITE = ESC_SEQ+"37;01m"
COL_RED = ESC_SEQ+"31;01m"


# init
DB = redis.Redis('localhost')
count = 1
uptime = 0

def timeformat(seconds):
	return time.strftime("%H:%M:%S", time.gmtime(seconds))


# banner
print COL_CYAN+"################################"
print "###### Time to Retrospect ######"
print "################################"+COL_RESET
print

# prepare from DB
myDB = {}
allKeys = []
cursor = 0
while True:
	allKeys.extend(DB.scan(cursor)[1])
	cursor = DB.scan(cursor)[0]
	if cursor == 0:
		break

# DB
# {
# 	chrome: facebook,gmail
# 	facebook: 5
# 	gmail: 3
# }

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
	print COL_BLUE+"----", myClass, "----" +COL_RESET
	for window in myDB[myClass]:
		class_sum += int(myDB[myClass][window])
		myTime = timeformat(float(myDB[myClass][window]))
		print COL_GREEN+str(count)+".",window, ":", COL_YELLOW+myTime+COL_RESET+COL_RESET
		count += 1
	print COL_WHITE+"Total time in", myClass, ":", timeformat(class_sum)+COL_RESET+"\n"
	uptime += class_sum

print COL_RED+"Total uptime:", timeformat(uptime)+COL_RESET
print

# banner end
print COL_CYAN+"#################################"
print "#### Half Your Battle is Won ####"
print "#################################"+COL_RESET

