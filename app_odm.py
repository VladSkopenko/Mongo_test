from mongoengine import connect, Document, EmbeddedDocument, StringField, IntField, ListField, DoesNotExist
from password import user, password
from bson.objectid import ObjectId
from argparse import ArgumentParser
from tabulate import tabulate
from colorama import Fore, Back, Style

connect(db="web_19", host=f"mongodb+srv://{user}:{password}@goitlearn.x6ks5fo.mongodb.net/?retryWrites=true&w=majority")

parser = ArgumentParser(description="Test with cats and oleg")
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


class Cat(Document):
    name = StringField(required=True, max_length=50)
    age = IntField(min_value=1, max_value=50)
    features = ListField(StringField(max_length=150))
    meta = {"collection": "cats"}


def create(name, age, features):
    result = Cat(name=name, age=age, features=features).save()
    return result


def find():
    return Cat.objects.all()


def delete_of(pk):
    try:
        cat = Cat.objects.get(id=pk)
        cat.delete()
        return cat
    except DoesNotExist :
        return None


def update(pk_cate, name_cate: str, age_cate: int, features_cate: list[str, ...]) -> None or ObjectId:
    cat = Cat.objects(id=pk_cate).first()
    if cat:
        cat.update(name=name_cate, age=age_cate, features=features_cate)
        cat.reload()
    return cat

def main():
    match action:
        case "create":
            result = create(name, age, features)
            print(result.to_mongo().to_dict())

        case "read":
            r = find()
            table = tabulate([e.to_mongo().to_dict() for e in r], headers="keys", tablefmt="grid")
            header = f"{Fore.GREEN}{Back.WHITE}{Style.BRIGHT}"
            table_colored = header + table.replace('\n', f"{Style.RESET_ALL}\n{header}") + Style.RESET_ALL
            print(table_colored)
        case "update":
            result = update(pk, name, age, features)
            print(result.to_mongo().to_dict())

        case "delete":
            result = delete_of(pk)
            print(result.to_mongo().to_dict())
        case _:
            print("Unknown command")
if __name__ == "__main__":
    main()