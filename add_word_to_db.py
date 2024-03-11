from bot.model import Word
from bot.common import session

file1 = open("test100.txt", "r")
lines = [line.rstrip() for line in file1]
file2 = open("translate.txt", "r", encoding='utf-8')
lines_t  = [line.rstrip() for line in file2]
print(lines_t)
file1.close()
file2.close()

for num, word in enumerate(lines):
    session.add(Word(value=word, translate=lines_t[num], package_id=1))
session.commit()