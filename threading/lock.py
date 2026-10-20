import threading
import time
# lock = threading.Lock()
counter = 0
def increment():
    global counter
    for _ in range(100000):
        # with lock:
            counter += 1
            
            time.sleep(0)
            
t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)
t1.start()
t2.start()
t1.join()
t2.join()
print(counter)  #