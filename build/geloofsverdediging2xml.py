#!/usr/bin/python
import sys
import re
import xml.etree.cElementTree as ET
import codecs

is_id = re.compile("([0-9]+\.)+[a-z]+")

summa = ET.Element(u"summa")

def indent(elem, level=0):
    i = u"\n" + level*u"  "
    j = u"\n" + (level-1)*u"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + u"  "
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

previous_type = u""
same_type_count = 1

sys.stdin = codecs.getreader("utf-8")(sys.stdin)

for line in sys.stdin:
    if is_id.match(line):
        lemma = ET.SubElement(summa, u"lemma")
        split_id = line.split(u'.')
        if split_id[0] == '0':
            ET.SubElement(lemma, u"liber").text = ''
        else:
            ET.SubElement(lemma, u"liber").text = split_id[0]
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
        ET.SubElement(lemma, u"quaestio").text = quaestio
        ET.SubElement(lemma, u"articulus").text = articulus
        ET.SubElement(lemma, u"type").text = type
        if type == previous_type:
            same_type_count += 1
        else:
            same_type_count = 1
            previous_type = type
        ET.SubElement(lemma, u"index").text = str(same_type_count)
        ET.SubElement(lemma, u"reference").text = line .rstrip()
        nl = ET.SubElement(lemma, u"nl") 
        nl.text = ''
    else:
        if line:
            nl.text += line.rstrip() + u" "

output = '<?xml version="1.0" encoding="UTF-8"?>\n'
output += (ET.tostring(indent(summa), method="xml"))

sys.stdout.write(output)
