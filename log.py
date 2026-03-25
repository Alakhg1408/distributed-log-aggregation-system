import time
from threading import Thread

def process_logs(log_queue):
    processed_logs = []
    count = 0
    start_time = time.time()

    while True:
        if log_queue:
            log = log_queue.pop(0)

            try:
                timestamp, machine, message = log.split("|")
                timestamp = int(timestamp)

                processed_logs.append((timestamp, machine, message))
                count += 1

            except:
                continue

        #Every second -> print throughput + sorted logs
        if time.time() - start_time >= 1:
            print("\n--- Throughput Report ---")
            print(f"Logs/sec: {count}")

            #Time ordering
            processed_logs.sort(key=lambda x: x[0])

            print("Sample logs:")
            for log in processed_logs[:5]:
                print(log)

            print("-------------------------\n")

            count = 0
            start_time = time.time()
            processed_logs.clear()


def start_log_processor(log_queue):
    t = Thread(target=process_logs, args=(log_queue,))
    t.daemon = True
    t.start()