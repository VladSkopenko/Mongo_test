from password import password, user
from pymongo.mongo_client import MongoClient

uri = f"mongodb+srv://{user}:{password}@goitlearn.x6ks5fo.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)
db = client.web_19


db.cats.insert_one(

        {"name": "Oleg",
         "age": 22,
         "Ya": "Love",
         }


)

