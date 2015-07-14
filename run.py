#-*- coding:utf-8 -*-
import Xlib.display
import time

disp = Xlib.display.Display()
root = disp.screen().root


NET_WM_NAME = disp.intern_atom('_NET_WM_NAME')
NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')
NET_WM_USER_TIME = disp.intern_atom('_NET_WM_USER_TIME')
WM_CLASS = disp.intern_atom('WM_CLASS')


# mydict = {}

prevWindow_name = None
prev = time.time()

while True:
	try:
		#print "I ran"
		
		window_id = root.get_full_property(NET_ACTIVE_WINDOW, Xlib.X.AnyPropertyType).value[0]
		window = disp.create_resource_object('window', window_id)
		window.change_attributes(event_mask=Xlib.X.StructureNotifyMask)
		
		window_name = window.get_full_property(NET_WM_NAME, 0).value
		window_class = window.get_full_property(WM_CLASS, 0).value


		if window_name != prevWindow_name:
			curr = time.time()
			print "Name: ", window_name, curr-prev #, " Type:", window_class, "Time: ", curr-prev
			
			prevWindow_name = window_name
			prevWindow_class = window_class
			prev = curr
			
		window_user_time = window.get_full_property(NET_WM_USER_TIME, 0).value[0]/1000.0

		
	except Xlib.error.XError:
		print "i fell"
		window_name = None
	
	#print "here1"
	event = disp.next_event()
	#print "here2"
	


	
