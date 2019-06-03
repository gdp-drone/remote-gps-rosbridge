import time
import roslibpy

# Created for debugging purposes
# remote gps computer publishes to localhost:9090
# use port forwarding to forward this traffic to <given-name>.serveo.net:80
# sh: ssh -R 80:localhost:9090 serveo.net

client = roslibpy.Ros(host='localhost', port=9090)

# Define MagneticField pub, sub, and msg transmitter
mag_listener = roslibpy.Topic(client, '/android/magnetic_field', 'sensor_msgs/MagneticField')
mag_talker = roslibpy.Topic(client, '/remote_mag', 'sensor_msgs/MagneticField')
mag_transmit = {}

def start_listening():
    mag_listener.subscriber(mag_recv)

def mag_recv(message):
    mag_transmit['magnetic_field'] = message['magnetic_field'] # TODO: unsure if subscript works
    print(mag_transmit)

def start_talking():
    while client.is_connected:
        mag_talker.publish(roslibpy.Message(mag_transmit))
        time.sleep(0.1)
    mag_talker.unadvertise()

client.on_ready(start_listening)
client.on_ready(start_talking)
client.run_forever()