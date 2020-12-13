import pymongo


client = pymongo.MongoClient(
    "mongodb+srv://Main:1q2w3e4r@cluster0.dbjal.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.get_database('Register')
col = db.get_collection('Login')

sign = {'ID': 'asd', 'PassWord': 'asdasd'}
col.insert_one(sign)

