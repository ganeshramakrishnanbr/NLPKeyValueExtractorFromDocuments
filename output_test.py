"""
Simple output test to verify console display
"""
import sys
import time
import os

print("=" * 50)
print("Simple output test script")
print("=" * 50)
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print("Now printing 1-10 with delays to test output streaming:")

for i in range(1, 11):
    print(f"Number: {i}")
    sys.stdout.flush()  # Force output to be displayed
    time.sleep(0.5)

print("=" * 50)
print("Test complete!")
print("=" * 50)
