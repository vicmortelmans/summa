import glob
import os
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
docs_dir = os.path.join(script_dir, "../docs/bronbestanden")

def slugify(text):
    # Remove non-alphanumeric characters and replace with hyphens
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

# Find all merged files matching "../docs/bronbestanden/*/merged/*.txt"
pattern = os.path.join(docs_dir, "*", "merged", "*.txt")
files = glob.glob(pattern)

for file_path in files:
    print(f"Processing: {file_path}")
    
    # Determine split directory: sibling of 'merged'
    merged_dir = os.path.dirname(file_path)
    parent_dir = os.path.dirname(merged_dir)
    split_dir = os.path.join(parent_dir, "split")
    
    if not os.path.exists(split_dir):
        os.makedirs(split_dir)
        
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    current_lines = []
    current_slug = "intro"
    file_counter = 0
    
    for line in lines:
        # Check for split keywords
        if "KWESTIE" in line or "ARTIKEL" in line:
            # If we have accumulated content, write it to a file
            if current_lines:
                output_filename = f"{file_counter:02d}_{current_slug}.txt"
                output_path = os.path.join(split_dir, output_filename)
                with open(output_path, "w", encoding="utf-8") as out_f:
                    out_f.write("".join(current_lines))
                
                file_counter += 1
                current_lines = []
            
            # Update slug for the new section using the current header line
            current_slug = slugify(line)
            
        current_lines.append(line)
        
    # Write the last section
    if current_lines:
        output_filename = f"{file_counter:02d}_{current_slug}.txt"
        output_path = os.path.join(split_dir, output_filename)
        with open(output_path, "w", encoding="utf-8") as out_f:
            out_f.write("".join(current_lines))