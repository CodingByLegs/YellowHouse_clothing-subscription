from uuid import UUID


class Order:
    id: UUID
    userId: UUID
    capsuleId: UUID
    price: str
    size: str
    deliveryDateToClient: str
    deliveryDateBack: str

    def __init__(self, json: dict):
        self.id = json['id']
        self.userId = json['userId']
        self.capsuleId = json['capsuleId']
        self.price = json['price']
        self.size = json['size']
        self.deliveryDateToClient = json['deliveryDateToClient']
        self.deliveryDateBack = json['deliveryDateBack']