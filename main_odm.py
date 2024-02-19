from mongoengine import *
from password import user, password

connect(db="web_19", host=f"mongodb+srv://{user}:{password}@goitlearn.x6ks5fo.mongodb.net/?retryWrites=true&w=majority")


class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)


class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User)
    tags = ListField(StringField(max_length=30))
    meta = {'allow_inheritance': True}


class TextPost(Post):
    content = StringField()


class ImagePost(Post):
    image_path = StringField()


class LinkPost(Post):
    link_url = StringField()


class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)


if __name__ == "__main__":
    ross = User(email='ross@example.com', first_name='Ross', last_name='Lawley').save()

    vlad = User(email='ross@example.com')
    vlad.first_name = 'Ross'
    vlad.last_name = 'Lawley'
    vlad.save()


    post1 = TextPost(title='Fun with MongoEngine', author=vlad)
    post1.content = 'Took a look at MongoEngine today, looks pretty cool.'
    post1.tags = ['mongodb', 'mongoengine']
    post1.save()

    post2 = LinkPost(title='MongoEngine Documentation', author=ross)
    post2.link_url = 'http://docs.mongoengine.com/'
    post2.tags = ['mongoengine']
    post2.save()
