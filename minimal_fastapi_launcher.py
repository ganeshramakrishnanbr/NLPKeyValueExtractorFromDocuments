"""
Extremely minimal FastAPI test with direct process launch
This bypasses the standard import approach
"""
import sys
import subprocess
import os

# Get the path to the Python executable
python_exe = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                          ".venv", "Scripts", "python.exe")

# Create a temporary file with a minimal FastAPI app
temp_file = "temp_fastapi_test.py"
with open(temp_file, "w") as f:
    f.write("""
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7777)
""")

print(f"Created temporary FastAPI test file: {temp_file}")
print(f"Using Python executable: {python_exe}")

# Launch the FastAPI app directly as a subprocess
try:
    print("Attempting to run the FastAPI app...")
    process = subprocess.Popen([python_exe, temp_file], 
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               text=True)
    
    # Print the first 10 lines of output
    print("First 10 lines of output:")
    count = 0
    for line in process.stdout:
        print(line.strip())
        count += 1
        if count >= 10:
            break
    
    # Kill the process
    process.terminate()
    
except Exception as e:
    print(f"Error running FastAPI: {str(e)}")
finally:
    # Clean up the temporary file
    try:
        os.remove(temp_file)
        print(f"Removed temporary file: {temp_file}")
    except:
        pass
