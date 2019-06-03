import time
import roslibpy

# Created for debugging purposes
# remote gps computer publishes to localhost:9090
# use port forwarding to forward this traffic to <given-name>.serveo.net:80
# sh: ssh -R 80:localhost:9090 serveo.net

client = roslibpy.Ros(host='localhost', port=9090)

# Define IMU pub, sub, and msg transmitter
imu_listener = roslibpy.Topic(client, '/android/imu', 'sensor_msgs/Imu')
imu_talker = roslibpy.Topic(client, '/remote_imu', 'sensor_msgs/Imu')
imu_transmit = {}

def start_listening():
    imu_listener.subscribe(imu_recv)

def imu_recv(message):
    imu_transmit['orientation']['x'] = message['orientation']['x']
    imu_transmit['orientation']['y'] = message['orientation']['y']
    imu_transmit['orientation']['z'] = message['orientation']['z']
    imu_transmit['orientation']['w'] = message['orientation']['w']

    imu_transmit['angular_velocity']['x'] = message['angular_velocity']['x']
    imu_transmit['angular_velocity']['y'] = message['angular_velocity']['y']
    imu_transmit['angular_velocity']['z'] = message['angular_velocity']['z']

    imu_transmit['linear_acceleration']['x'] = message['linear_acceleration']['x']
    imu_transmit['linear_acceleration']['y'] = message['linear_acceleration']['y']
    imu_transmit['linear_acceleration']['z'] = message['linear_acceleration']['z']
    print(imu_transmit)

def start_talking():
    while client.is_connected:
        imu_talker.publish(roslibpy.Message(imu_transmit))
        time.sleep(0.1)
    imu_talker.unadvertise()

client.on_ready(start_listening)
client.on_ready(start_talking)
client.run_forever()