#!/usr/bin/env python3
"""
Convert full_depth_structure.json to a text file containing the Latin titles
of quaestiones and articuli of the Summa Theologiae.

The four parts are assigned numbers 1 to 4.
Before each quaestio title, a line is added with:
  <part_number>.<quaestio_number> (e.g. "2.35")
followed by the quaestio's title_latin, and each articulus's title_latin underneath.
"""

import argparse
import json
import os
import sys


def find_parts(data):
    """
    Locate the 4 'part' elements in the hierarchical JSON structure.
    Handles direct Next.js flight data format (e.g. data['2f'][3]['parts']),
    standard dictionaries, or recursive search.
    """
    # 1. Direct Next.js flight data structure check
    if isinstance(data, dict):
        if "2f" in data and isinstance(data["2f"], list) and len(data["2f"]) > 3:
            candidate = data["2f"][3]
            if isinstance(candidate, dict) and "parts" in candidate:
                parts = candidate["parts"]
                if isinstance(parts, list) and len(parts) == 4:
                    return parts

        # 2. Direct 'parts' key
        if "parts" in data and isinstance(data["parts"], list):
            parts = data["parts"]
            if len(parts) == 4 and all(isinstance(p, dict) and p.get("type") == "part" for p in parts):
                return parts

    # 3. Direct list of parts
    if isinstance(data, list) and len(data) == 4:
        if all(isinstance(p, dict) and p.get("type") == "part" for p in data):
            return data

    # 4. Recursive search
    if isinstance(data, dict):
        for v in data.values():
            found = find_parts(v)
            if found is not None:
                return found
    elif isinstance(data, list):
        for item in data:
            found = find_parts(item)
            if found is not None:
                return found

    return None


def extract_titles(parts):
    """
    Extract quaestio and articulus Latin titles from the parts hierarchy.

    Returns:
        lines: list of strings (numbering lines and Latin titles)
        stats: dict containing counts of parts, quaestiones, and articuli
    """
    # Ensure parts are sorted by sort_order if present
    sorted_parts = sorted(parts, key=lambda p: p.get("sort_order", 0))

    lines = []
    total_q = 0
    total_art = 0

    for part_idx, part in enumerate(sorted_parts, start=1):
        q_idx = 0
        for child in part.get("children", []):
            if child.get("type") == "quaestio":
                q_idx += 1
                q_num = child.get("num", q_idx)
                total_q += 1

                # Add part.quaestio line (e.g., "2.35")
                lines.append(f"{part_idx}.{q_num}")

                # Add quaestio title_latin
                q_title = child.get("title_latin")
                if q_title:
                    lines.append(q_title.strip())

                # Add articulus title_latin for each articulus under this quaestio
                for art in child.get("children", []):
                    if art.get("type") == "articulus":
                        total_art += 1
                        art_title = art.get("title_latin")
                        if art_title:
                            lines.append(art_title.strip())

    stats = {
        "parts": len(sorted_parts),
        "quaestiones": total_q,
        "articuli": total_art,
        "lines": len(lines),
    }
    return lines, stats


def resolve_input_path(input_arg):
    """Resolve input file path checking current directory and script directory."""
    if input_arg and os.path.exists(input_arg):
        return input_arg

    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)

    candidates = []
    if input_arg:
        candidates.extend([
            input_arg,
            os.path.join(script_dir, input_arg),
            os.path.join(workspace_root, input_arg),
            os.path.join(workspace_root, "supplement", input_arg),
        ])
    else:
        candidates.extend([
            "full_depth_structure.json",
            os.path.join(script_dir, "full_depth_structure.json"),
            os.path.join("supplement", "full_depth_structure.json"),
            os.path.join(workspace_root, "supplement", "full_depth_structure.json"),
        ])

    for path in candidates:
        if os.path.isfile(path):
            return os.path.abspath(path)

    return None


def convert(input_path, output_path):
    """Read full_depth_structure.json and write Latin titles to output_path."""
    print(f"Loading JSON from: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    parts = find_parts(data)
    if not parts:
        raise ValueError("Could not find the 4 'part' elements in the JSON file.")

    lines, stats = extract_titles(parts)

    output_dir = os.path.dirname(os.path.abspath(output_path))
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(
        f"Successfully extracted:\n"
        f"  - Parts:       {stats['parts']}\n"
        f"  - Quaestiones: {stats['quaestiones']}\n"
        f"  - Articuli:    {stats['articuli']}\n"
        f"  - Total lines: {stats['lines']}\n"
        f"Output saved to: {output_path}"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Convert full_depth_structure.json to a text file with Latin titles of quaestiones and articuli."
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        default=None,
        help="Path to full_depth_structure.json (optional, defaults to searching automatically)",
    )
    parser.add_argument(
        "output_file",
        nargs="?",
        default=None,
        help="Path to output text file (optional, defaults to 'latin_titles.txt')",
    )
    parser.add_argument(
        "-i", "--input",
        dest="input_flag",
        default=None,
        help="Input JSON file path",
    )
    parser.add_argument(
        "-o", "--output",
        dest="output_flag",
        default=None,
        help="Output text file path",
    )

    args = parser.parse_args()

    input_arg = args.input_flag or args.input_file
    output_arg = args.output_flag or args.output_file

    input_path = resolve_input_path(input_arg)
    if not input_path:
        search_target = input_arg or "full_depth_structure.json"
        print(f"Error: Could not find input file '{search_target}'.", file=sys.stderr)
        sys.exit(1)

    if not output_arg:
        # Default to latin_titles.txt in the same directory as the input file
        output_dir = os.path.dirname(input_path)
        output_path = os.path.join(output_dir, "latin_titles.txt")
    else:
        output_path = output_arg

    convert(input_path, output_path)


if __name__ == "__main__":
    main()
