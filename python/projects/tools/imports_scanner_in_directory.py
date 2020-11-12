#!/usr/bin/env python3
import os
import re
from collections import Counter
import pandas as pd

"""
This is a simple script to scan the python files in a given directory and reports stats of imports
"""


def grab_imports(file_path):
    if not os.path.isfile(file_path):
        print('Invalid file - ', file_path)

    content = open(file_path).read()
    imports = re.findall('^(import.*)', content, re.MULTILINE) + \
              re.findall('^(from.*)', content, re.MULTILINE)
    return imports


if __name__ == '__main__':
    target_path = ''

    while True:
        if not target_path:
            target_path = input('Enter the directory to scan >> ')
        if not os.path.isdir(target_path):
            print('Sorry, re-enter the valid directory or Press Ctrl+C to quit')
            target_path = None
        else:
            break

    python_files = []
    all_imports = []
    home_path = os.path.abspath(target_path)
    for folder, sub_folder, files in os.walk(target_path):
        for file in files:
            if not file.endswith('.py'):
                continue
            file_path = os.path.join(folder, file)
            python_files.append(file_path)
            _imports = grab_imports(file_path)
            all_imports.extend(_imports)
            if _imports:
                print(file_path.replace(home_path, ''), _imports)

    print('-*-' * 20)
    all_imports.sort()
    imports_stats = Counter(all_imports)
    df_records = []
    print('{:<8} {:<100}'.format('usage', 'import'))
    for key in imports_stats.keys():
        print('{:<8} {:<100} '.format(imports_stats[key], key))
        df_records.append({'count': imports_stats[key], 'import': key})

    df = pd.DataFrame(df_records)
    df.to_excel('imports.xlsx')
