from pymongo import MongoClient

client = MongoClient("mongodb+srv://gcastronuevo026:gelain110503@milkteamain.khvv2k1.mongodb.net/milktea?retryWrites=true&w=majority")  # try standard string
db = client["milkteamain"]
print(db.list_collection_names())
