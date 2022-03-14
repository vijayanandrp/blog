import os
import sys
import re

get_cwd = os.path.dirname(__file__)

print(f"Current working directory - {get_cwd}")

if len(sys.argv) <= 1:
    print("Exit: No query filename or path found ...")
    exit()

file_name = sys.argv[1]

if not os.path.isfile(file_name):
    file_name = os.path.join(get_cwd, file_name)
    if not os.path.isfile(file_name):
        print(f"Exit: File not found .. {file_name}")
        exit()

sql_text = open(file_name).read()

# print(sql_text)

TABLE_PATTERN = r"\$\{(.*)\}\.([a-zA-Z0-9_]*)"

result = re.findall(TABLE_PATTERN, sql_text)

UNIQUE_SCHEMA = list()
UNIQUE_TABLE = list()
UNIQUE_SCHEMA_TABLE = list()

for s in result:
    if not len(s) == 2:
        continue
    UNIQUE_SCHEMA.append(s[0])
    UNIQUE_TABLE.append(s[1])
    UNIQUE_SCHEMA_TABLE.append(s[0] + '.' + s[1])


def set_list(tl):
    _l = list(set([x.upper().strip() for x in tl if x.strip()]))
    _l.sort()
    return _l


UNIQUE_TABLE = set_list(UNIQUE_TABLE)
UNIQUE_SCHEMA = set_list(UNIQUE_SCHEMA)
UNIQUE_SCHEMA_TABLE = set_list(UNIQUE_SCHEMA_TABLE)

print("\nTABLES\n", '+' * 20)
for _ in UNIQUE_TABLE:
    print(_)

print("\nSCHEMA", "\n", '+' * 20)
for _ in UNIQUE_SCHEMA:
    print(_)

print("\nSCHEMA TABLE", "\n", '+' * 20)
for _ in UNIQUE_SCHEMA_TABLE:
    print(_)

RENAME = {r"volatile": r"temporary"}

for key, value in RENAME.items():
    sql_text = re.sub(key.upper(), value.upper(), sql_text.upper(), re.MULTILINE)

for schema in UNIQUE_SCHEMA:
    if schema.lower().endswith('_eds'):
        sql_text = sql_text.replace('${' + schema.upper() + '}', "DEV_AM.EDS")
    if schema.lower().endswith('_stg'):
        sql_text = sql_text.replace('${' + schema.upper() + '}', "DEV_AM.STAGE")

# print(sql_text)

output_file = file_name.split('.')[0] + '_modified.' + file_name.split('.')[1]
with open(output_file, 'w') as fp:
    fp.write(sql_text)
    fp.write('\n')
