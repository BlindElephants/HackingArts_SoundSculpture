# First

## Connect to the SoundSculpture WIFI

- SSID: soundSculpture_WIFI
- PWD: soundSculpture_WIFI_2018

## Hardware Addresses

In the file __HardwareAddresses.txt__ is a list of addresses for communicating with the LED hardware, as well as the Pozyx positioning system.

Each line represents a single cube:
- Index (as written on the bottom of the cube)
- IP address to send messages to the LED hardware
- Identifier for the Pozyx positioning system

# SoundSculpture_PozyxConnector

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


# LED Hardware

## Functionality

- LED hardware receives OSC formatted messages via UDP connection.
- LED hardware operates with an interpolation system based on sent timing patterns paired with RGB or Brightness (greyscale) values.

### Available Messages / Formatting

Address attached to a given OSC message sent to the LED hardware is not used. Instead, the first argument on a given message indicates the function to call.

- __[2]__ Set All LEDs to a Brightness value (Greyscale)
  - Takes four additional arguments: Attack Time, Sustain Time, Release Time, Brightness Value [0-255]
- __[3]__ Set All LEDs to Color value
  - Takes four additional arguments: Attack Time, Sustain Time, Release Time, RGB Value
- __[4]__ Set LEDs to Values
  - Takes 47 additional arguments
    - Attack Time
    - Sustain Time
    - Release Time
    - Rotation Direction, [0, 1, 2] where 0 == no rotation
    - Rotation Rate
    - Arguments 6-47 are RGB values for each LED individually
  - This message has not been fully tested. No guarantees for behavior or functionality.
- __[5]__ Set Release Color to Brightness (Greyscale)
  - Takes one additional argument: brightness value [0-255]
  - This alters the color to release to after one of the messages above. I.e., instead of returning to black, we can set the hardware to go to another color after completing an ASR envelope.
- __[6]__ Set Release Color to RGB
  - Takes one additional argument: RGB value
  - This alters the color to release to after one of the messages above. I.e., instead of returning to black, we can set the hardware to go to another color after completing an ASR envelope.
- __[7]__ Set Release Color to Each LED Value
  - takes 42 arguments: each an RGB value per LED
  - This has not been fully tested. No guarantees for behavior or functionality.

#### RGB Values in messages

RGB values sent to the LED hardware are single INTEGER values.

The LED hardware converts these INT values to RGB values using the following definition:

``` c++
rgb_color intToRgb(int intVal)
{
    rgb_color outColor;
    outColor.red  = (intVal >> 16) & 0xFF;
    outColor.green= (intVal >> 8 ) & 0xFF;
    outColor.blue = (intVal) & 0xFF;
    return outColor;
}
```

In order to properly address the LEDs using RGB values, the inverse function will need to be written to convert RGB values to INTs.

C++ example:

``` c++
void RgbToInt(int red, int green, int blue)
{
    return (((red << 8)+green)<<8)+blue;
}
```

#### Example messages


The following message will set all LEDs in a given cube to white (255). The ASR (Attack, Sustain, Release) envelope timings are 250, 500, 250: fade to white over 250ms, hold for 500ms, fade out over 250ms:

```
/msg 2 250 500 250 255
```


To set all LEDs to purple rgb(255, 0, 255) with the same timings:

```
/msg 3 250 500 250 16711935
```
