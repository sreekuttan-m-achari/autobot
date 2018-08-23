from config import config_data
import Tkinter as tk 
import zmq

cnf_dat = config_data() 

server_address = cnf_dat["stream_ip"] 
port = cnf_dat["stream_port"] 


print("Connecting to "+server_address+" at "+port+"...")

context = zmq.Context()
command_socket = context.socket(zmq.PUB)
command_socket.connect('tcp://' + server_address + ':' + port)

print("Connected to "+server_address+" at "+port)


def robot_status(command):

    print("Sending Command : "+command) 
    command_socket.send(command)

def key_input(event):
    print "Key:" , event.char
    key_pressed = event.char
    ST = 0.05 
   
    if key_pressed.lower() == 'w':
        mov_fwd(event)
    elif key_pressed.lower() == 's':
        mov_fwd(event)
    elif key_pressed.lower() == 'a':
        #trn_right(event)
        pvt_right(event)
    elif key_pressed.lower() == 'd':
        #trn_left(event)
        pvt_left(event)
    elif key_pressed.lower() == 'q':
        pvt_left(event)
    elif key_pressed.lower() == 'e':
        pvt_right(event)
    elif key_pressed.lower() == 'f':
        find_way(event)
    elif key_pressed.lower() == 'x':
        stop(event)
    else:
        robot_status( key_pressed.lower())


def mov_fwd(event = None ): 
    status = "FORWARD" 
    robot_status(status)

def mov_bkwd(event = None): 
    status = "REVERSE" 
    robot_status(status)

def trn_right(event = None): 
    #status = "RIGHT"
    status = "PIVOT_RIGHT"
    robot_status(status)

def trn_left(event = None): 
    #status = "LEFT" 
    status = "PIVOT_LEFT" 
    robot_status(status)

def pvt_right(event = None): 
    status = "PIVOT_RIGHT"
    robot_status(status)

def pvt_left(event = None): 
    status = "PIVOT_LEFT" 
    robot_status(status)

def find_way(event = None): 
    status = "FIND_WAY" 
    robot_status(status)

def stop(event = None): 
    status = "STOP" 
    robot_status(status)


def write_slogan():
    print("Tkinter is easy to use!")
   
command_listner = tk.Tk()
command_listner.bind('<KeyPress>' , key_input)
command_listner.bind('<Up>', mov_fwd)
command_listner.bind('<Down>', mov_bkwd)
command_listner.bind('<Right>', trn_right)
command_listner.bind('<Left>', trn_left)

frame = tk.Frame(command_listner)
frame.pack()


btn_FWD = tk.Button(frame,
                   text="FWD",
                   command=mov_fwd )

btn_BKWD = tk.Button(frame,
                   text="BKWD",
                   command=mov_bkwd)

btn_TR = tk.Button(frame,
                   text="RIGHT",
                   command=trn_right)

btn_TL = tk.Button(frame,
                   text="LEFT",
                   command=trn_left)

btn_QIT = tk.Button(frame, 
                   text="QUIT", 
                   fg="red",
                   command=quit)

btn_FWD.pack(side=tk.LEFT)
btn_BKWD.pack(side=tk.LEFT)
btn_TR.pack(side=tk.LEFT)
btn_TL.pack(side=tk.LEFT)

btn_QIT.pack(side=tk.LEFT)


command_listner.mainloop()
 