#!/usr/bin/python3
# coding: utf8
import sys
from guess_language import guess_language

for line in sys.stdin:
  lang = guess_language(line, hints=['nl','la'])
  sys.stdout.write(lang + ' ' + line)

