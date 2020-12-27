import uuid
from . import Roommate


class Post:
    def __init__(self, text: str, title: str, author: Roommate, date=None, uid=None):
        self.id = uuid.uuid4() if uid is None else uid
        self.text = text
        self.title = title
        self.author = author

    def serialize(self):
        return {
            "id": str(self.id),
            "text": self.text,
            "title": self.title,
            "author": self.author.serialize()
        }
