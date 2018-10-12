# Sound Sculpture Pozyx MQTT->OSC

This script will subscribe to the MQTT feed on the Pozyx gateway machine (locally, via WiFi) and forward Pozyx related data over OSC to a target destination (i.e., your app)

## Dependencies

- paho-mqtt
- python-osc

## Tested

Created to run on Python 3. This script has been tested with Python versions 3.6, 3.7.

## Functionality

This script forwards messages received from the Pozyx Gateway (MQTT Protocol) to a target destination (your app) via OSC formatted messages over UDP. The OSC sender, by default, targets __localhost:3333__.

Formatting for the OSC messages:

```
/position TagIndex Position_X Position_Y
```

Where ```/position``` is the address for the message, all following arguments are INTs.

The minimum and maximum values for position data (both X and Y) is determined by the Pozyx calibration pre-runtime, and is dependant on each specific setup. This data will be available once the system is set up and calibrated.

## Arguments

Arguments can be provided to the script to point connections in the correct direction.

```--pozyxGatewayAddr``` accepts an IP address. This is the IP address of the Pozyx Gateway on the local network. Defaults to "192.168.0.22"

```--targetAddr``` accepts an IP address. This is the IP address of the application that needs Pozyx position data. By default, this is "localhost"

```--targetPort``` accepts an INT as argument. This is the port for the OSC sender to the target application.

```--printDebug``` if called, this script will print all positional data as it is received.
