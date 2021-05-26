# Form2MQTT
This is a simple form that can be used to submit some text to a MQTT message broker.

## Features

* Basic regular expressions may be used to validate the input
* Most text can be customized via environment variables
* Redirect urls can be setup for success and failure.
* MQTT Topic can be set via environment variables. Default: `Form2MQTT/test`
* Public MQTT broker already setup for first tests
    * Access [MQTT Webclient](http://www.hivemq.com/demos/websocket-client/) and subscribe to `Form2MQTT/test`