import socket
import time
import random
from cryptography.fernet import Fernet

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9999

#encryption using Fernet (symmetric encryption)
key = Fernet.generate_key()
cipher = Fernet(key)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)

#Send key once
while True:
    sock.sendto(b"key" + key, (SERVER_IP, SERVER_PORT))
    print("Sending key")
    try:
        data, _ = sock.recvfrom(1024)
        if data == b"OK":
            print("Sending logs:")
            break
    except socket.timeout:
        print("Retry")
        time.sleep(1)

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
    encrypted_log = cipher.encrypt(log.encode()) #encrypting the log

    sock.sendto(encrypted_log, (SERVER_IP, SERVER_PORT))
    #log.encode()->convert string to bytes

    time.sleep(0.01)  #100 logs/sec total