# /home/vic/summa/ai/rewrite.py

import glob
import os
import re

BOOK = "1"  # Assuming we are only dealing with BOOK for KWESTIE files

def dutch_ordinal_to_int(text):
    """
    Parses a Dutch ordinal number string (e.g., "HONDERD EN ZEVENDE") into an integer.
    """
    # Normalize text
    text = text.lower().replace('.', '').replace(',', '')
    words = text.split()
    
    # Mapping of Dutch number words to values
    units = {
        'een': 1, 'eene': 1, 'één': 1, 'eerste': 1,
        'twee': 2, 'tweede': 2,
        'drie': 3, 'derde': 3,
        'vier': 4, 'vierde': 4,
        'vijf': 5, 'vijfde': 5,
        'zes': 6, 'zesde': 6,
        'zeven': 7, 'zevende': 7,
        'acht': 8, 'achtste': 8,
        'negen': 9, 'negende': 9,
        'tien': 10, 'tiende': 10,
        'elf': 11, 'elfde': 11,
        'twaalf': 12, 'twaalfde': 12,
        'dertien': 13, 'dertiende': 13,
        'veertien': 14, 'veertiende': 14,
        'vijftien': 15, 'vijftiende': 15,
        'zestien': 16, 'zestiende': 16,
        'zeventien': 17, 'zeventiende': 17,
        'achttien': 18, 'achttiende': 18,
        'negentien': 19, 'negentiende': 19,
        'twintig': 20, 'twintigste': 20,
        'dertig': 30, 'dertigste': 30,
        'veertig': 40, 'veertigste': 40,
        'vijftig': 50, 'vijftigste': 50,
        'zestig': 60, 'zestigste': 60,
        'zeventig': 70, 'zeventigste': 70,
        'tachtig': 80, 'tachtigste': 80,
        'negentig': 90, 'negentigste': 90,
        'honderd': 100, 'honderdste': 100,
        'duizend': 1000, 'duizendste': 1000
    }

    total = 0
    current_val = 0
    
    for word in words:
        if word == 'en':
            continue
        
        val = units.get(word)
        if val is None:
            # Skip unknown words
            continue
            
        if val == 100 or val == 1000:
            if current_val == 0:
                current_val = 1
            total += current_val * val
            current_val = 0
        else:
            current_val += val
            
    total += current_val
    return total

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    if not lines:
        return

    new_content = []
    iterator = iter(lines)
    kwestie_found = False
    kwestie_number = None
    
    # 1. Find and process the KWESTIE line
    try:
        while True:
            line = next(iterator)
            # Check for the KWESTIE header
            if "KWESTIE" in line:
                # Extract the number part (e.g., "HONDERD EN ZEVENDE" from "HONDERD EN ZEVENDE KWESTIE.")
                match = re.search(r"^(.*?)\s+KWESTIE", line, re.IGNORECASE)
                if match:
                    number_str = match.group(1)
                    number = dutch_ordinal_to_int(number_str)
                    kwestie_number = number
                    # Format as requested: "1.<numeric number>.pr"
                    #new_content.append(f"{BOOK}.{number}.pr")
                    kwestie_found = True
                break
    except StopIteration:
        pass

    # If we didn't find a KWESTIE line, we might want to reset and process from start, 
    # or just abort. Assuming valid files, we proceed.
    if not kwestie_found:
        iterator = iter(lines)

    # 2. Skip Title and Article Count, keep Body
    in_body = False
    
    for line in iterator:
        stripped = line.strip()
        
        # Remove empty lines
        if not stripped:
            continue
            
        if in_body:
            # Reproduce verbatim (preserving indentation if any), but we already skipped empty lines
            new_content.append(line.rstrip())
            continue
            
        # Heuristic: Skip Article count line "(Vijf Artikelen.)"
        if re.match(r"^.?\(.*\bArtikel(en)?\s*\.?\s*\).?$", stripped, re.IGNORECASE):
            in_body = True # The next line starts the body
            continue
            
        # Heuristic: Skip Title (usually fully Uppercase)
        # We check length > 3 to avoid skipping short words if they happen to be upper
        if stripped.isupper() and len(stripped) > 3:
            continue
            
        # If it's not empty, not article count, and not title, it must be the start of the body
        in_body = True
        new_content.append(line.rstrip())

    # Determine output path
    split_dir = os.path.dirname(file_path)
    parent_dir = os.path.dirname(split_dir)
    annotated_dir = os.path.join(parent_dir, "annotated")
    
    if not os.path.exists(annotated_dir):
        os.makedirs(annotated_dir)

    output_filename = f"{BOOK}.{kwestie_number}.-0-pr.txt" if kwestie_number is not None else os.path.basename(file_path)
    output_path = os.path.join(annotated_dir, output_filename)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_content) + '\n')

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.join(script_dir, "../docs/bronbestanden")
    
    # Pattern matches the output of split.py
    pattern = os.path.join(docs_dir, "*", "split", "*kwestie.txt")
    
    files = glob.glob(pattern)
    print(f"Found {len(files)} files to rewrite.")
    
    for file_path in files:
        process_file(file_path)
    
    print("Rewrite complete.")

if __name__ == "__main__":
    main()
