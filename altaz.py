from __future__ import print_function
from sys import argv, exit


################
## Insert whole bunch of desciptive shit here
################

	
def get_altaz(obj_name, ipt_lon, ipt_lat):
	
	import astropy.units as u
	from astropy.time import Time
	from astropy.coordinates import SkyCoord, EarthLocation

	from astroplan import FixedTarget, Observer
	from astroquery.simbad import Simbad as simbad

	import ephem
	
	## Set up the observer
	obs_el = 100 * u.m
	loc = EarthLocation.from_geodetic(ipt_lon, ipt_lat, obs_el)
	my_site = Observer(name='My_Site', location=loc)

	obs_lat = my_site.location.latitude
	obs_lon = my_site.location.longitude

	#observer for pyephem
	ephem_site = ephem.Observer()
	ephem_site.lon, ephem_site.lat = str(obs_lat.deg), str(obs_lon.deg)


	##Get the object
	#Check for planet-hood.
	#if planet: resolve the individual planet with pyephem.
	#else query simbad


	############
	# Put in an auto-correct for kids
	############

	if obj_name in ["Sun","Mercury","Venus","Moon","Mars","Jupiter","Saturn","Uranus","Neptune","Pluto"]:
    
		if obj_name == "Sun":       my_planet = ephem.Sun()
		elif obj_name == "Mercury": my_planet = ephem.Mercury()
		elif obj_name == "Venus":   my_planet = ephem.Venus()
		elif obj_name == "Moon":    my_planet = ephem.Moon()
		elif obj_name == "Mars":    my_planet = ephem.Mars()
		elif obj_name == "Jupiter": my_planet = ephem.Jupiter()
		elif obj_name == "Saturn":  my_planet = ephem.Saturn()
		elif obj_name == "Uranus":  my_planet = ephem.Uranus()
		elif obj_name == "Neptune": my_planet = ephem.Neptune()
		elif obj_name == "Pluto":   my_planet = ephem.Pluto()
    
		my_planet.compute(ephem_site)
		az = my_planet.az * 180 / 3.1415926535
		alt = my_planet.alt * 180 / 3.1415926535
    
	else:
		try: 
			q = simbad.query_object(obj_name)
			c = SkyCoord(q["RA"][0], q["DEC"][0], unit=(u.hourangle, u.deg))
			my_star = FixedTarget(name='my_star', coord=c)
        
			az = my_site.altaz(Time.now(), my_star).az.deg
			alt = my_site.altaz(Time.now(), my_star).alt.deg				
		except: 
			print("Couldn't find Object in Database")
			alt, az = 0, 0

	return alt, az

#####################################################################

"""
if len(argv) == 2: 
	obj_name = argv[1]
	ipt_lon = 149.0660861
	ipt_lat = -31.27703889
	print("Assuming that we're in Sydney", ipt_lon, ipt_lat)
	
	a = get_altaz(obj_name, ipt_lon, ipt_lat)
	print(a[0], a[1])
	
elif len(argv) == 4:
	obj_name, ipt_lon, ipt_lat = argv[1], argv[2], argv[3]
	
	a = get_altaz(obj_name, ipt_lon, ipt_lat)
	print(a[0], a[1])
	
else: print("The proper syntax is \n >> python altaz.py ObjectName Longitude Latitude")
"""
