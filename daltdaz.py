from __future__ import print_function
from sys import argv, exit
import poynter_module as finger

if len(argv) == 2: 
	obj = argv[1]
	lon = 149.0660861
	lat = -31.27703889
	print("Assuming that we're in Sydney", lon, lat)
	
	a = finger.get_daltdaz(obj, lon, lat)
	print(a[0], a[1])
	
elif len(argv) == 4:
	obj, lon, lat, dt = argv[1], argv[2], argv[3]
	
	a = finger.get_daltdaz(obj, lon, lat)
	print(a[0], a[1])
	
elif len(argv) == 5:
	obj, lon, lat, dt = argv[1], argv[2], argv[3], argv[4]
	
	a = finger.get_daltdaz(obj, lon, lat, dt)
	print(a[0], a[1])
	
else: print("The proper syntax is \n >> python altaz.py ObjectName Longitude Latitude")
