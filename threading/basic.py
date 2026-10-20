import threading
import time

def task(name):
    for i in range(3):
        print(f"{name} running")
        time.sleep(1)

# Create threads
t1 = threading.Thread(target=task, args=("Thread-1",))
t2 = threading.Thread(target=task, args=("Thread-2",))

# Start threads
t1.start()
t2.start()
# Wait for completion
t1.join()
t2.join()
print("Main thread finished")