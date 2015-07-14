#-*- coding:utf-8 -*-
import Xlib.display
import time

disp = Xlib.display.Display()
root = disp.screen().root


NET_WM_NAME = disp.intern_atom('_NET_WM_NAME')
NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')
WM_CLASS = disp.intern_atom('WM_CLASS')


retro = {};
# {
# 	"chrome": {
# 	"facebook": 2.34,
# 	"gmail": 2.12
# 	},
# 	"terminal": {
# 	"bla": 12.34
# 	}
# }

prev_window_name = None
prev_window_class = None
prev_timestamp = time.time()

while True:
	try:
		#print "I ran"
		
		window_id = root.get_full_property(NET_ACTIVE_WINDOW, Xlib.X.AnyPropertyType).value[0]
		window = disp.create_resource_object('window', window_id)
		window.change_attributes(event_mask=Xlib.X.StructureNotifyMask)
		
		window_name = window.get_full_property(NET_WM_NAME, 0).value
		window_class = window.get_full_property(WM_CLASS, 0).value.split("\x00")[0]


		if window_name != prev_window_name:
			curr_timestamp = time.time()
			time_spent = int(curr_timestamp-prev_timestamp)

			if window_class in retro:
				retro[window_class][window_name] += time_spent
			else:
				retro[window_class] = {}
				retro[window_class][window_name] = time_spent

			print retro
			
			prev_window_name = window_name
			prev_window_class = window_class
			prev_timestamp = curr_timestamp
			

		
	except Xlib.error.XError:
		print "i fell"
		window_name = None
	
	event = disp.next_event()
	


	
