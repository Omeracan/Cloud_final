import pymongo
client = pymongo.MongoClient("mongodb://cloud:cloud123@docdb-2021-04-21-14-50-47.cluster-clt7czphqdta.ap-southeast-1.docdb.amazonaws.com:27017/?ssl=true&ssl_ca_certs=rds-combined-ca-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false") 
db = client["myDatabase"]
users_db = db["users_db"]
items_db = db["items"]

myquery = { "username": "d.thus_sk135@hotmail.com\u200b" }

x=users_db.delete_many(myquery)

print(x.deleted_count)
#print(x)
