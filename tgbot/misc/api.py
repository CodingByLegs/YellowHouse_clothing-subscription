import logging

import requests


from tgbot.config import API_data, load_config
from tgbot.models.capsule import Capsule
from tgbot.models.order import Order
from tgbot.models.user import User

logger = logging.getLogger(__name__)

class API:
    api: API_data
    config = load_config(".env")
    api = config.api

    def getUsers(self):
        response = requests.get(self.api.url + '/users')
        users = []
        for item in response.json():
            users.append(User(item))
        return users

    def getUserByPhoneNumber(self, phoneNumber):
        response = requests.get(self.api.url + '/users/user-by-phone-number',
                                params={'phoneNumber': phoneNumber})
        logger.info(f"getUserByPhoneNumber, response: {response.json()}, satus code: {response.status_code}")
        return User(response.json())

    def userIsRegistered(self, phoneNumber, email):
        response = requests.get(self.api.url + '/users/registered',
                                params={'phoneNumber': phoneNumber,
                                        'email': email})
        return bool(response.json())

    def createNewUser(self, fName, lName, phNum, address, password, email='-'):
        response = requests.post(self.api.url + '/users',
                                  json={'firstName': fName,
                                       'lastName': lName,
                                       'phoneNumber': phNum,
                                       'email': email,
                                       'address': address,
                                       'password': password})
        if response.status_code == 200:
            logger.info("user created successfully")
        else:
            logger.info("user did not create")

    def getSizesWithTypeSize(self, type, size):
        response = requests.get(self.api.url + '/capsules/capsule-with-type-size',
                                params={'type': type,
                                        'size': size})
        logger.info(f"getSizesWithTypeSize, response: {response.json()}")
        return response.json()

    def addNewAddress(self, id, address):
        response = requests.patch(self.api.url + '/users/' + id,
                                  json={'address': address})
        logger.info(f"addNewAddress, response: {response.json()}, status code: {response.status_code}")

    def createOrder(self, userId, capsuleId):
        capsule_response = requests.get(self.api.url + '/capsules/' + capsuleId)
        logger.info(f"createOrder_getCapsuleById, response: {capsule_response.json()}")
        capsule = Capsule(capsule_response.json())
        response = requests.post(self.api.url + '/orders',
                                 json={'userId': userId,
                                       'capsuleId': capsuleId,
                                       'price': capsule.price,
                                       'size': capsule.size})
        logger.info(f"createOrder, response: {response.json()}")
        return Order(response.json())

    def getOrderById(self, orderId):
        response = requests.get(self.api.url + '/orders' + orderId)
        logger.info(f"getOrderById, orderID:{orderId}, response:{response.json()}")
        return Order(response.json())

    def addOrderDeiveryDate(self, orderId, deliveryDate):
        response = requests.patch(self.api.url + '/orders/' + orderId,
                                  json={'deliveryDateToClient': deliveryDate})
        logger.info(f"addOrderDeiveryDate, orderId={orderId}, deliveryDate={deliveryDate} response: {response.json()}")
        return response

    def getRandomCapsule(self, type, size):
        response = requests.get(self.api.url + '/capsules/random-capsule',
                                params={'type': type,
                                        'size': size})
        if response.status_code == 200:
            logger.info(f"getRandomCapsule, capsule founded, id: {response.json()}")
        else:
            logger.info(f"getRandomCapsule, capsule did not found, type={type}, size={size}")
            return False
        return Capsule(response.json())

    def getCapsuleById(self, capsuleId):
        response = requests.get(self.api.url + '/capsules/' + capsuleId)
        logger.info(f"getCapsuleById, response: {response.json()}")
        return Capsule(response.json())

    def getDeliveriesByDate(self, date):
        response = requests.get(self.api.url + '/orders/get-deliveries-by-date',
                                params={'date': date})
        time_dirty = list(response.json())
        logger.info(f"getDeliveriesByDate, params= date: {date}, response: {response.json()}")
        time = []
        for date in time_dirty:
            new_time = date.split(' ')[1].split(':')
            time.append(new_time[0] + ':' + new_time[1])
        logger.info(f"getDeliveriesByDate, return times: {time}")
        return time

    def getOrders(self):
        response = requests.get(self.api.url + '/orders')
        orders = []
        for order in response.json():
            orders.append(Order(order))
        return orders

    def getClothesById(self, id):
        response = requests.get(self.api.url + '/clothes/' + id)
        logger.info(f"getClothesById, id:{id}, response:{response.json()}")

api = API()
