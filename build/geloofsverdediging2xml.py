#!/usr/bin/python
import sys
import re
import xml.etree.cElementTree as ET

is_id = re.compile("([0-9]+\\.)+[a-z]+")

summa = ET.Element("summa")

def indent(elem, level=0):
    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem        

previous_type = ""
same_type_count = 1

sys.stdin.reconfigure(encoding="utf-8")

for line in sys.stdin:
    if is_id.match(line):
        lemma = ET.SubElement(summa, "lemma")
        split_id = line.split('.')
        if split_id[0] == '0':
            ET.SubElement(lemma, "liber").text = ''
        else:
            ET.SubElement(lemma, "liber").text = split_id[0]
        if split_id[1].isdigit():
            quaestio = split_id[1]
            if split_id[2].isdigit():
                articulus = split_id[2]
                type = split_id[3].rstrip()
            else:
                articulus = ''
                type = split_id[2].rstrip()
        else:
            quaestio = ''
            articulus = ''
            type = split_id[1].rstrip()
        ET.SubElement(lemma, "quaestio").text = quaestio
        ET.SubElement(lemma, "articulus").text = articulus
        ET.SubElement(lemma, "type").text = type
        if type == previous_type:
            same_type_count += 1
        else:
            same_type_count = 1
            previous_type = type
        ET.SubElement(lemma, "index").text = str(same_type_count)
        ET.SubElement(lemma, "reference").text = line.rstrip()
        nl = ET.SubElement(lemma, "nl") 
        nl.text = ''
    else:
        if line:
            nl.text += line.rstrip() + " "

output = '<?xml version="1.0" encoding="UTF-8"?>\n'
output += ET.tostring(indent(summa), method="xml").decode("utf-8")

sys.stdout.write(output)
