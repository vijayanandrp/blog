
# http://api.mongodb.com/python/current/tutorial.html

import pymongo
from pymongo import MongoClient

client = MongoClient()  # simple connection string that uses the default port to connect
client = MongoClient('localhost', 27017)  # specify port number to connect mongodb
client = MongoClient('mongodb://localhost:27017/')  # Mongo URI


def _(*args):
	return print(args)


# print(dir(client))
print('Database names: ', client.database_names())
# print(client.server_info())
db = client.test_database
import datetime
post = {"author": "Mike",
	"text": "My first blog post!",
	"tags": ["mongodb", "python", "pymongo"],
	"date": datetime.datetime.utcnow()}
print(post)
posts = db.post
post_id = posts.insert_one(post).inserted_id
print(post_id)
db.collection_names(include_system_collections=False)

_(posts.find_one())

_(posts.find_one({"author": "Mike"}))

_(post_id)

_(posts.find_one({"_id": post_id}))

from bson.objectid import ObjectId
# The web framework gets post_id from the URL and passes it as a string

def get(post_id):
	# Convert from string to ObjectId:
	document = client.db.collection.find_one({'_id': ObjectId(post_id)})
	_(document)

print(get('5832bc611fc0c82be8e08b20'))
print(get(post_id))