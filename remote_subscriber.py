import time
import roslibpy

# remote gps computer publishes (via port forwarding) to <given-name>.serveo.net:80
# remote_subscriber intercepts traffic and publishes to topic /mobile/fix

client = roslibpy.Ros(host='turbo.serveo.net', port=80)
listener = roslibpy.Topic(client, '/remote_gps', 'sensor_msgs/NavSatFix')
talker = roslibpy.Topic(client, '/mobile/fix', 'sensor_msgs/NavSatFix')
transmit = {}

def start_listening():
    listener.subscribe(receive_message)

def receive_message(message):
    transmit['altitude'] = message['altitude']
    transmit['longitude'] = message['longitude']
    transmit['latitude'] = message['latitude']
    print(transmit)

def start_talking():
    while client.is_connected:
        talker.publish(roslibpy.Message(transmit))
        print('Publishing Remote GPS coordinates to /mobile/fix ...')
        time.sleep(1)

    talker.unadvertise()

client.on_ready(start_listening)
client.on_ready(start_talking)
client.run_forever()