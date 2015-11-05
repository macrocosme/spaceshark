from flask import Flask, request, render_template
from poynter_module import get_altaz, get_daltdaz
import requests
from os import system, fork
import sched, time

s = sched.scheduler(time.time, time.sleep)
API_KEY = 'AIzaSyCY8AUysBMDz0d20GuIUaMbyJrr6pL-RYQ'
global PROCESSES
PROCESSES = []
DELAY = 60

app = Flask(__name__)

class Objects:
    objects = ["Sun","Mercury","Venus","Moon","Mars","Jupiter","Saturn","Uranus","Neptune","Pluto"]
    processes = []

@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        try:
            if request.form['temp'] == 'List':
                object = request.form['object_list']
            else:
                object = request.form['object_textbox']

            device_id = request.form['device_id']
            access_token = request.form['access_token']
            address = request.form['address']


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
            if len(PROCESSES) > 0:
                os.kill(PROCESSES[0], signal.SIGKILL)
            pid = fork()
            PROCESSES.append(pid)
            s.enter(DELAY, 1, delta_update, (s, device_id, access_token, d_alt, d_az,))
            s.run()
            sys.exit()

        except:
            print("oops.")
    return render_template('index.html', objects=Objects.objects)

def delta_update(sc, device_id, access_token, d_alt, d_az):
    print('delta_update...')
    # Send command to clouddy hardware for alt
    system('curl https://api.particle.io/v1/devices/'+str(device_id)+'/track_alt ' \
                                                                    '-d access_token='+str(access_token)+' ' \
                                                                    '-d "args='+str(d_alt)+'"')
    # Send command to clouddy hardware for az
    system('curl https://api.particle.io/v1/devices/'+str(device_id)+'/track_az ' \
                                                                    '-d access_token='+str(access_token)+' ' \
                                                                    '-d "args='+str(d_az)+'"')
    sc.enter(DELAY, 1, delta_update, (sc, device_id, access_token, d_alt, d_az,))

if __name__ == "__main__":
    app.run()
