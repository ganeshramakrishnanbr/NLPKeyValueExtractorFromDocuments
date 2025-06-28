import json
import os
from standalone_extractor import extract_from_file

result = extract_from_file('markdown_sample.md')
output_path = os.path.join(os.getcwd(), 'markdown_results.json')
with open(output_path, 'w') as f:
    json.dump(result, f, indent=2)
print(f"Results saved to {output_path}")

# Also print to console for debugging
print(json.dumps(result, indent=2))
