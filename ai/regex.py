import glob
import os
import re

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.join(script_dir, "../docs/bronbestanden")

    # Find all text files in 'merged' directories
    pattern = os.path.join(docs_dir, "*", "merged", "*.txt")
    files = glob.glob(pattern)

    # Define the regex replacements based on the provided mapping
    # Format: (pattern, replacement)
    replacements = [
        (r'mensch', 'mens'),
        (r'Mensch', 'mens'),
        (r'zooals', 'zoals'),
        (r'Zooals', 'Zoals'),
        (r'gansch', 'gans'),
        (r'Gansch', 'Gans'),
        (r'zoo ', 'zo '),
        (r'Zoo ', 'Zo '),
        (r'teeken', 'teken'),
        (r'zooals', 'zoals'),
        (r'Zooals', 'Zoals'),
        (r'zoover', 'zover'),
        (r'roovi', 'rovi'),
        (r'eeren', 'eren'),
        (r'eenig', 'enig'),
    ]

    for file_path in files:
        print(f"Processing: {file_path}")
        
        # Determine the output directory (replace 'merged' with 'regex')
        merged_dir = os.path.dirname(file_path)
        parent_dir = os.path.dirname(merged_dir)
        regex_dir = os.path.join(parent_dir, "regex")
        
        # Ensure the output directory exists
        os.makedirs(regex_dir, exist_ok=True)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Apply each replacement
        for pattern_str, replacement_str in replacements:
            content = re.sub(pattern_str, replacement_str, content)
            
        output_filename = os.path.basename(file_path)
        output_path = os.path.join(regex_dir, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    main()