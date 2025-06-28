"""
Simplified startup script for the NLP Key-Value Extractor
Designed to handle Windows-specific issues
"""
import os
import sys
import subprocess
import signal
import time
import threading

# Get the absolute path to the project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"Project directory: {BASE_DIR}")

# Get the absolute path to the virtual environment Python executable
VENV_PYTHON = os.path.join(BASE_DIR, ".venv", "Scripts", "python.exe")
print(f"Python executable: {VENV_PYTHON}")

if not os.path.exists(VENV_PYTHON):
    print(f"ERROR: Virtual environment Python not found at: {VENV_PYTHON}")
    print("Make sure you have activated the virtual environment")
    sys.exit(1)

# List of running processes
processes = []

def run_command(command, name, cwd=None):
    """Run a command and capture its output"""
    print(f"Starting {name}: {' '.join(command)}")
    
    try:
        # Use CREATE_NEW_CONSOLE flag on Windows to open in new window
        if sys.platform == 'win32':
            process = subprocess.Popen(
                command,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                cwd=cwd
            )
        else:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=cwd
            )
            
            # Only set up output logging for non-Windows platforms
            def log_output():
                for line in process.stdout:
                    print(f"[{name}] {line.strip()}")
            
            threading.Thread(target=log_output, daemon=True).start()
        
        processes.append((process, name))
        return process
    
    except Exception as e:
        print(f"ERROR starting {name}: {str(e)}")
        return None

def cleanup():
    """Clean up all running processes"""
    print("\nShutting down services...")
    
    for process, name in processes:
        try:
            print(f"Terminating {name} (PID: {process.pid})...")
            if sys.platform == 'win32':
                # On Windows, use taskkill to force terminate
                subprocess.run(['taskkill', '/F', '/T', '/PID', str(process.pid)], 
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                process.terminate()
                process.wait(timeout=2)
        except:
            print(f"Could not terminate {name} gracefully")

def signal_handler(sig, frame):
    """Handle interrupt signals"""
    cleanup()
    sys.exit(0)

def main():
    """Main function to start the application"""
    signal.signal(signal.SIGINT, signal_handler)
    
    print("======================================================")
    print("      NLP Key-Value Extractor - Launch Script         ")
    print("======================================================")
    
    # Start FastAPI backend - open in new window
    backend_cmd = [VENV_PYTHON, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"]
    backend_process = run_command(backend_cmd, "FastAPI Backend")
    
    if not backend_process:
        print("Failed to start backend")
        cleanup()
        return
    
    time.sleep(1)  # Brief pause before starting the frontend
    
    # Start Django frontend - open in new window
    frontend_dir = os.path.join(BASE_DIR, "frontend")
    frontend_cmd = [VENV_PYTHON, os.path.join(frontend_dir, "manage.py"), "runserver", "127.0.0.1:8080"]
    frontend_process = run_command(frontend_cmd, "Django Frontend", cwd=frontend_dir)
    
    if not frontend_process:
        print("Failed to start frontend")
        cleanup()
        return
    
    print("\n======================================================")
    print(" Application is now running!")
    print(" - Backend API: http://127.0.0.1:8000")
    print(" - Frontend:    http://127.0.0.1:8080")
    print("======================================================")
    print(" Press Ctrl+C to shut down all services")
    print("======================================================\n")
    
    try:
        # Keep the script running until interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()

if __name__ == "__main__":
    main()
