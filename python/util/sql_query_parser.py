import os
import sys
import re

# CONFIG
DATABASE = "DEV_AM"
TEMP_SCHEMA = "PUBLIC"

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


def replace_temp_schema(m):
    return f" {DATABASE}.{TEMP_SCHEMA}.{m.group(1)}"


RENAME = {r"volatile": r"TEMPORARY",
          r"(?s)COLLECT(.*?);": r" ",
          r"(?s)WITH\s*DATA(.*?);": r" ",
          r"(VT_.*)": replace_temp_schema
          }

for key, value in RENAME.items():
    sql_text = re.sub(key, value, sql_text, flags=re.IGNORECASE)

for schema in UNIQUE_SCHEMA:
    if schema.lower().endswith('_eds'):
        sql_text = sql_text.replace('${' + schema.upper() + '}', f"{DATABASE}.EDS")
    if schema.lower().endswith('_stg'):
        sql_text = sql_text.replace('${' + schema.upper() + '}', f"{DATABASE}.STAGE")
    if schema.lower().endswith('_etl'):
        sql_text = sql_text.replace('${' + schema.upper() + '}', f"{DATABASE}.ETL")

# print(sql_text)
SELECT_QUERY = "SELECT COUNT(1) AS TOTAL, '{SCHEMA}' AS TABLE_NAME FROM {SCHEMA}"

FINAL_UNIQUE_SCHEMA_TABLE = list()
for _ in UNIQUE_SCHEMA_TABLE:
    _ = _.split('.')
    if _[0].lower().endswith('_eds'):
        _[0] = f"{DATABASE}.EDS"
    if _[0].lower().endswith('_stg'):
        _[0] = f"{DATABASE}.STAGE"
    if _[0].lower().endswith('_etl'):
        _[0] = f"{DATABASE}.ETL"
    _ = '.'.join(_)
    FINAL_UNIQUE_SCHEMA_TABLE.append(_)

print("\nCOUNT QUERY", "\n", '+' * 20)
final_query = " UNION ALL \n".join([SELECT_QUERY.format(SCHEMA=_) for _ in FINAL_UNIQUE_SCHEMA_TABLE])
final_query += "\n ORDER BY TOTAL ASC"
print(final_query)

output_file = file_name.split('.')[0] + '_snowflake_version.' + file_name.split('.')[1]
with open(output_file, 'w') as fp:
    fp.write(sql_text)
    fp.write('\n\n')
    fp.write("\n--COUNT QUERY")
    fp.write(final_query)
