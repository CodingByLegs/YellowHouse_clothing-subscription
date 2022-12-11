from uuid import UUID


class User:
    id: UUID
    firstName: str
    lastName: str
    phoneNumber: str
    email: str
    address: str
    password = ''

    def __init__(self, json: dict):
        self.id = json['id']
        self.firstName = json['firstName']
        self.lastName = json['lastName']
        self.phoneNumber = json['phoneNumber']
        self.email = json['email']
        self.address = json['address']
        if json['password']:
            self.password = json['password']


