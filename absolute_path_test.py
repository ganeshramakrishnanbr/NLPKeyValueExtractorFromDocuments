import json
import os
from standalone_extractor import extract_from_file

# Use absolute path for input file
input_file = os.path.join(os.getcwd(), 'markdown_sample.md')
# Use absolute path for output file
output_file = os.path.join(os.getcwd(), 'output.json')

# Extract data
result = extract_from_file(input_file)

# Write to file using absolute path
with open(output_file, 'w') as f:
    json.dump(result, f, indent=2)

# Print status for confirmation
print(f"Data written to {output_file}")
