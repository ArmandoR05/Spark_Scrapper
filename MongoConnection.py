from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['GOLLO']
collection = db['PRODUCTOS_GOLLO']

