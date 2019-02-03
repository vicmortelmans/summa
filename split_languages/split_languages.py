#!/usr/bin/python3
# coding: utf8
import sys
from guess_language import guess_language

current_line = ''
next_line = ''
current_lang = 'UNKNOWN'
next_lang = 'UNKNOWN'

for line in sys.stdin:
  previous_line = current_line
  current_line = next_line
  next_line = line
  previous_lang = current_lang
  current_lang = next_lang
  next_lang = guess_language(next_line, hints=['nl','la'])
  if current_lang == 'nl':
    sys.stdout.write(current_line)
  if current_lang == 'UNKNOWN' and (previous_lang == 'nl' or next_lang == 'nl'):
    sys.stdout.write(current_line)

# I never care about the last line of a file
