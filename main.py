import argparse

from bson.objectid import ObjectId
from password import password, user
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from tabulate import tabulate
from colorama import Fore, Style, Back

uri = f"mongodb+srv://{user}:{password}@goitlearn.x6ks5fo.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi("1"))
db = client.web_19

parser = argparse.ArgumentParser(description="Test with cats and oleg")
parser.add_argument("--action", help="create, update, read, delete")  # CRUD
parser.add_argument("--id")
parser.add_argument("--name")
parser.add_argument("--age")
parser.add_argument("--features", nargs="+")

arg = vars(parser.parse_args())
action = arg.get("action")
age = arg.get("age")
pk = arg.get("id")
name = arg.get("name")
features = arg.get("features")


def find():
    return db.cats.find()


def create(name, age, features):
    result = db.cats.insert_one({
        "name": name,
        "age": int(age),
        "features": features,
    })
    return result


def update(pk, name, age, features):
    result = db.cats.update_one({"_id": ObjectId(pk)}, {
        "$set": {                    #Это надо щоб если що была не замена полная а именно модификация
            "name": name,
            "age": int(age),
            "features": features,
        }
    })
    return result


def delete_of(pk):
    result = db.cats.delete_one({"_id": ObjectId(pk)})
    return result




def main():
    match action:
        case "create":
            r = create(name, age, features)
            print((r))

        case "read":
            r = find()
            table = tabulate([e for e in r], headers="keys", tablefmt="grid")
            header = f"{Fore.GREEN}{Back.WHITE}{Style.BRIGHT}"
            table_colored = header + table.replace('\n', f"{Style.RESET_ALL}\n{header}") + Style.RESET_ALL
            print(table_colored)

        case "update":
            result = update(pk, name, age, features)
            print(result)

        case "delete":
            result = delete_of(pk)
            print(result)
        case _:
            print("Unknown command")


if __name__ == "__main__":
    main()
