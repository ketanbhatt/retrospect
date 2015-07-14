#-*- coding:utf-8 -*-
import redis
import Xlib.display
import time


# Setting and clearing DB
DB = redis.Redis('localhost')
DB.flushall()

# init
disp = Xlib.display.Display()
root = disp.screen().root
root.change_attributes(event_mask=Xlib.X.PropertyChangeMask)

# property macros
NET_WM_NAME = disp.intern_atom('_NET_WM_NAME')
NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')
WM_CLASS = disp.intern_atom('WM_CLASS')


#retro = {};

# {
# 	"chrome": {
# 	"facebook": 2.34,
# 	"gmail": 2.12
# 	},
# 	"terminal": {
# 	"bla": 12.34
# 	}
# }


# {
# 	chrome: facebook,gmail
# 	facebook: 5
# 	gmail: 3
# }


# initialize current window
window_id = root.get_full_property(NET_ACTIVE_WINDOW, Xlib.X.AnyPropertyType).value[0]
window = disp.create_resource_object('window', window_id)
window.change_attributes(event_mask=Xlib.X.PropertyChangeMask)
		
window_name = window.get_full_property(NET_WM_NAME, 0).value
window_class = window.get_full_property(WM_CLASS, 0).value.split("\x00")[0]

prev_timestamp = time.time()

while True:

	event = disp.next_event()
	try:
		if event.atom == NET_ACTIVE_WINDOW or disp.get_atom_name(event.atom)=='WM_NAME':
			pass
		else:
			continue
	except:
		continue
	
	try:
		curr_timestamp = time.time()
		time_spent = int(curr_timestamp-prev_timestamp)

		if time_spent and window_name:
			prev_timestamp = curr_timestamp

			DB.sadd(window_class, window_name)
			DB.incrby(window_name, time_spent)

			print "class:",window_class,"name:",window_name,"time:",time_spent

		window_id = root.get_full_property(NET_ACTIVE_WINDOW, Xlib.X.AnyPropertyType).value[0]
		window = disp.create_resource_object('window', window_id)
		window.change_attributes(event_mask=Xlib.X.PropertyChangeMask)
		
		window_name = window.get_full_property(NET_WM_NAME, 0).value
		window_class = window.get_full_property(WM_CLASS, 0).value.split("\x00")[0]

			
	except :
		window_name = None
		window_class = None

