# coding=utf-8

import sys
sys.path.insert(0, "..")
import logging
import os
import time

try:
    from IPython import embed
except ImportError:
    import code



from opcua import ua, uamethod, Server

var_Servo_left_angle = None
var_Servo_right_angle = None
var_Servo_middle_angle = None
var_Servo_claw_angle = None

SNums = [0,1,2,3] #Numbers of the Servos we’ll be using in ServoBlaster
SName = ["Waist","Left","Right","Claw"] #Names of Servos
AInis = [90,152,90,60] #Initial angle for Servos 0-3
AMins = [0,60,40,60] #Minimum angles for Servos 0-3
AMaxs = [180,165,180,180] #Maximum angles for Servos 0-3
ACurs = AInis #Current angles being set as the intial angles
Step = 5

# method to be exposed through server
def func(parent, variant):
    ret = False
    if variant.Value % 2 == 0:
        ret = True
    return [ua.Variant(ret, ua.VariantType.Boolean)]


# method to be exposed through server
# uses a decorator to automatically convert to and from variants

@uamethod
def move_servo_left(parent, angle):
    os.system("echo 1=%d%% > /dev/servoblaster" % angle)
    var_Servo_left_angle.set_value(angle)

@uamethod
def move_servo_right(parent, angle):
    os.system("echo 2=%d%% > /dev/servoblaster" % angle)
    var_Servo_right_angle.set_value(angle)

@uamethod
def move_servo_middle(parent, angle):
    os.system("echo 0=%d%% > /dev/servoblaster" % angle)
    var_Servo_middle_angle.set_value(angle)

@uamethod
def move_servo_claw(parent, angle):
    os.system("echo 3=%d%% > /dev/servoblaster" % angle)
    var_Servo_claw_angle.set_value(angle)

if __name__ == "__main__":
	# optional: setup logging
    logging.basicConfig(level=logging.WARN)
    #logger = logging.getLogger("opcua.address_space")
    # logger.setLevel(logging.DEBUG)
    #logger = logging.getLogger("opcua.internal_server")
    # logger.setLevel(logging.DEBUG)
    #logger = logging.getLogger("opcua.binary_server_asyncio")
    # logger.setLevel(logging.DEBUG)
    #logger = logging.getLogger("opcua.uaprocessor")
    # logger.setLevel(logging.DEBUG)
    #logger = logging.getLogger("opcua.subscription_service")
    # logger.setLevel(logging.DEBUG)
	
    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    server.set_server_name("FreeOpcUa Example Server")
	
    server.load_certificate("robotarm_cert.der")
    server.load_private_key("robotarm_pk.pem")

    # setup our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our custom stuff
    objects = server.get_objects_node()
	
     # populating our address space
    myfolder = objects.add_folder(idx, "GFISmartFleet")
    myobj = server.get_root_node().get_child(["0:Objects","2:GFISmartFleet"]).add_object(idx, "RobotArm")
	
    var_Servo_left_angle = myobj.add_variable(idx, "Servo_left_angle", 90)
    var_Servo_left_angle.set_writable()
	
    var_Servo_right_angle = myobj.add_variable(idx, "Servo_right_angle", 90)
    var_Servo_right_angle.set_writable()
	
    var_Servo_middle_angle = myobj.add_variable(idx, "Servo_middle_angle", 90)
    var_Servo_middle_angle.set_writable()
	
    var_Servo_claw_angle = myobj.add_variable(idx, "Servo_claw_angle", 25)
    var_Servo_claw_angle.set_writable()
	
    #myarrayvar = myobj.add_variable(idx, "myarrayvar", [6.7, 7.9])
    #myarrayvar = myobj.add_variable(idx, "myStronglytTypedVariable", ua.Variant([], ua.VariantType.UInt32))
    #myprop = myobj.add_property(idx, "myproperty", "I am a property")
    #mymethod = myobj.add_method(idx, "move_servo1", func, [ua.VariantType.Int64], [ua.VariantType.Boolean])
    #inargx = ua.Argument()
    #inargx.Name = "x"
    #inargx.DataType = ua.NodeId(ua.ObjectIds.Int64)
    #inargx.ValueRank = -1
    #inargx.ArrayDimensions = []
    #inargx.Description = ua.LocalizedText("First number x")
    #inargy = ua.Argument()
    #inargy.Name = "y"
    #inargy.DataType = ua.NodeId(ua.ObjectIds.Int64)
    #inargy.ValueRank = -1
    #inargy.ArrayDimensions = []
    #inargy.Description = ua.LocalizedText("Second number y")
    #outarg = ua.Argument()
    #outarg.Name = "Result"
    #outarg.DataType = ua.NodeId(ua.ObjectIds.Int64)
    #outarg.ValueRank = -1
    #outarg.ArrayDimensions = []
    #outarg.Description = ua.LocalizedText("Multiplication result")
    #multiply_node = myobj.add_method(idx, "move_servo1", multiply, [inargx, inargy], [outarg])

    method_servo_left_node = myobj.add_method(idx, "move_servo_left", move_servo_left, [ua.VariantType.Int64])
    method_servo_right_node = myobj.add_method(idx, "move_servo_right", move_servo_right, [ua.VariantType.Int64])
    method_servo_middle_node = myobj.add_method(idx, "move_servo_middle", move_servo_middle, [ua.VariantType.Int64])
    method_servo_claw_node = myobj.add_method(idx, "move_servo_claw", move_servo_claw, [ua.VariantType.Int64])


    # starting!
    server.start()
    print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
    try:
         os.system('sudo /home/pi/PiBits/ServoBlaster/user/servod –-idle-timeout=2000') #This line is sent to command line to start the servo controller
         while True:
             time.sleep(1)
#            myvar.set_value(count)
    finally:
        #close connection, remove subcsriptions, etc
        server.stop()
