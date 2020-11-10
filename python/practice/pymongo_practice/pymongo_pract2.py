import datetime

from pymongo import MongoClient

client = MongoClient()
print('Dbs : ', client.database_names())
db = client['try2']
posts = db.post
post1 = db.post1
post = {"author": "Mike",
	"text": "My first blog post!",
	"tags": ["mongodb", "python", "pymongo"],
	"date": datetime.datetime.utcnow()}

post_id = posts.insert_one(post).inserted_id
print(post_id)

post_id1 = post1.insert_one(post).inserted_id
print(post_id1)
print('*'*120)
print('collection_names  - ', db.collection_names(include_system_collections=False))
print('*'*120)
for post in post1.find():
	print(post)
print('*'*120)
for post in posts.find():
	print(post)
print('*'*120)

new_posts = [{"author": "Mike",
               "text": "Another post!",
               "tags": ["bulk", "insert"],
               "date": datetime.datetime(2009, 11, 12, 11, 14)},
              {"author": "Eliot",
               "title": "MongoDB is fun",
               "text": "and pretty easy too!",
               "date": datetime.datetime(2009, 11, 10, 10, 45)}]

result = posts.insert_many(new_posts)
print(result.inserted_ids)

for post in posts.find({"author": "Eliot"}):
	print(post)

print(posts.count())

d = datetime.datetime(2009, 11, 12, 12)

for post in posts.find({"date": {"$lt": d}}).sort("author"):
	print(post)