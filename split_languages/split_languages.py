#!/usr/bin/python
# coding: utf8
import sys
from guess_language import guess_language

for line in sys.stdin:
  lang = guess_language(line)
  sys.stdout.write(lang + ' ' + line)

