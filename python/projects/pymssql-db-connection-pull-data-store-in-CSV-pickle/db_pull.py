import csv
import pymssql
import pickle

# Connection Config with MS SQL Windows
conn = pymssql.connect(
    host=r"172.0.0.0",  # Ip Address or Host name
    user=r'DOMAIN\vijay-works',    # Domain\user_name
    password=r'enter your password',    # password
    database='sample' # Database name
)

# Initiate DB Connection
cursor = conn.cursor()
print('[+] Connected with DB ')

# Query to be executed
query = """SELECT  [Category]
      ,[Source Value]
      ,[Corrected Value] FROM dbo.sample where Category='Age'"""


# Execute the query
cursor.execute(query)
print('[+] Executed Query')

# Writes the rows in a CSV File
with open("age.csv", "w") as outfile:
    writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
    for row in cursor:
        writer.writerow(row)

# Execute the query
cursor.execute(query)
print('[+] Executed Query 2nd time')

age_data = []
age_pickle = open("age.pickle", "wb")
# Writes the rows in a list
for row in cursor:
    age_data.append(row)

# dumping age_data to a pickle file
pickle.dump(age_data, age_pickle)
age_pickle.close()
print('[+] Dumped as a pickle file ')

# Close the cursor and the database connection
cursor.close()
conn.close()

# debug
print(age_data)
