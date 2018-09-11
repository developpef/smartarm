from flask import Flask, jsonify, request, json
import os
import datetime
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

@app.route('/hello')
def hello():
    # returns details about environment
    environment_data = {
        'platformUrl': os.getenv('C8Y_BASEURL'),
        'mqttPlatformUrl': os.getenv('C8Y_BASEURL_MQTT'),
        'tenant': os.getenv('C8Y_BOOTSTRAP_TENANT'),
        'user': os.getenv('C8Y_BOOTSTRAP_USER'),
        'password': os.getenv('C8Y_BOOTSTRAP_PASSWORD'),
        'microserviceIsolation': os.getenv('C8Y_MICROSERVICE_ISOLATION')
    }
    return jsonify(environment_data)

@app.route('/kepware-agent', methods = ['POST'])
def translateKepwareMessage():
    kepMsg = request.json
    kep_id = kepMsg['values'][0]['id']
    servo_key = ''
    c8y_id = 0
    if('claw' in kep_id) :
        servo_key = 'claw_angle'
        c8y_id = 69213
    elif('left' in kep_id) :
        servo_key = 'left_angle'
        c8y_id = 68638
    elif('right' in kep_id) :
        servo_key = 'right_angle'
        c8y_id = 68641
    elif('middle' in kep_id) :
        servo_key = 'middle_angle'
        c8y_id = 69201
    
    c8y_measurement = {
        'time': datetime.datetime.fromtimestamp(kepMsg['timestamp']/1000).isoformat(),
        'source': {
            'id': str(c8y_id)
        },
        'type': 'smartarm_servos',
        'smartarm_servos': {
        servo_key : {
                'value': kepMsg['values'][0]['v']
            }
        }
    }

    url = 'https://pefgfi.cumulocity.com/measurement/measurements'#'http://localhost:1880/bin'#
    auth = HTTPBasicAuth('paul-emmanuel.faidherbe@gfi.fr', '!an12PEF')
    headers = {'Content-Type':'application/json'}
    response2 = requests.post(url, headers=headers, json=c8y_measurement, auth=auth, verify=False)

    resp = jsonify(c8y_measurement)
    resp.status_code = response2.status_code
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
