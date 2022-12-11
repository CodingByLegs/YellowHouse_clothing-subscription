from uuid import UUID


class Capsule:
    id: UUID
    type: str
    size: str
    price: str
    clothesSize: str
    status: str
    clothesInCapsulaIds: list

    def __init__(self, json: dict):
        self.id = json['id']
        self.type = json['type']
        self.price = json['price']
        self.size = json['price']
        self.clothesSize = json['clothesSize']
        self.status = json['status']
        self.clothesInCapsulaIds = list(json['clothesInCapsulaIds'])