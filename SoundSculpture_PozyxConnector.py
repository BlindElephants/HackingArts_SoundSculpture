import paho.mqtt.client as mqtt
import ssl
import json
from pythonosc import osc_message_builder
from pythonosc import udp_client
import argparse

parser = argparse.ArgumentParser("\n\nPozyx MQTT Subscription -> OSC output script.\nThis script will subscribe to the MQTT feed on the Pozyx gateway machine (locally, via WiFi) and forward Pozyx related data over OSC to a targeted destination.\nThis script requires libraries: paho-mqtt, python-osc (Install via pip)\nCreated to run on Python 3 (created and tested with Python 3.6, 3.7).\n")
parser.add_argument("--pozyxGatewayAddr", default="192.168.0.22", help="This is the IP Address of the Pozyx Gateway machine on the LAN. [Default = \"192.168.0.22\"]")
parser.add_argument("--targetAddr", default="localhost", help="This is the IP Address of the target machine [Default = \"localhost\"]")
parser.add_argument("--targetPort", default=3333, help="This is the Port of the target machine [Default = 3333]")
parser.add_argument("--printDebug", action="store_true", help="If called, all debug info will be printed to terminal (Tag IDs and position data)")

args = parser.parse_args()
print("\nPozyx MQTT Subscription -> OSC output script.\nThis script will subscribe to the MQTT feed on the Pozyx gateway machine (locally, via WiFi) and forward Pozyx related data over OSC to a targeted destination.\nThis script requires libraries: paho.mqtt, python-osc\nCreated to run on Python 3 (created and tested with Python 3.6, 3.7).")
print("\nCreating OSC UDP Client to target:\t", args.targetAddr, " : ", args.targetPort)
oscSender = udp_client.SimpleUDPClient(args.targetAddr, args.targetPort)

host = args.pozyxGatewayAddr
port = 1883
topic = "tagsLive"

def on_connect(client, userdata, flags, rc):
    print(mqtt.connack_string(rc))

def on_message(client, userdata, msg):
    #print("Received msg")
    tag_data = json.loads(msg.payload.decode())

    try:
        network_id = tag_data["tagId"]
        position   = tag_data["data"]["coordinates"]
        if(args.printDebug):
            print("Received ID: {}, position {}".format(network_id, position))
        msg_builder = osc_message_builder.OscMessageBuilder("/position")
        msg_builder.add_arg(int(network_id), "i")
        msg_builder.add_arg(int(position["x"]), "i")
        msg_builder.add_arg(int(position["y"]), "i")
        oscSender.send(msg_builder.build())

    except KeyError:
        if(args.printDebug):
            print("No valid tag data: ", tag_data["tagId"])

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to topic")


print("\nCreating MQTT Client")
client = mqtt.Client()
print("Attempting to subscribe to MQTT Feed (Pozyx) on local WiFi at addr:\t", args.pozyxGatewayAddr)
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

client.connect(host, port=port)
client.subscribe(topic)

client.loop_forever()
