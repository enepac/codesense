import socket
import psutil
import os

def find_available_port():
    """Find an available port by binding to port 0."""
    with socket.socket() as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def kill_process_on_port(port):
    """Kill the process using the specified port."""
    try:
        # Get all network connections
        connections = psutil.net_connections()
        for conn in connections:
            if conn.laddr and conn.laddr.port == port:
                pid = conn.pid
                try:
                    # Get the process and terminate it
                    proc = psutil.Process(pid)
                    print(f"Killing process {proc.name()} (PID: {pid}) using port {port}")
                    proc.terminate()  # Gracefully terminate the process
                    proc.wait(timeout=5)  # Wait for the process to terminate
                    return
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    print(f"Failed to kill process with PID {pid}")
                    continue
        print(f"No process found using port {port}")
    except Exception as e:
        print(f"Error while checking connections: {e}")

def main():
    port = 5173  # Replace with the port you want to free
    print(f"Attempting to free port {port}...")
    kill_process_on_port(port)

    print("\nFinding an available port...")
    available_port = find_available_port()
    print(f"Available port: {available_port}")

if __name__ == "__main__":
    main()