import pymongo

client = pymongo.MongoClient("mongodb+srv://root:root123@testparking.3yyne.mongodb.net/")
db = client.testparking
collection = db.users

# 插入文件到集合中
collection.insert_one({
    "id": "d06",
    "use": "0"
})

print("成功")
