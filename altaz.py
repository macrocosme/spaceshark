from __future__ import print_function
from sys import argv, exit


################
## Insert whole bunch of desciptive shit here
################

from astropy.time import Time
	
def get_altaz(obj_name, ipt_lon, ipt_lat, t=Time.now()):
	
	#for html scrapping
	#from lxml import html
	#from bs4 import BeautifulSoup
	#to place requests
	import requests
	#import the javascript object notationjson
	import json

	import astropy.units as u
	from astropy.time import Time
	from astropy.coordinates import SkyCoord, EarthLocation, Angle, Latitude, Longitude

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
	ephem_site.lon, ephem_site.lat = str(obs_lon.deg), str(obs_lat.deg)
	ephem_site.date=ephem.Date(t.jd)


	##Get the object
	#Check for planet-hood.
	#if planet: resolve the individual planet with pyephem.
	#else if satellite or ISS (or TIANGONG) scrap the appropriate websites and return info
	#else query simbad

	############
	# Put in an auto-correct for kids
	############
	#just make it lower case for now

	obj_name=obj_name.lower()

	if obj_name in ["sun","mercury","venus","moon","mars","jupiter","saturn","uranus","neptune","pluto"]:
    
		if obj_name == "sun":       my_planet = ephem.Sun()
		elif obj_name == "mercury": my_planet = ephem.Mercury()
		elif obj_name == "venus":   my_planet = ephem.Venus()
		elif obj_name == "moon":    my_planet = ephem.Moon()
		elif obj_name == "mars":    my_planet = ephem.Mars()
		elif obj_name == "jupiter": my_planet = ephem.Jupiter()
		elif obj_name == "saturn":  my_planet = ephem.Saturn()
		elif obj_name == "uranus":  my_planet = ephem.Uranus()
		elif obj_name == "peptune": my_planet = ephem.Neptune()
		elif obj_name == "pluto":   my_planet = ephem.Pluto()
    
		my_planet.compute(ephem_site)
		az = my_planet.az * 180 / 3.1415926535
		alt = my_planet.alt * 180 / 3.1415926535
    #here coded for just ISS but for all satellites we should have similar setups, probably poll site
	elif (obj_name=="iss"):
		#try a request for the iss from the open notify site. Gives current json data
		page=requests.get("http://api.open-notify.org/iss-now.json")
		issdata=page.json()
		tstamp=issdata['timestamp'];isslat=issdata['iss_position']['latitude'];isslon=issdata['iss_position']['longitude']
		#there are issues with just this amount of data as you do not know the altitude of the object
		#here we fix it to 350 km 
		issheight=350*u.km 
		isslat=Latitude(isslat,unit=u.deg)
		isslon=Longitude(isslon,unit=u.deg)

		#there are issues however as this data does NOT contain the altitude so lets try scrapping the html 
		#the issue with fullissdata is that it contains information in NASA style units (M50 Cartesian & M50 Keplerian)
		page=requests.get("http://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/orbit/ISS/SVPOST.html")
		#fullissdata=html.fromstring(page.text)

		#there are also other satellites liseted in, issue is parsing the information as I do not know what each field contains
		#the issue here is that all sat data contains unknown units and uncertain which entries contain useful information
		page=requests.get("http://www.celestrak.com/NORAD/elements/stations.txt")
		allsatdata=page.text

		c=SkyCoord(isslon, isslat, issheight)
		my_target = FixedTarget(name='ISS', coord=c)
		az = my_site.altaz(t, my_target).az.deg
		alt = my_site.altaz(t, my_target).alt.deg				
	else:
		try: 
			q = simbad.query_object(obj_name)
			c = SkyCoord(q["RA"][0], q["DEC"][0], unit=(u.hourangle, u.deg))
			my_star = FixedTarget(name='my_star', coord=c)
        
			az = my_site.altaz(t, my_star).az.deg
			alt = my_site.altaz(t, my_star).alt.deg				
		except: 
			print("Couldn't find Object in Database")
			alt, az = 0, 0

	return alt, az

#####################################################################

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
