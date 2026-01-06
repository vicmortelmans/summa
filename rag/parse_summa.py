import glob
import json
import os
import re
import xml.etree.ElementTree as ET

def parse_summa_files(input_dir, output_file, xml_file):
    """
    Parses text files in the specified directory and outputs a JSON file.
    
    The text files are expected to contain lines with identifiers (e.g., "1.104.1.ad")
    followed by lines of text.
    """
    # Regex to match identifiers:
    # Starts with digits, dots, digits, optional dots/digits, ending with dots/letters.
    # Examples: 1.104.1.ad, 1.103.pr
    identifier_pattern = re.compile(r'^\d+\.\d+(?:\.\d+)?\.[a-z]+$')
    
    parsed_data = []
    
    # Resolve the input directory relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.normpath(os.path.join(script_dir, input_dir))
    
    # Load XML titles
    xml_path = os.path.normpath(os.path.join(script_dir, xml_file))
    titles_map = {}
    if os.path.exists(xml_path):
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            for liber in root.findall('liber'):
                b_idx = liber.get('index')
                for quaestio in liber.findall('quaestio'):
                    q_idx = quaestio.get('index')
                    titles_map[(b_idx, q_idx)] = quaestio.get('title')
                    for articulus in quaestio.findall('articulus'):
                        a_idx = articulus.get('index')
                        titles_map[(b_idx, q_idx, a_idx)] = articulus.get('title')
        except Exception as e:
            print(f"Error parsing XML: {e}")

    def create_entry(ident, text_lines):
        entry = {
            "identifier": ident,
            "text": "\n".join(text_lines).strip()
        }
        parts = ident.split('.')
        if len(parts) >= 2:
            b_idx = parts[0]
            q_idx = parts[1]
            if (b_idx, q_idx) in titles_map:
                entry["quaestio_title"] = titles_map[(b_idx, q_idx)]
            
            if len(parts) == 4: # book.quaestio.articulus.suffix
                a_idx = parts[2]
                if (b_idx, q_idx, a_idx) in titles_map:
                    entry["articulus_title"] = titles_map[(b_idx, q_idx, a_idx)]
        return entry

    search_pattern = os.path.join(target_dir, "*.txt")
    files = sorted(glob.glob(search_pattern))
    
    print(f"Parsing files in: {target_dir}")
    
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        current_id = None
        current_text = []
        
        for line in lines:
            stripped_line = line.strip()
            
            if identifier_pattern.match(stripped_line):
                # Save previous entry
                if current_id is not None:
                    parsed_data.append(create_entry(current_id, current_text))
                
                # Start new entry
                current_id = stripped_line
                current_text = []
            elif current_id is not None:
                # Accumulate text lines
                current_text.append(line.rstrip())
        
        # Save the last entry of the file
        if current_id is not None:
            parsed_data.append(create_entry(current_id, current_text))
            
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, indent=2, ensure_ascii=False)
        
    print(f"Parsed {len(parsed_data)} entries. Output saved to {output_file}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    INPUT_DIRECTORY = os.path.join(script_dir, "../build/geloofsverdediging")
    OUTPUT_FILENAME = os.path.join(script_dir, "./summa_parsed.json")
    XML_FILE = "../build/xml_latin_nl/xml_latin_nl.xml"
    
    parse_summa_files(INPUT_DIRECTORY, OUTPUT_FILENAME, XML_FILE)