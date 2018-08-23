import base64
import cv2
import zmq
import serial

from Camera import Camera

from config import config_data

cnf_dat = config_data()

print("Enabling Stream Connection...")

context = zmq.Context()
stream_socket = context.socket(zmq.PAIR)
stream_socket.connect('tcp://' + cnf_dat["controler_ip"] + ':' + cnf_dat["stream_port"])

print("Stream Connection Enabled..!")

print("Enabling Serial Connection...")

ser = serial.Serial(cnf_dat["serial_port"], 9600)  # change ACM number as found from ls /dev/ttyUSB*
ser.baudrate = 9600

ser.write("PING")


def get_serial_data():
    read_ser = ser.readline()
    if (read_ser):
        return read_ser
    else:
        return "None"


srl_data = get_serial_data()

if (srl_data):
    print("Serial Connection Enabled..!")

print("Enabling Camera...")

camera = Camera()
camera.start_capture()

print("Enabled Camera!")

print("Starting Stream to " + cnf_dat["controler_ip"] + ':' + cnf_dat["stream_port"])

while True:

    try:
        # srl_data = get_serial_data()

        # if(srl_data):
        #     print("Serial Data : " +srl_data )

        frame = camera.current_frame.read()  # grab the current frame 

        encoded, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)

        combained = jpg_as_text + "$$MSG$$" + srl_data

        stream_socket.send(combained)

        command = stream_socket.recv_string()
        print("Command : " + command)
        ser.write(command)

    except KeyboardInterrupt:
        camera.release()
        break
