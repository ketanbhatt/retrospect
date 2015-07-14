import redis

print "\n#### Time to Retrospect ####\n"

DB = redis.Redis('localhost')

myDB = {}
allKeys = DB.scan(0)[1]

for key in allKeys:
	if(DB.type(key) == 'set'):
		windows = DB.smembers(key)
		for window in windows:
			myDB[key] = {} 
			myDB[key][window] = DB.get(window)

for myClass in myDB:
	class_sum = 0
	for window in myDB[myClass]:
		print "----", myClass, "----" 
		class_sum += int(myDB[myClass][window])
		print window, ":", myDB[myClass][window]

	print "Total time in", myClass, ":", class_sum, "\n"


print "#### Half the Battle Won ####"