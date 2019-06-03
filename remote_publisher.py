import time
import roslibpy

# remote gps computer publishes to localhost:9090
# use port forwarding to forward this traffic to <given-name>.serveo.net:80
# sh: ssh -R 80:localhost:9090 serveo.net

client = roslibpy.Ros(host='localhost', port=9090)

# Define GPS pub, sub, and msg transmitter
gps_listener = roslibpy.Topic(client, '/android/fix', 'sensor_msgs/NavSatFix')
gps_talker = roslibpy.Topic(client, '/remote_gps', 'sensor_msgs/NavSatFix')
gps_transmit = {}

# Define IMU pub, sub, and msg transmitter
imu_listener = roslibpy.Topic(client, '/android/imu', 'sensor_msgs/Imu')
imu_talker = roslibpy.Topic(client, '/remote_imu', 'sensor_msgs/Imu')
imu_transmit = {}

# Define MagneticField pub, sub, and msg transmitter
mag_listener = roslibpy.Topic(client, '/android/magnetic_field', 'sensor_msgs/MagneticField')
mag_talker = roslibpy.Topic(client, '/remote_mag', 'sensor_msgs/MagneticField')
mag_transmit = {}

def start_listening():
    gps_listener.subscribe(gps_recv)
    imu_listener.subscribe(imu_recv)
    mag_listener.subscribe(mag_recv)

def gps_recv(message):
    gps_transmit['altitude'] = message['altitude']
    gps_transmit['longitude'] = message['longitude']
    gps_transmit['latitude'] = message['latitude']
    print(gps_transmit)

def imu_recv(message):
    imu_transmit['orientation'] = message['orientation'] # TODO: unsure if subscript works
    imu_transmit['angular_velocity'] = message['angular_velocity']
    imu_transmit['linear_acceleration'] = message['linear_acceleration']
    # print(imu_transmit)

def mag_recv(message):
    mag_transmit['magnetic_field'] = message['magnetic_field'] # TODO: unsure if subscript works
    # print(mag_transmit)

def start_talking():
    while client.is_connected:
        gps_talker.publish(roslibpy.Message(gps_transmit))
        imu_talker.publish(roslibpy.Message(imu_transmit))
        mag_talker.publish(roslibpy.Message(mag_transmit))
        time.sleep(0.1)

    gps_talker.unadvertise()
    imu_talker.unadvertise()
    mag_talker.unadvertise()

client.on_ready(start_listening)
client.on_ready(start_talking)
client.run_forever()