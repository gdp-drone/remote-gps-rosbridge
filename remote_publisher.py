import time
import roslibpy

# remote gps computer publishes to localhost:9090
# use port forwarding to forward this traffic to <given-name>.serveo.net:80
# sh: ssh -R 80:localhost:9090 serveo.net

client = roslibpy.Ros(host='localhost', port=9090)
listener = roslibpy.Topic(client, '/android/fix', 'sensor_msgs/NavSatFix')
talker = roslibpy.Topic(client, '/remote_gps', 'sensor_msgs/NavSatFix')
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
        print('Publishing Local GPS coordinates to /remote_gps ...')
        time.sleep(1)

    talker.unadvertise()

client.on_ready(start_listening)
client.on_ready(start_talking)
client.run_forever()