import socket
from log import start_log_processor
from cryptography.fernet import Fernet

HOST = "0.0.0.0"
PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#AF_INET->IPv4
#SOCK_DGRAM->UDP
sock.bind((HOST, PORT))

print(f"Server listening on port {PORT}...")
cipher = None  #will store Fernet object

log_queue = []
max = 1000
dropped = 0
client_ciphers = {}

#Start log processing thread
start_log_processor(log_queue)

while True:
    data, addr = sock.recvfrom(1024)
    if data.startswith(b"key"):
        key = data[3:]
        cipher = Fernet(key)
        client_ciphers[addr]=cipher
        print("Received key from client")
        sock.sendto(b"OK", addr)
        continue
    if addr not in client_ciphers:
        continue
    # Decrypt logs
    cipher = client_ciphers[addr]
    try:
        log = cipher.decrypt(data).decode()
    except:
        print("Decryption failed")

    #Backpressure handling
    if len(log_queue) >= max:
        dropped += 1
        continue

    log_queue.append(log)

    if dropped > 0:
        print(f"Dropped logs: {dropped}")