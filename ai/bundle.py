import os
import glob
import re

def process_filename(filename):
    """
    Derives the header line from the filename.
    Removes extension, numbers between dashes, and trailing numbers.
    """
    # Remove file extension
    name = os.path.splitext(filename)[0]
    
    # Remove prefix "outputN_"
    name = re.sub(r'^output\d+_', '', name)
    
    # Remove number between dashes (e.g. -4- in 1.107.1.-4-ad)
    name = re.sub(r'-\d+-', '', name)
    
    # Remove number at the end (e.g. .3 in ad.3)
    name = re.sub(r'\.\d+$', '', name)
    
    return name

def main():
    # Path pattern to find corrected directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.join(script_dir, "../docs/bronbestanden")
    search_pattern = os.path.join(docs_dir, '*', 'corrected')
    corrected_dirs = glob.glob(search_pattern)
    
    for corrected_dir in corrected_dirs:
        if not os.path.isdir(corrected_dir):
            print(f"Skipping non-directory: {corrected_dir}")
            continue
            
        # Get parent directory name for the target file
        parent_dir = os.path.dirname(corrected_dir)
        target_name = os.path.basename(parent_dir)
        bundle_dir = os.path.join(parent_dir, 'bundle')
        os.makedirs(bundle_dir, exist_ok=True)
        target_file = os.path.join(bundle_dir, f"{target_name}.txt")
        
        # Find all text files in the corrected directory
        source_files = sorted(glob.glob(os.path.join(corrected_dir, '*.txt')))
        
        if not source_files:
            print(f"No text files found in {corrected_dir}, skipping.")
            continue
            
        with open(target_file, 'w', encoding='utf-8') as outfile:
            for source_file in source_files:
                filename = os.path.basename(source_file)
                header = process_filename(filename)
                
                # Write header line
                outfile.write(f"{header}\n")
                
                # Write file content
                with open(source_file, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    outfile.write(content)
                    
                    # Ensure newline between files
                    if content and not content.endswith('\n'):
                        outfile.write('\n')

if __name__ == "__main__":
    main()
