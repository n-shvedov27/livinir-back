import uuid


class Roommate:
    def __init__(self, username: str, email: str, password: str, uid=None):
        self.id = uuid.uuid4() if uid is None else uid
        self.username = username
        self.email = email
        self.password = password

    def serialize(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "password": self.password,
        }

    @staticmethod
    def deserialize(json):
        return Roommate(
            username=json['username'],
            email=json['email'],
            password=json['password']
        )
