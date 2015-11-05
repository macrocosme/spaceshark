from flask import Flask, request, render_template
from altaz import get_altaz
import requests
from os import system

API_KEY = 'AIzaSyCY8AUysBMDz0d20GuIUaMbyJrr6pL-RYQ'

app = Flask(__name__)

class Objects:
    objects = ["Sun","Mercury","Venus","Moon","Mars","Jupiter","Saturn","Uranus","Neptune","Pluto"]

@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        object = request.form['object']
        device_id = request.form['device_id']
        access_token = request.form['access_token']
        address = request.form['address']

        # Retrieve address from google map
        response_get = requests.get('https://maps.googleapis.com/maps/api/geocode/json',
                        params={'address': address, 'key': API_KEY})
        location = response_get.json()['results'][0]['geometry']['location']

        # Convert coordinates (lng, lat) --> (alt, az)
        alt, az = get_altaz(object, location.lng, location.lat)

        command = 'curl https://api.particle.io/v1/devices/'+str(device_id)+'/point_alt ' \
                                                                            '-d access_token='+str(access_token)+' ' \
                                                                            '-d "args='+angle+'"'
        system(command)

    return render_template('index.html', objects=Objects.objects)

if __name__ == "__main__":
    app.run()
