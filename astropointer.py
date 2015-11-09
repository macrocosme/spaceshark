from flask import Flask, request, render_template, jsonify
from poynter_module import get_altaz, get_daltdaz
import requests
from os import system, fork
import sched, time
from subprocess import Popen
import random
import sys

s = sched.scheduler(time.time, time.sleep)
API_KEY = 'AIzaSyCY8AUysBMDz0d20GuIUaMbyJrr6pL-RYQ'
global PROCESSES
PROCESSES = []
DELAY = 60.

rand = random.random()

app = Flask(__name__)

class Objects:
    objects = ["Sun","Mercury","Venus","Moon","Mars","Jupiter","Saturn","Uranus","Neptune","Pluto"]
    processes = []

@app.route("/", methods=['GET', 'POST'])
def hello():
    return render_template('index.html', objects=Objects.objects)

@app.route("/_point")
def point():
    try:
        print "allo."
        print request.args.get('temp')

        if request.args.get('temp') == 'List':
            object = request.args.get('object_list')
        else:
            object = request.args.get('object_textbox')

        device_id = request.args.get('device_id')
        access_token = request.args.get('access_token')
        address = request.args.get('address')

        """
        # Retrieve address from google map
        response_get = requests.get('https://maps.googleapis.com/maps/api/geocode/json',
                        params={'address': address, 'key': API_KEY})
        location = response_get.json()['results'][0]['geometry']['location']

        # Convert coordinates (lng, lat) --> (alt, az)
        alt, az = get_altaz(object, location['lng'], location['lat'])
        # Send command to clouddy hardware for alt
        system('curl https://api.particle.io/v1/devices/'+str(device_id)+'/point_alt ' \
               '-d access_token='+str(access_token)+' ' \
               '-d "args='+str(alt)+'"')

        system('curl https://api.particle.io/v1/devices/'+str(device_id)+'/point_az ' \
               '-d access_token='+str(access_token)+' ' \
               '-d "args='+str(az)+'"')

        # Convert coordinates (lng, lat) --> (alt, az)
        d_alt, d_az = get_daltdaz(object, location['lng'], location['lat'])
        #  d_alt, d_az = d_alt*1000, d_az*1000
        #  print(d_alt, d_az)
        """

        if len(PROCESSES) > 0:
            for process in PROCESSES:
                print("process:", process)
                try:
                    os.kill(process, signal.SIGKILL)
                    print "after"
                except OSError, e:
                    print "error: ", e.errno

        #p = Popen(['python', 'astropointer.py', str(device_id), str(access_token), str(d_alt), str(d_az), str(DELAY)])
        p = Popen(['python', 'astropointer.py', str(device_id), str(access_token), str(1), str(1), str(DELAY)])

        PROCESSES.append(p.pid)
    except:
        print("oops.")

    return jsonify(response="ok")

def delta_update(device_id, access_token, d_alt, d_az, delay):
    print('delta_update...')
    print(rand)

    #time.sleep(delay)
    time.sleep(1.)
    delta_update(device_id, access_token, d_alt, d_az, delay)
    """
    # Send command to clouddy hardware for alt
    system('curl https://api.particle.io/v1/devices/'+str(device_id)+'/track_alt ' \
                                                                    '-d access_token='+str(access_token)+' ' \
                                                                    '-d "args='+str(d_alt)+'"')
    # Send command to clouddy hardware for az
    system('curl https://api.particle.io/v1/devices/'+str(device_id)+'/track_az ' \
                                                                    '-d access_token='+str(access_token)+' ' \
                                                                    '-d "args='+str(d_az)+'"')
    """
    #sc.enter(delay, 1, delta_update, (sc, device_id, access_token, d_alt, d_az,))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        app.run()
    else:
        print len(sys.argv)
        delta_update(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
