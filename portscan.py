    # py2
import socket
import threading
from Queue import Queue


memes = int(input("Amount of threads to use: "))
target = raw_input("IP address: ")
minRange = int(input("min port to scan: "))
maxRange = int(input("max port to scan: "))
maxRange += 1


print_lock = threading.Lock()
q = Queue()


def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = s.connect((target,port))
        with print_lock:
            print(port,'OPEN')
        con.close()
    except:
	    with print_lock:
		    print(port, 'CLOSED')
		    return


def threader():
    while True:
        worker = q.get()
        portscan(worker)
        q.task_done


for x in range(memes):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()


for worker in range(minRange,maxRange):
    q.put(worker)


q.join()


# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server = ''

#target = IP
