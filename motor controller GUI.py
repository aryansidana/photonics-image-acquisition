from ctypes import *
import time
import os
import sys
import platform
import tempfile
import re
from tkinter import *

#Global Variables
global device_id
global degPerRev
global countsPerRev
global speed
global begin
global rotate
global microsteps
global microstep_deg
global motorActivated
global step_size
global open_name
motorActivated= True

countsPerRev = 200 
degPerRev = 1.8

#Libximc INSTALLATION
if sys.version_info >= (3,0):
    import urllib.parse
    
cur_dir = os.path.abspath(os.path.dirname(__file__))
print(cur_dir)
ximc_dir = os.path.join(cur_dir, "ximc")
ximc_package_dir = os.path.join(ximc_dir, "crossplatform", "wrappers", "python")
sys.path.append(ximc_package_dir)  # add ximc.py wrapper to python path

if platform.system() == "Windows":
    arch_dir = "win64" if "64" in platform.architecture()[0] else "win32"
    libdir = os.path.join(ximc_dir, arch_dir)
    os.environ["Path"] = libdir + ";" + os.environ["Path"]  # add dll

try: 
    from pyximc import *
except ImportError as err:
    print ("Can't import pyximc module. The most probable reason is that you changed the relative location of the testpython.py and pyximc.py files. See developers' documentation for details.")
    exit()
except OSError as err:
    print ("Can't load libximc library. Please add all shared libraries to the appropriate places. It is decribed in detail in developers' documentation. On Linux make sure you installed libximc-dev package.\nmake sure that the architecture of the system and the interpreter is the same")
    exit()

# variable 'lib' points to a loaded library
# note that ximc uses stdcall on win
print("Library loaded")

sbuf = create_string_buffer(64)
lib.ximc_version(sbuf)
print("Library version: " + sbuf.raw.decode().rstrip("\0"))

# Set bindy (network) keyfile. Must be called before any call to "enumerate_devices" or "open_device" if you
# wish to use network-attached controllers. Accepts both absolute and relative paths, relative paths are resolved
# relative to the process working directory. If you do not need network devices then "set_bindy_key" is optional.
# In Python make sure to pass byte-array object to this function (b"string literal").
lib.set_bindy_key(os.path.join(ximc_dir, "win32", "keyfile.sqlite").encode("utf-8"))

# This is device search and enumeration with probing. It gives more information about devices.
probe_flags = EnumerateFlags.ENUMERATE_PROBE + EnumerateFlags.ENUMERATE_NETWORK
enum_hints = b"addr=192.168.0.1,172.16.2.3"
# enum_hints = b"addr=" # Use this hint string for broadcast enumerate
devenum = lib.enumerate_devices(probe_flags, enum_hints)
print("Device enum handle: " + repr(devenum))
print("Device enum handle type: " + repr(type(devenum)))

dev_count = lib.get_device_count(devenum)
print("Device count: " + repr(dev_count))

controller_name = controller_name_t()
for dev_ind in range(0, dev_count):
    enum_name = lib.get_device_name(devenum, dev_ind)
    result = lib.get_enumerate_device_controller_name(devenum, dev_ind, byref(controller_name))
    if result == Result.Ok:
        print("Enumerated device #{} name (port name): ".format(dev_ind) + repr(enum_name) + ". Friendly name: " + repr(controller_name.ControllerName) + ".")

open_name = None
if len(sys.argv) > 1:
    open_name = sys.argv[1]
elif dev_count > 0:
    open_name = lib.get_device_name(devenum, 0)
elif sys.version_info >= (3,0):
    # use URI for virtual device when there is new urllib python3 API
    tempdir = tempfile.gettempdir() + "/testdevice.bin"
    if os.altsep:
        tempdir = tempdir.replace(os.sep, os.altsep)
    # urlparse build wrong path if scheme is not file
    uri = urllib.parse.urlunparse(urllib.parse.ParseResult(scheme="file", \
            netloc=None, path=tempdir, params=None, query=None, fragment=None))
    open_name = re.sub(r'^file', 'xi-emu', uri).encode()

if not open_name:
    exit(1)

if type(open_name) is str:
    open_name = open_name.encode()
   
print("\nOpen device " + repr(open_name))
device_id = lib.open_device(open_name)
print("Device id: " + repr(device_id))


#ROTATION/CONTROL FUNCTION
def move(lib, device_id, distance, udistance):
    lib.command_move(device_id, distance, udistance)
    
def homezero (lib, device_id):
    lib.command_home(device_id)
    
def close_device(lib, device_id):
    lib.close_device(byref(cast(device_id, POINTER(c_int))))

def open_device(lib,open_name):
    lib.open_device(open_name)

def set_speed(lib, device_id, speed):
    mvst = move_settings_t()
    result = lib.get_move_settings(device_id, byref(mvst))
    print("Read command result: " + repr(result))
    print("The speed was equal to {0}. We will change it to {1}".format(mvst.Speed, speed))
    mvst.Speed = int(speed)
    result = lib.set_move_settings(device_id, byref(mvst))
    print("Write command result: " + repr(result))  

