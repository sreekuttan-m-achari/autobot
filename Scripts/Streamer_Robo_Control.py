import base64
import cv2
import zmq
import serial

from Camera import Camera

from config import config_data

cnf_dat = config_data()

img_quality = cnf_dat["img_quality"]

print("Enabling Stream Connection...")

context = zmq.Context()
stream_socket = context.socket(zmq.PAIR)
stream_socket.connect('tcp://' + cnf_dat["controler_ip"] + ':' + cnf_dat["stream_port"])

print("Stream Connection Enabled..!")

print("Enabling Serial Connection...")

ser = serial.Serial(cnf_dat["serial_port"], cnf_dat["baudrate"])  # change ACM number as found from ls /dev/ttyUSB*
ser.baudrate = cnf_dat["baudrate"]

ser.write("PING")


def get_serial_data():
    # if (1):
    #     return "None"
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

print("Enabled Camera..!")

print("Waiting for Control Initialization..!")

msg = stream_socket.recv()
print msg

print("Control Initialized..!")

print("Starting Stream to " + cnf_dat["controler_ip"] + ':' + cnf_dat["stream_port"])

while True:

    try:

        frame = camera.current_frame.read()  # grab the current frame

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), img_quality]


        encoded, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)

        srl_data = get_serial_data()

        #if (srl_data):
        # print("Serial Data : " + srl_data)

        combined = jpg_as_text + "$$MSG$$" + srl_data

        stream_socket.send(combined)


    except KeyboardInterrupt:
        break

    command = stream_socket.recv()

    if (command):
        print("Command : " + command)
        if (command == "QUIT"):
            break
        ser.write(command)

print("Exited : ")
quit()
