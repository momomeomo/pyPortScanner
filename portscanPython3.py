	# py3
import socket
import threading
import queue

memes = int(input("threads: "))
target = (input("IP address: "))
minRange = int(input("min: "))
maxRange = int(input("max: "))

maxRange += 1

print_lock = threading.Lock()
q = queue.Queue()

def portscan(port):
	s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
	try:
		con = s.connect((target,port))
		with print_lock:
			print(port,'open')
		con.close()
	except:
		with print_lock:
			print(port,'closed')
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


#queue.put in python3 queue.Queue()
#target = IP

#doesnt work on ubuntu? only responds as closed
