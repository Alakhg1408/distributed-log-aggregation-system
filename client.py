import socket
import time
import random

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#AF_INET->IPv4
#SOCK_DGRAM->UDP

machines = [f"machine{i}" for i in range(1, 51)]

messages = [
    "CPU high",
    "Memory usage high",
    "Disk warning",
    "User login",
    "Service started"
]

while True:
    timestamp = int(time.time()) #timestamp 
    machine = random.choice(machines) #random machine
    message = random.choice(messages) #random message 

    log = f"{timestamp}|{machine}|{message}"

    sock.sendto(log.encode(), (SERVER_IP, SERVER_PORT))
    #log.encode()->convert string to bytes

    time.sleep(0.01)  #100 logs/sec total