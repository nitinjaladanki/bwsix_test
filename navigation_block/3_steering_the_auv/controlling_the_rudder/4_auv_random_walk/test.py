# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 20:49:23 2021

@author: JO20993
"""
from BWSI_AUV import AUV

import numpy as np
import matplotlib.pyplot as plt

import hashlib
    
def my_hash(data):
    if not isinstance(data, str):
        d2 = data.tobytes()
    else:
        d2 = data.encode("UTF-8")
        
    return hashlib.md5(d2).hexdigest()

def round_and_report(data, n):
    d2 = np.rint(data * 10**n).astype(np.int32)
    return my_hash(d2)
    
# in this exercise we'll make a series of random commands at random times
command_list = ["RUDDER RIGHT 5 DEGREES",
                "RUDDER LEFT 5 DEGREES",
                "RUDDER RIGHT 10 DEGREES",
                "RUDDER LEFT 10 DEGREES",
                "POLLY WANT A CRACKER",
                "RIGHT STANDARD RUDDER",
                "LEFT STANDARD RUDDER",
                "RIGHT FULL RUDDER",
                "LEFT FULL RUDDER",
                "INCREASE YOUR RUDDER TO 90 DEGREES!",
                "HARD RIGHT RUDDER",
                "HARD LEFT RUDDER",
                "SHIFT YOUR RUDDER",
                "RUDDER AMIDSHIPS",
                "YEARRRGHHH!!"]

np.random.seed(2021)
count = 0
hdg = 0
print(f"\nCreating AUV instance at heading = {hdg}")
myAUV = AUV(latlon=(42.4, -171.3), heading=hdg, datum=(42.5,-171.5))
start_x = myAUV._AUV__position[0]
start_y = myAUV._AUV__position[1]
x = [0]
y = [0]
t = [0]
    
dt = 1
positions = list()
 
cmd = "ENGINE HALF AHEAD"
reply = myAUV.engine_command(cmd)
print(f"{cmd} : {reply}")
for i in range(1000):
    myAUV.update_state(dt)

    # captain makes a random command occasionally
    if (np.random.rand() < 0.1):
        idx = np.int( np.floor( np.random.rand() * len(command_list) ) )
        cmd = command_list[idx]
        reply = myAUV.helm_command(cmd)
        print(f"{cmd} : {reply}")

    cmd = "MARK YOUR HEAD"
    reply = myAUV.helm_command(cmd)
    heading = float(reply.split()[1])
    print(f"{cmd} : {reply}")
  
    positions.append(myAUV._AUV__position[0])
    positions.append(myAUV._AUV__position[1])
    x.append(myAUV._AUV__position[0] - start_x)
    y.append(myAUV._AUV__position[1] - start_y)
    t.append(t[-1]+dt)
         
    count = count + 1

fig = plt.figure()
ax1 = fig.add_subplot(2,2,1)
ax1.plot(t, x)
ax1.set_xlabel('Time (sec)')
ax1.set_ylabel('Relative Easting (m)')
ax2 = fig.add_subplot(2,2,3)
ax2.plot(t, y)
ax2.set_xlabel('Time (sec)')
ax2.set_ylabel('Relative Northing (m)')
ax3 = fig.add_subplot(2,2,(2,4))
ax3.plot(x, y)
ax3.set_xlabel('Relative Easting (m)')
ax3.set_ylabel('Relative Northing (m)')

# plt.plot(np.array(x), np.array(y))
# plt.show()
 