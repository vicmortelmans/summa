import json
import re

def parse_flight_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    # Combine all streaming chunks into a single dictionary of line key -> raw value
    chunks_map = {}
    for chunk in raw:
        if isinstance(chunk, list) and len(chunk) >= 2:
            lines = chunk[1].splitlines()
            for line in lines:
                if ":" in line:
                    key, val = line.split(":", 1)
                    chunks_map[key] = val

    # Helper function to recursively parse standard JSON string payloads
    def parse_value(val):
        if isinstance(val, str):
            try:
                parsed = json.loads(val)
                return parse_value(parsed)
            except (json.JSONDecodeError, TypeError):
                return val
        elif isinstance(val, list):
            return [parse_value(item) for item in val]
        elif isinstance(val, dict):
            return {k: parse_value(v) for k, v in val.items()}
        return val

    # Resolve all line entries into a cleaned JSON structure
    resolved_structure = {}
    for key, val in chunks_map.items():
        resolved_structure[key] = parse_value(val)

    return resolved_structure

# Execute parsing
parsed_full_tree = parse_flight_data("sacraresponda_q1_a1_next_f_data.json")

# Write out the full depth JSON object
with open("full_depth_structure.json", "w", encoding="utf-8") as f:
    json.dump(parsed_full_tree, f, indent=2, ensure_ascii=False)

print("Full-depth structure saved to 'full_depth_structure.json'.")
