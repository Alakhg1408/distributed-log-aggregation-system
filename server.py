import socket
from log import start_log_processor

HOST = "0.0.0.0"
PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#AF_INET->IPv4
#SOCK_DGRAM->UDP
sock.bind((HOST, PORT))

print(f"Server listening on port {PORT}...")

log_queue = []
max = 1000
dropped = 0

#Start log processing thread
start_log_processor(log_queue)

while True:
    data, addr = sock.recvfrom(1024)
    log = data.decode()

    #Backpressure handling
    if len(log_queue) >= max:
        dropped += 1
        continue

    log_queue.append(log)

    if dropped > 0:
        print(f"Dropped logs: {dropped}")