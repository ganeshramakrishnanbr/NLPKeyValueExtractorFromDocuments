"""
Simplified launcher for the NLP Key-Value Extractor application.
This script now only starts the Django frontend, which handles all functionality.
"""
import os
import sys
import subprocess
import signal
import threading
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] %(message)s',
)
logger = logging.getLogger("django_launcher")

# Get the absolute path to the virtual environment Python executable
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_PYTHON = os.path.join(BASE_DIR, ".venv", "Scripts", "python.exe")
if not os.path.exists(VENV_PYTHON):
    # Fallback to the system python if venv is not found
    VENV_PYTHON = sys.executable
    logger.warning(f"Virtual environment not found. Using system python: {VENV_PYTHON}")

# Use a simpler command that will be run from within the 'frontend' directory
FRONTEND_CMD = [VENV_PYTHON, "manage.py", "runserver", "127.0.0.1:8000"]

process = None

def cleanup(sig=None, frame=None):
    """Terminate the running process."""
    global process
    if process:
        logger.info("Shutting down the Django server...")
        process.terminate()
    sys.exit(0)

def log_stream(stream, logger_func):
    """Reads from a stream line-by-line and logs it."""
    for line in iter(stream.readline, ''):
        logger_func(line.strip())
    stream.close()

def main():
    """Main function to launch the Django service."""
    global process
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    logger.info("Starting NLP Key-Value Extractor application (Django Frontend)")
    logger.info(f"Command: {' '.join(FRONTEND_CMD)}")
    logger.info("Navigate to http://127.0.0.1:8000/upload/ in your browser.")
    logger.info("Press Ctrl+C to shut down.")

    try:
        process = subprocess.Popen(
            FRONTEND_CMD,
            cwd=os.path.join(BASE_DIR, "frontend"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # Line-buffered
        )

        # Start threads to log stdout and stderr from the Django process
        stdout_thread = threading.Thread(target=log_stream, args=(process.stdout, logger.info))
        stderr_thread = threading.Thread(target=log_stream, args=(process.stderr, logger.error))
        stdout_thread.daemon = True
        stderr_thread.daemon = True
        stdout_thread.start()
        stderr_thread.start()

        process.wait()  # Wait for the process to complete

        if process.returncode != 0:
            logger.error(f"Django server exited unexpectedly with code: {process.returncode}.")
            logger.error("Check the error messages above for the root cause.")

    except KeyboardInterrupt:
        cleanup()
    except Exception as e:
        logger.error(f"Failed to start Django server: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    # We don't need to call activate.bat as we're already using the venv Python executable
    main()
