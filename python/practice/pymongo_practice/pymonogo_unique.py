import datetime
import pymongo
from pymongo import MongoClient

client = MongoClient()
print(client.database_names())
db = client['user_profiles']  # DB Creation
# Table Creation which  called collections
result = db.profiles.create_index([('user_id', pymongo.ASCENDING)], unique=True)
print('collection_names  - ', db.collection_names(include_system_collections=False))
print(list(db.profiles.index_information()))

# user_profiles = [
#    {'user_id': 211, 'name': 'Luke'},
#    {'user_id': 212, 'name': 'Ziltoid'}]

# result = db.profiles.insert_many(user_profiles)

new_profile = {'user_id': 213, 'name': 'Drew'}
duplicate_profile = {'user_id': 212, 'name': 'Tommy'}
result = db.profiles.insert_one(duplicate_profile)