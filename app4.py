import time
import threading

counter = 0
lock = threading.Lock()

def increment_counter():
    global counter
    for _ in range(100000):
        with lock: 
            counter += 1

threads = []
for _ in range(5):
    thread = threading.Thread(target=increment_counter)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print(f"Final counter value: {counter}")  