import json
import os
from standalone_extractor import extract_from_file

# Use absolute path for input file
input_file = os.path.join(os.getcwd(), 'markdown_sample.md')
# Use Documents folder for output
output_file = os.path.expanduser("~/Documents/markdown_results.json")

# Extract data
result = extract_from_file(input_file)

# Write to file in Documents folder
with open(output_file, 'w') as f:
    json.dump(result, f, indent=2)

# Print status for confirmation
print(f"Data written to {output_file}")

# Also print the results to the console
print("\nExtracted data:")
print(json.dumps(result, indent=2))
