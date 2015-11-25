import os
import re

def fileNameCheckInsert(fileName, fileNameList):
    '''
    Функція для визначення нового імені файла при його завантаженні
    Повне ім'я файла порівнюється із списком наявних імен.
    При співпадінні ім'я файла (перед розширенням) доповнюється
    номером копії у дужках, наприклад "qwerty (1).py"
    Якщо виявиться, що подібні назви вже існуть, буде знайдено
    найбільший номер копії, наприклад "qwerty (3).py"
    Функція повертає нову або стару назву файла
    а також доповнює змінюваний список файлів.
    '''
    if fileName in fileNameList:
        (name, ext) = os.path.splitext(fileName)
        pattern = '\((?P<xxx>\d+)\)'.join((re.escape(name+" "), re.escape(ext)))
        print(pattern)
        pattern = re.compile(pattern)
        print(pattern)
        i = 0
        for f in fileNameList:
            s = re.search(pattern, f)
            if s:
                j = int(s.group('xxx'))
                i = max(i,j)
                print(s,j)
        s = " (%s)" % (i+1)
        fileName = s.join((name, ext))
    fileNameList.append(fileName)
    return fileName

fileNameList = [
    'alfa.abc',
    'beta.cde',
    'beta (1).cde',
    'beta (2).cde',
]
fileName = 'beta.cde'
print(fileName)
fileName = fileNameCheckInsert(fileName, fileNameList)
print(fileName)
