import pymongo
import sys

##Create a MongoDB client, open a connection to Amazon DocumentDB as a replica set and specify the read preference as secondary preferred
client = pymongo.MongoClient('mongodb://cloud:cloud123@docdb-2021-04-21-14-50-47.cluster-clt7czphqdta.ap-southeast-1.docdb.amazonaws.com:27017/?ssl=true&ssl_ca_certs=rds-combined-ca-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false') 

##Specify the database to be used
db = client["myDatabase"]

##Specify the collection to be used
col = db["myCollectiontest"]

##Insert a single document
col.insert_one({'hello':'Amazon DocumentDB','trans':{"apple":1,"banana":2}})

##Find the document that was previously written
x = col.find_one({'hello':'Amazon DocumentDB'})

##Print the result to the screen
print(x)

##Close the connection
client.close()