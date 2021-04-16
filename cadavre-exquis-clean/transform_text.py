import get_text
import re
import random

text = get_text.text
text = text.lower()
replacements = ["wsh", "bref", "genre", "mdr", "ptdr", "jpp"]
newText = ''

def randomponctuation(match):
    ponctuation = random.choice(replacements)
    length = random.randint(0, 6)
    if length == 1:
        length = 0
    if ponctuation == "mdr":
        ponctuation = ponctuation + length*"r"
    if ponctuation == "jpp":
        ponctuation = ponctuation + length*"p"
    print(match.group())
    if match.group() == "," or match.group() == ".":
        ponctuation = " " + ponctuation
    return ponctuation

def randompoints(match):
    length = random.randint(4, 10)
    string = "." * length
    return string

def transform_text_wsh(newText): 
  newText = re.sub("[,;:!?—]", randomponctuation, newText)
  newText = re.sub("(?<!\.)\.(?!\.)", randomponctuation, newText)
  newText = re.sub("\.\.\.", randompoints, newText)
  newText = re.sub("[()\"]|(« | »)", "", newText)
  newText = re.sub("c(’|')est", "c", newText)
  return newText

newText = transform_text_wsh(text)
print(newText)