def get_position(lib, device_id):
    x_pos = get_position_t()
    result = lib.get_position(device_id, byref(x_pos))
    print("Result: " + repr(result))
    if result == Result.Ok:
        print("Position: {0} steps, {1} microsteps".format(x_pos.Position, x_pos.uPosition))
    return x_pos.Position, x_pos.uPosition 

def switchButtonState(button):
    if (button['state'] == NORMAL):
        button['state'] = DISABLED
    else:
        button['state'] = NORMAL

#Motor Controller GUI
root = Tk()
root.title("Stepper Motor Controller")
root.geometry('300x700')
root.resizable(False,False)

#FRAMES
frame1 = LabelFrame (root, text = "Motor Controller", padx = 5, pady = 5)
frame1.pack(fill="both", expand="yes")

frame2 = LabelFrame (frame1, text = "Activation", padx = 5, pady = 5)
frame2.pack(fill="both")

frame3 = LabelFrame (frame1, text = "Rotation", padx = 5, pady = 5)
frame3.pack(fill="both")

frame4 = LabelFrame (frame1, text = "Microsteps", padx = 5, pady = 5)
frame4.pack(fill="both", expand="yes")

#MOTOR ACTIVATION BUTTON EVENT BINDERS
def activate_clicked():
    global motorActivated
    global device_id
    global open_name
    if motorActivated:
        lib.command_sstp(device_id)
        close_device(lib, device_id)
        switchButtonState(runforw_btn)
        switchButtonState(reset_btn)
        switchButtonState(enter_btn)
        print("Stepper Motor is off")
        motorActivated = False
    else:
        open_device(lib, open_name)
        switchButtonState(runforw_btn)
        switchButtonState(reset_btn)
        switchButtonState(enter_btn)
        print("Stepper Motor is on")
        motorActivated = True

def runforw_clicked():
    global device_id
    global degPerRev
    global countsPerRev
    global speed
    global begin
    global rotate
    global microsteps
    global microstep_deg
    global step_size
    set_speed(lib,device_id, speed)
    num = begin
    

    while num < rotate or num == rotate : 
        position = round(num*(countsPerRev/degPerRev))
        #print (position)
        #print (num)
        time.sleep(3)
        move(lib, device_id, position, microsteps)
        get_position(lib, device_id)
        num += step_size
      
      
    move(lib, device_id, 0, 0)
    get_position(lib, device_id)
    #get signal from image aquisiton team
    
def reset_clicked():
    global device_id
    homezero(lib, device_id)
    get_position(lib, device_id)
    
    
#BUTTONS FOR MOTOR ACTIVATION

activate_btn = Button(frame2, text = "Activate", font=("Helvetica 10"), command= activate_clicked, state=NORMAL)
activate_btn.pack(side = "top")

runforw_btn = Button(frame2, text = "Run Forward", font=("Helvetica 10"), command = runforw_clicked, state=NORMAL)
runforw_btn.pack(side = "top")

reset_btn = Button(frame2, text = "Reset", font=("Helvetica 10"), command = reset_clicked, state=NORMAL)
reset_btn.pack(side = "top")


#BUTTONS FOR ROTATION
speed_frame = LabelFrame (frame3, text = "Speed")
speed_frame.pack(fill="both")

begin_frame = LabelFrame (frame3, text = "Begin At (Degrees)")
begin_frame.pack(fill="both")

rotate_frame = LabelFrame (frame3, text = "Rotate (Degrees)")
rotate_frame.pack(fill="both")

step_frame = LabelFrame (frame3, text = "Step Size (Degrees)")
step_frame.pack(fill="both")

speed_entry = Entry(speed_frame)
speed_entry.pack(fill="both", expand = "yes", side = "left",padx = 10, pady = 10)

begin_entry = Entry(begin_frame)
begin_entry.pack(fill="both", expand = "yes", side = "left",padx = 10, pady = 10)

rotate_entry = Entry(rotate_frame)
rotate_entry.pack(fill="both", expand = "yes", side = "left",padx = 10, pady = 10)

step_entry = Entry(step_frame)
step_entry.pack(fill="both", expand = "yes", side = "left",padx = 10, pady = 10)

#ROTATION/MICROSTEP BUTTON COMMAND BINDERS
def get_info():
    global speed
    speed = float(speed_entry.get())
    global begin
    begin = float(begin_entry.get())
    global rotate
    rotate = float(rotate_entry.get())
    global microsteps
    microsteps = int(microsteps_listbox.get(ANCHOR))
    global step_size
    step_size = float(step_entry.get())
        
#BUTTONS FOR MICROSTEPS
microstep_frame = LabelFrame (frame4, text = "Options")
microstep_frame.pack(side = "left",padx = 15, pady = 15)

microsteps_listbox = Listbox(microstep_frame, width = 10, height = 10, state=NORMAL)
microsteps = ["0", "2", "4", "8", "16", "32", "64", "128", "256"]
for microstep in microsteps:
    microsteps_listbox.insert(END, microstep)
microsteps_listbox.pack()

#MICROSTEP BUTTON COMMAND BINDERS
enter_btn = Button(frame1, text = "Enter", font=("Helvetica 10"), command = get_info, state=NORMAL)
enter_btn.pack(expand = "yes", fill="both")

root.mainloop()
