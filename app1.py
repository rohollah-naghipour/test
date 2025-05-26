import time
import threading


def my_task():
    print("Thread starting")
    time.sleep(2)  # Simulate work
    print("Continue function operation")

# Create the thread
thread = threading.Thread(target=my_task)

# Start the thread
thread.start()

# Wait for the thread to finish
thread.join()
print("Main program continues")