# Reads text files from ../docs/bronbestanden/*/*.nl.txt and writes merged text to ../docs/bronbestanden/*/merged/*.txt

import glob
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
docs_dir = os.path.join(script_dir, "../docs/bronbestanden")

# Find all files matching the pattern
pattern = os.path.join(docs_dir, "*", "*.nl.txt")
files = glob.glob(pattern)

# Group files by parent directory
files_by_dir = {}
for file_path in files:
    parent_dir = os.path.dirname(file_path)
    if parent_dir not in files_by_dir:
        files_by_dir[parent_dir] = []
    files_by_dir[parent_dir].append(file_path)

# Process each directory
for parent_dir, file_list in files_by_dir.items():
    # Sort files by filename
    file_list.sort()
    
    merged_paragraphs = []
    
    for i, file_path in enumerate(file_list):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Split content into paragraphs
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        
        if not paragraphs:
            continue
            
        print(f"Processing: {file_path}")

        if not merged_paragraphs:
            # First file, just add all paragraphs
            merged_paragraphs.extend(paragraphs)
        else:
            # Check the final paragraph of the accumulated text
            last_paragraph = merged_paragraphs[-1]
            
            # If it doesn't end with a '.', '?' or '!', merge with the first paragraph of the current file
            if not last_paragraph.endswith((".", "?", "!")):
                first_paragraph_current = paragraphs[0]
                # Merge on a single line (join with space)
                merged_paragraphs[-1] = last_paragraph + " " + first_paragraph_current
                # Add the remaining paragraphs from the current file
                merged_paragraphs.extend(paragraphs[1:])
            else:
                merged_paragraphs.extend(paragraphs)

    # Define output filename: parent directory name + .txt
    dir_name = os.path.basename(parent_dir)
    output_filename = f"{dir_name}.txt"
    output_path = os.path.join(parent_dir, "merged", output_filename)
    
    print(f"Writing merged file: {output_path}")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(merged_paragraphs))