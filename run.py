#-*- coding:utf-8 -*-
import Xlib.display
import time

disp = Xlib.display.Display()
root = disp.screen().root
root.change_attributes(event_mask=Xlib.X.FocusChangeMask)

NET_WM_NAME = 345 #disp.intern_atom('_NET_WM_NAME')
NET_ACTIVE_WINDOW = 337 #disp.intern_atom('_NET_ACTIVE_WINDOW')
WINDOW_IS = 67

prevWindow_name = ""
prevWindow_is = ""
timeStart = None


mydict = {}

while True:
	
	try:
		window_id = root.get_full_property(NET_ACTIVE_WINDOW, Xlib.X.AnyPropertyType).value[0]
		window = disp.create_resource_object('window', window_id)
		window.change_attributes(event_mask=Xlib.X.PropertyChangeMask)
		
		window_name = window.get_full_property(NET_WM_NAME, 0).value
		window_is = window.get_full_property(WINDOW_IS, 0).value
	
		if window_name != prevWindow_name or window_is != prevWindow_is:
			if not timeStart:
				timeStart = time.time()
			prevWindow_name = window_name
			prevWindow_is = window_is
			
			timeEnd = time.time()
			timeDiff = timeEnd-timeStart
			timeStart = timeEnd
			
			timeDiff = str(timeDiff)
			timeDiff = float(timeDiff[:timeDiff.find('.')+3])

			print timeDiff

			if window_name not in mydict.keys():
				mydict[window_name] = [window_name,window_is,timeDiff]
			else:
				mydict[window_name][2] += timeDiff

			for key in mydict.keys():
				print mydict[key]

			# print "%.2f" % timeDiff
			# print window_name
			# print window_is
			
	except Xlib.error.XError:
		window_name = None
	

	event = disp.next_event()
	
