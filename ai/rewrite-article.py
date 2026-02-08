# /home/vic/summa/ai/rewrite-article.py

import glob
import os
import re

BOOK = "1"  # Assuming we are only dealing with BOOK for KWESTIE files

def roman_to_int(s):
    """
    Parses a Roman numeral string into an integer.
    """
    s = s.upper().strip()
    roman = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    val = 0
    for i in range(len(s)):
        if i > 0 and roman[s[i]] > roman[s[i - 1]]:
            val += roman[s[i]] - 2 * roman[s[i - 1]]
        else:
            val += roman[s[i]]
    return val

def dutch_ordinal_to_int(text):
    """
    Parses a Dutch ordinal number string (e.g., "HONDERD EN ZEVENDE") into an integer.
    Copied from rewrite.py to ensure standalone functionality.
    """
    text = text.lower().replace('.', '').replace(',', '')
    words = text.split()
    
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

def get_question_number(current_file_path):
    """
    Finds the preceding 'kwestie.txt' file in the split directory and extracts the question number.
    """
    split_dir = os.path.dirname(current_file_path)
    current_filename = os.path.basename(current_file_path)
    
    files = sorted(os.listdir(split_dir))
    last_kwestie = None
    
    for f in files:
        if f == current_filename:
            break
        if f.endswith("kwestie.txt"):
            last_kwestie = f
            
    if last_kwestie:
        base = os.path.splitext(last_kwestie)[0]
        parts = base.split('_', 1)
        slug = parts[1] if len(parts) > 1 else parts[0]
        if slug.endswith("-kwestie"):
            slug = slug[:-8]
        return dutch_ordinal_to_int(slug.replace('-', ' '))
    return None

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    if not lines:
        return

    q_num = get_question_number(file_path)
    q_str = str(q_num) if q_num else "x"

    article_num = None
    
    # Output directory setup
    split_dir = os.path.dirname(file_path)
    parent_dir = os.path.dirname(split_dir)
    annotated_dir = os.path.join(parent_dir, "annotated")
    
    if not os.path.exists(annotated_dir):
        os.makedirs(annotated_dir)
    
    # State tracking
    state = 0
    
    # Flags to handle unnumbered first items
    first_arg_started = False
    first_ad_started = False
    
    current_lines = []
    current_filename = None
    
    def write_current_section():
        nonlocal current_lines, current_filename
        if current_filename and current_lines:
            output_path = os.path.join(annotated_dir, current_filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(current_lines) + '\n')
        current_lines = []
        current_filename = None

    iterator = iter(lines)
    
    try:
        while True:
            line = next(iterator).strip()
            if not line:
                continue
            
            # --- State 0: Header/Title ---
            if state == 0:
                # Check for ARTIKEL header (e.g. "Ie ARTIKEL.")
                match = re.match(r"^#*\s*([IVX]+)(e|.|er|°)?\s+ARTIKEL", line, re.IGNORECASE)
                if match:
                    article_num = roman_to_int(match.group(1))
                    continue # Skip this line
                
                # Check for Objections start to transition state
                if re.match(r"^\**(BEDENKINGEN|Men beweert)", line, re.IGNORECASE):
                    state = 1
                    # Fall through to process this line in state 1
                else:
                    # Assume Title or other preamble, skip
                    continue

            # --- State 1: Objections ---
            if state == 1:
                # Check for transition to SC
                if re.match(r"^Daartegenover", line, re.IGNORECASE):
                    write_current_section()
                    state = 2
                    # Fall through to process this line in state 2
                else:
                    # Check for trigger words to remove (BEDENKINGEN)
                    trigger_match = re.match(r"^\**(BEDENKINGEN)[\.\*\s—]*", line, re.IGNORECASE)
                    if trigger_match:
                        line = line[trigger_match.end():].strip()
                    
                    # Filter out "— 1." if present (often in first objection)
                    line = re.sub(r"^—\s*1\.\s*", "", line).strip()

                    if not line:
                        continue

                    # Check for numbered objection (e.g. "1. ...")
                    num_match = re.match(r"^(\d+)\.\s*", line)
                    if num_match:
                        write_current_section()
                        line = line[num_match.end():].strip()
                        arg_num = int(num_match.group(1))
                        current_filename = f"{BOOK}.{q_str}.{article_num}.-1-arg.{arg_num}.txt"
                        #current_lines = [f"{BOOK}.{q_str}.{article_num}.arg", line]
                        current_lines.append(line)
                        first_arg_started = True
                    else:
                        # Unnumbered line. 
                        # If it's the first objection (and unnumbered), emit tag.
                        # Otherwise it's a continuation of the previous objection.
                        if not first_arg_started:
                            write_current_section()
                            arg_num = 1
                            current_filename = f"{BOOK}.{q_str}.{article_num}.-1-arg.{arg_num}.txt"
                            #current_lines = [f"{BOOK}.{q_str}.{article_num}.arg", line]
                            current_lines.append(line)
                            first_arg_started = True
                        else:
                            current_lines.append(line)
                    continue

            # --- State 2: Sed Contra ---
            if state == 2:
                # Check for transition to Body
                if re.match(r"^\**LEERSTELLING", line, re.IGNORECASE):
                    write_current_section()
                    state = 3
                    # Fall through to process this line in state 3
                else:
                    if current_filename is None:
                        current_filename = f"{BOOK}.{q_str}.{article_num}.-2-sc.txt"
                        #current_lines = [f"{BOOK}.{q_str}.{article_num}.sc", line]
                        current_lines.append(line)
                    else:
                        current_lines.append(line)
                    continue

            # --- State 3: Body ---
            if state == 3:
                # Check for transition to Answers
                if re.search(r"(^\**ANTW..RD OP DE BEDENKINGEN|antwoord op de bedenkingen)", line, re.IGNORECASE):
                    write_current_section()
                    state = 4
                    # Fall through to process this line in state 4
                else:
                    # Handle Body line
                    trigger_match = re.match(r"^\**LEERSTELLING[\.\*\s—]*", line, re.IGNORECASE)
                    if trigger_match:
                        line = line[trigger_match.end():].strip()
                        current_filename = f"{BOOK}.{q_str}.{article_num}.-3-co.txt"
                        #current_lines = [f"{BOOK}.{q_str}.{article_num}.co"]
                        if line:
                            current_lines.append(line)
                    else:
                        if current_filename is None:
                            current_filename = f"{BOOK}.{q_str}.{article_num}.-3-co.txt"
                            #current_lines = [f"{BOOK}.{q_str}.{article_num}.co", line]
                            current_lines.append(line)
                        else:
                            current_lines.append(line)
                    continue

            # --- State 4: Answers ---
            if state == 4:
                # Remove trigger if present
                trigger_match = re.match(r"^\**ANTW..RD OP DE BEDENKINGEN[\.\*\s—]*", line, re.IGNORECASE)
                if trigger_match:
                    line = line[trigger_match.end():].strip()
                
                if not line:
                    continue

                # Check for numbered answer
                num_match = re.match(r"^(\d+)\.\s*", line)
                if num_match:
                    write_current_section()
                    line = line[num_match.end():].strip()
                    ad_num = int(num_match.group(1))
                    current_filename = f"{BOOK}.{q_str}.{article_num}.-4-ad.{ad_num}.txt"
                    #current_lines = [f"{BOOK}.{q_str}.{article_num}.ad", line]
                    current_lines.append(line)
                    first_ad_started = True
                else:
                    # Unnumbered line.
                    if not first_ad_started:
                        write_current_section()
                        ad_num = 1
                        current_filename = f"{BOOK}.{q_str}.{article_num}.-4-ad.{ad_num}.txt"
                        #current_lines = [f"{BOOK}.{q_str}.{article_num}.ad", line]
                        current_lines.append(line)
                        first_ad_started = True
                    else:
                        current_lines.append(line)
                continue

    except StopIteration:
        pass

    write_current_section()

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.join(script_dir, "../docs/bronbestanden")
    
    # Pattern matches the output of split.py for articles
    pattern = os.path.join(docs_dir, "*", "split", "*artikel.txt")
    
    files = glob.glob(pattern)
    print(f"Found {len(files)} files to rewrite.")
    
    for file_path in files:
        process_file(file_path)
    
    print("Rewrite complete.")

if __name__ == "__main__":
    main()
