from __future__ import print_function
from dronekit import connect, VehicleMode
import time


aTargetAltitude=20
#Set up option parsing to get connection string
import argparse  
parser = argparse.ArgumentParser(description='Print out vehicle state information. Connects to SITL on local PC by default.')
parser.add_argument('--connect', 
                   help="vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None
baud_rate=115200

#Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()


# Connect to the Vehicle. 
#   Set `wait_ready=True` to ensure default attributes are populated before `connect()` returns.
print("\nConnecting to vehicle on: %s" % connection_string)
vehicle = connect(connection_string, baud=baud_rate, wait_ready=True)

vehicle.wait_ready('autopilot_version')

print(" Global Location: %s" % vehicle.location.global_frame)
print(" Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
print(" Local Location: %s" % vehicle.location.local_frame)
print(" Attitude: %s" % vehicle.attitude)
print(" Velocity: %s" % vehicle.velocity)
print(" Is Armable?: %s" % vehicle.is_armable)
print(" System status: %s" % vehicle.system_status.state)
print(" Airspeed: %s" % vehicle.airspeed)    # settable
print(" Mode: %s" % vehicle.mode.name)    # settable

##change vehicle mode
vehicle.mode = VehicleMode("GUIDED")
while not vehicle.mode.name=='GUIDED':  #Wait until mode has changed
    print(" Waiting for mode change ...")
    time.sleep(1)

print(" Mode: %s" % vehicle.mode.name)

# Check that vehicle is armable
##while not vehicle.is_armable:
##    print(" Waiting for vehicle to initialise...")
##    time.sleep(1)
    # If required, you can provide additional information about initialisation
    # using `vehicle.gps_0.fix_type` and `vehicle.mode.name`.   
#print "\nSet Vehicle.armed=True (currently: %s)" % vehicle.armed 

##Arm vehicle
vehicle.armed = True
while not vehicle.armed:
    print (" Waiting for arming...")
    time.sleep(1)
print (" Vehicle is armed: %s" % vehicle.armed)


###----------------take off
print("Taking off!")
vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude
  
time.sleep(10) ###    TEST
print('Return to launch')
vehicle.mode = VehicleMode("RTL")

#while True:
#        print(" Altitude: ", vehicle.location.global_relative_frame.alt)      
#        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: #Trigger just below target alt.
#            print("Reached target altitude")
#            time.sleep(2)
#            print('Return to launch')
#            vehicle.mode = VehicleMode("RTL")
#        time.sleep(1)


###--------------------------------------



#Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()