#!/usr/bin/python
import sys
import re
import xml.etree.cElementTree as ET

is_id = re.compile("([0-9]+\.)+")

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

same_quaestio_count = 1

for line in sys.stdin:
    if is_id.match(line):
        quaestio = ET.SubElement(summa, "quaestio")
        split_id = line.split('.')
        quaestio.set("liber", str(split_id[0]))
        quaestio.set("index", str(split_id[1]).rstrip())
        same_quaestio_count = 1
    else:
        if line:
            if same_quaestio_count == 1:  # first title is that of the quaestio
                quaestio.set("title", line.decode('utf-8').rstrip() + ' ') 
            else:  # following titles are that of articles 
                articulus = ET.SubElement(quaestio, "articulus")
                articulus.set("title", line.decode('utf-8').rstrip() + ' ')
                articulus.set("index", str(same_quaestio_count - 1)) 
            same_quaestio_count += 1

output = '<?xml version="1.0" encoding="UTF-8"?>\n'
output += (ET.tostring(indent(summa), method="xml"))

sys.stdout.write(output)
