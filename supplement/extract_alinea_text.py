import json
import re
import html
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path


def normalize_html_text(raw_value):
    """
    Convert HTML-like content to plain text:
    - <br> / <br/> / <br /> -> newline
    - other HTML tags removed
    - multiple consecutive newlines collapsed to one
    """
    if raw_value is None:
        return ""

    text = str(raw_value)

    # Convert <br> to newline
    text = re.sub(r"(?is)<br\s*/?>", "\n", text)

    # Remove all remaining HTML tags
    text = re.sub(r"(?is)<[^>]+>", "", text)

    # Decode HTML entities like &amp; etc.
    text = html.unescape(text)

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove whitespace around newlines
    text = re.sub(r"[ \t]*\n[ \t]*", "\n", text)

    # Collapse multiple adjacent newlines into a single newline
    text = re.sub(r"\n{2,}", "\n", text)

    text = text.strip()
    return text


def find_alinea_text_values(obj, results=None):
    if results is None:
        results = []

    if isinstance(obj, dict):
        if "alinea_text" in obj and obj["alinea_text"] is not None:
            cleaned = normalize_html_text(obj["alinea_text"])
            if cleaned:
                results.append(cleaned)
        for value in obj.values():
            find_alinea_text_values(value, results)
    elif isinstance(obj, list):
        for item in obj:
            find_alinea_text_values(item, results)

    return results


def parse_id(id_line):
    """
    Derive liber, quaestio, articulus, reference, and type from an ID line.
    - liber: always '5'
    - quaestio: derived from 'q. <number>' (or 'ap. <number>' -> 100, 101)
    - articulus: derived from 'a. <number>'
    - reference: the full ID line
    - type: derived from the ID ('arg', 'ad', 'sc', 'co', 'pr')
    """
    liber = "5"
    reference = id_line.strip()

    # Extract quaestio
    qm = re.search(r"\bq\.\s*(\d+)", id_line, re.IGNORECASE)
    apm = re.search(r"\bap\.\s*(\d+)", id_line, re.IGNORECASE)
    if qm:
        quaestio = qm.group(1)
    elif apm:
        quaestio = str(99 + int(apm.group(1)))
    else:
        quaestio = ""

    # Extract articulus
    am = re.search(r"\ba\.\s*(\d+)", id_line, re.IGNORECASE)
    articulus = am.group(1) if am else ""

    # Extract type
    if re.search(r"\bs\.\s*c\.", id_line, re.IGNORECASE) or re.search(r"\bsc\b", id_line, re.IGNORECASE):
        lemma_type = "sc"
    elif re.search(r"\bco\.", id_line, re.IGNORECASE) or re.search(r"\bco\b", id_line, re.IGNORECASE):
        lemma_type = "co"
    elif re.search(r"\bpr\.", id_line, re.IGNORECASE) or re.search(r"\bpr\b", id_line, re.IGNORECASE):
        lemma_type = "pr"
    elif re.search(r"\bad\b", id_line, re.IGNORECASE):
        lemma_type = "ad"
    elif re.search(r"\barg\.", id_line, re.IGNORECASE) or re.search(r"\barg\b", id_line, re.IGNORECASE):
        lemma_type = "arg"
    else:
        lemma_type = ""

    return liber, quaestio, articulus, reference, lemma_type


def load_entries(input_path):
    """
    Load (id_line, content) pairs from either a JSON file or a TXT file.
    """
    path = Path(input_path)
    with path.open("r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            values = [v for v in find_alinea_text_values(data) if v]
            entries = []
            for v in values:
                lines = v.split("\n")
                id_line = lines[0].strip()
                content = " ".join(line.strip() for line in lines[1:] if line.strip())
                entries.append((id_line, content))
            return entries
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass

    # If not JSON, parse as TXT file
    with path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    entries = []
    cur_id = None
    cur_content = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if re.match(r"^(?:Suppl\s+)?(?:q|ap)\.\s*\d+", line, re.IGNORECASE):
            if cur_id is not None:
                entries.append((cur_id, " ".join(cur_content)))
            cur_id = line
            cur_content = []
        else:
            if cur_id is not None:
                cur_content.append(line)
    if cur_id is not None:
        entries.append((cur_id, " ".join(cur_content)))

    return entries


def build_summa_xml(entries):
    """
    Convert a list of (id_line, content) tuples into an XML ElementTree root (<summa>).
    Tracks index as the sequence number of subsequent items of the same type.
    """
    root = ET.Element("summa")
    previous_type = None
    previous_section = None
    same_type_count = 1

    for id_line, content in entries:
        liber, quaestio, articulus, reference, lemma_type = parse_id(id_line)

        section = (quaestio, articulus)
        if lemma_type == previous_type and section == previous_section:
            same_type_count += 1
        else:
            same_type_count = 1
            previous_type = lemma_type
            previous_section = section

        index = str(same_type_count)

        lemma = ET.SubElement(root, "lemma")
        ET.SubElement(lemma, "liber").text = liber
        ET.SubElement(lemma, "quaestio").text = quaestio
        ET.SubElement(lemma, "articulus").text = articulus
        ET.SubElement(lemma, "reference").text = reference
        ET.SubElement(lemma, "type").text = lemma_type
        ET.SubElement(lemma, "index").text = index
        ET.SubElement(lemma, "latin").text = content

    ET.indent(root, space="  ")
    return root


def main():
    parser = argparse.ArgumentParser(
        description="Extract alinea_text values from JSON or TXT and write them as XML lemmas."
    )
    parser.add_argument("input_file", help="Path to the source JSON or TXT file")
    parser.add_argument("output_xml", help="Path to the output XML file")
    args = parser.parse_args()

    input_path = Path(args.input_file)
    output_path = Path(args.output_xml)

    entries = load_entries(input_path)
    root = build_summa_xml(entries)

    xml_header = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_body = ET.tostring(root, encoding="utf-8").decode("utf-8")
    output_text = xml_header + xml_body + "\n"

    with output_path.open("w", encoding="utf-8") as f:
        f.write(output_text)

    print(f"Extracted {len(entries)} lemmas to {output_path}")


if __name__ == "__main__":
    main()