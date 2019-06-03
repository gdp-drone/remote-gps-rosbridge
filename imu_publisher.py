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
    imu_transmit['orientation'] = message['orientation'] # TODO: unsure if subscript works
    imu_transmit['angular_velocity'] = message['angular_velocity']
    imu_transmit['linear_acceleration'] = message['linear_acceleration']
    print(imu_transmit)

def start_talking():
    while client.is_connected:
        imu_talker.publish(roslibpy.Message(imu_transmit))
        time.sleep(0.1)
    imu_talker.unadvertise()

client.on_ready(start_listening)
client.on_ready(start_talking)
client.run_forever()