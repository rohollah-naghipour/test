import time
import threading


def worker(name, delay):
    print(f"{name} starting work")
    time.sleep(delay)
    print(f"{name} finished work")

thread1 = threading.Thread(target=worker, args=("Worker-1", 2))
thread2 = threading.Thread(target=worker, args=("Worker-2", 3))

thread1.start()
thread2.start()

thread1.join()
thread2.join()
print("All workers done")