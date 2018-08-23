PORT = '5555'
SERVER_ADDRESS = 'localhost'

CAMERA_PORT = 0
IS_RASPBERRY_PI = True

#RESOLUTION_W = 640 
#RESOLUTION_H = 480

RESOLUTION_W = 320 
RESOLUTION_H = 320

GPIO_SWITCH = 24


def config_data():
	cnf = {}
	cnf['serial_port'] = "/dev/ttyUSB0"
	cnf['stream_ip'] = "192.168.43.198"
	cnf['stream_port'] = "3333"
	cnf['controler_ip'] = "192.168.43.82"
	cnf['controller_port'] = "4444"
	cnf['baudrate'] = 115200
	cnf["img_quality"] = 80
	
	return cnf
