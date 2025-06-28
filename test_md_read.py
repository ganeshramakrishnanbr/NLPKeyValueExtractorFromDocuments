# Simple test to confirm we can read and process a Markdown file
import os

# Get the current directory
current_dir = os.getcwd()
print(f"Current directory: {current_dir}")

# Path to the Markdown file
md_file = os.path.join(current_dir, 'markdown_sample.md')
print(f"Markdown file path: {md_file}")

# Check if the file exists
if os.path.exists(md_file):
    print(f"File exists: {md_file}")
    # Try to read it
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"Successfully read {len(content)} characters")
            # Print first few lines
            print("First 100 characters:")
            print(content[:100])
    except Exception as e:
        print(f"Error reading file: {str(e)}")
else:
    print(f"File does not exist: {md_file}")
