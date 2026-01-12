# Reads text files from ../docs/bronbestanden/*/*.txt and writes filtered Dutch text to *.nl.txt in the same directory.

import glob
import os
import re
import pycld2

script_dir = os.path.dirname(os.path.abspath(__file__))
docs_dir = os.path.join(script_dir, "../docs/bronbestanden")

# Iterate all txt-files matching "../docs/bronbestanden/*/*.txt"
txt_files = glob.glob(os.path.join(docs_dir, "*", "*.txt"))

for file_path in txt_files:
    # Skip output files if they happen to be in the list
    if file_path.endswith(".nl.txt"):
        continue

    print(f"Processing: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split content into paragraphs based on double newlines
    paragraphs = content.split("\n\n")
    dutch_paragraphs = []
    latin_count = 0
    first_dutch_found = False

    for p in paragraphs:
        if not p.strip():
            continue

        # Skip paragraphs that are only hyphens
        if p.strip().replace("-", "") == "":
            continue

        # Skip paragraphs that start with a number surrounded by brackets
        if re.match(r"^\s*\(\d+\)", p):
            continue
        
        try:
            # Detect language
            is_reliable, _, details = pycld2.detect(p)
            # details[0] is the top prediction: (name, code, percent, score)
            top_lang_code = details[0][1]

            # Skip leading paragraphs that start with "Kw." until we find the first Dutch one
            if not first_dutch_found:
                if top_lang_code == 'nl':
                    first_dutch_found = True
                elif p.strip().startswith("Kw.") or p.strip().isdigit():
                    continue

            # Filter away Latin ('la'). Keep Dutch ('nl') and others (e.g. 'un' for numbers/headers)
            if top_lang_code == 'la':
                latin_count += 1
                if latin_count >= 2:
                    break
            else:
                if top_lang_code == 'nl' or not latin_count:
                    dutch_paragraphs.append(p)
        except Exception as e:
            print(f"Warning: Language detection failed for a paragraph in {file_path}: {e}")
            dutch_paragraphs.append(p)

    output_path = file_path[:-4] + ".nl.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(dutch_paragraphs))