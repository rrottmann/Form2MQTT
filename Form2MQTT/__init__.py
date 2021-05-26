import json
import os
import re

import paho.mqtt.client as mqtt
from flask import Flask, redirect, request, render_template

mqttc = mqtt.Client()

app = Flask(__name__)

for env_var in [
    'TITLE',
    'DESCRIPTION',
    'INSTRUCTION',
    'PLACEHOLDER',
    'SUBMIT_REGEXP',
    'SUBMIT_CAPTION',
    'FOOTER',
    'MQTT_BROKER',
    'MQTT_TOPIC',
    'SUCCESS_URL',
    'FAILED_URL',
]:
    env_var_value = os.environ.get(env_var, None)
    globals()[env_var] = env_var_value

if not TITLE:
    TITLE = "Form2MQTT"
if not DESCRIPTION:
    DESCRIPTION = "This is a sample form for submitting text to MQTT message broker."
if not INSTRUCTION:
    INSTRUCTION = "Enter text and submit it to MQTT:"
if not PLACEHOLDER:
    PLACEHOLDER = "URL"
if not SUBMIT_REGEXP:
    SUBMIT_REGEXP = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
if not SUBMIT_CAPTION:
    SUBMIT_CAPTION = "Submit to MQTT"
if not FOOTER:
    FOOTER = 'Form2MQTT by <a href="https://github.com/rrottmann">rrottmann</a>'
if not MQTT_BROKER:
    MQTT_BROKER = 'broker.hivemq.com'
if not MQTT_TOPIC:
    MQTT_TOPIC = 'Form2MQTT/test'
if not SUCCESS_URL:
    SUCCESS_URL = 'https://en.wikipedia.org/wiki/Success_(concept)'
if not FAILED_URL:
    FAILED_URL = 'https://en.wikipedia.org/wiki/Failure'


@app.route('/')
def index():
    d = {
        "title": TITLE,
        "description": DESCRIPTION,
        "instruction": INSTRUCTION,
        "placeholder": PLACEHOLDER,
        "submit_caption": SUBMIT_CAPTION,
        "footer": FOOTER,
    }

    return render_template('index.html', d=d)


@app.route('/api/submit', methods=['POST'])
def api_submit():
    data = request.form.get("input", None)
    if re.compile(SUBMIT_REGEXP).match(data):
        client = mqtt.Client('Form2MQTT')
        client.connect(host=MQTT_BROKER, port=1883, keepalive=60, bind_address="")
        message = {
            "data": data
        }
        client.publish(topic=MQTT_TOPIC, payload=json.dumps(message))
        return redirect(location=SUCCESS_URL)
    else:
        return redirect(location=FAILED_URL)


if __name__ == '__main__':
    app.run(debug=True)
