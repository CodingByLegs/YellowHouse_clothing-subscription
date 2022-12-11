from uuid import UUID


class Clothes:
    id: UUID
    type: str
    name: str
    size: int
    price: int
    inCapsula: bool
    wear: int
    status: int
    coolKoef: int
    capsulesWereThisClothesIds: list

    def __init__(self, json: dict):
        self.id = json['id']
        self.type = json['type']
        self.name = json['name']
        self.size = json['size']
        self.price = json['price']
        self.inCapsula = json['inCapsula']
        self.wear = json['wear']
        self.status = json['status']
        self.coolKoef = json['coolKoef']
        self.capsulesWereThisClothesIds = list(json['capsulesWereThisClothesIds'])