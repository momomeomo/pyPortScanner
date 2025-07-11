# updated but need to test script
# py3
import socket
import threading
import queue
from concurrent.futures import ThreadPoolExecutor
import time

# Get user input
def get_input():
    try:
        threads = int(input("Number of threads: "))
        target = input("IP address: ")
        min_range = int(input("Min port: "))
        max_range = int(input("Max port: "))
        return threads, target, min_range, max_range + 1
    except ValueError:
        print("Please enter valid numbers for threads and ports")
        exit(1)

# Port scanning function
def portscan(port, target, timeout=1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)  # Set timeout to prevent hanging
    try:
        s.connect((target, port))
        print(f"Port {port} is open")
        return port
    except (socket.timeout, socket.error):
        return None  # Silently return None for closed ports
    finally:
        s.close()

# Main scanning function
def scan_ports(target, min_range, max_range, threads):
    open_ports = []
    
    # Using ThreadPoolExecutor for better thread management
    with ThreadPoolExecutor(max_workers=threads) as executor:
        # Create futures for all ports
        futures = [executor.submit(portscan, port, target) 
                  for port in range(min_range, max_range)]
        
        # Collect results
        for future in futures:
            result = future.result()
            if result:
                open_ports.append(result)
    
    return sorted(open_ports)

def main():
    # Get input
    threads, target, min_range, max_range = get_input()
    
    # Validate input
    if min_range < 1 or max_range > 65535:
        print("Port range must be between 1 and 65535")
        return
    
    print(f"Scanning {target} from port {min_range} to {max_range-1}...")
    start_time = time.time()
    
    # Run scan
    open_ports = scan_ports(target, min_range, max_range, threads)
    
    # Print results
    print(f"\nScan completed in {time.time() - start_time:.2f} seconds")
    if open_ports:
        print("Open ports found:", open_ports)
    else:
        print("No open ports found")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScan interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")

	    
