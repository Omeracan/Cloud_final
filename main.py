from fastapi import FastAPI,Body
import uvicorn
from pydantic import BaseModel
import os
from typing import Optional
import pymongo
import sys

class LoginObject(BaseModel):
    username : str 
    password : str


class  ItemObject(BaseModel):
    username : str
    item : str

class  addItemObject(BaseModel):
    name : str
    price : int

class purchaseObject(BaseModel):
    username: str

client = pymongo.MongoClient("mongodb://cloud:cloud123@docdb-2021-04-21-14-50-47.cluster-clt7czphqdta.ap-southeast-1.docdb.amazonaws.com:27017/?ssl=true&ssl_ca_certs=rds-combined-ca-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false") 
db = client["myDatabase"]
users_db = db["users_db"]
items_db = db["items"]

app = FastAPI()

@app.post("/register")
async def register(req_body : LoginObject):
    users_db.insert_one({"username":req_body.username,"password":req_body.password,"transaction":{}})
    return {
        "statusCode":200,
        "body": "Register Successful"
        }


@app.post("/login")
async def login(req_body : LoginObject):
    info = users_db.find_one({"username":req_body.username})
    try:
        if info["password"] == req_body.password:
            return {
            "statusCode":200,
            "body": "Login Successful"
            }
    except:
        return {
        "statusCode":400,
        "body": "invalid username"
        }
    return {
        "statusCode":400,
        "body": "invalid password"
        }

@app.post("/buyItem")
async def buyItem(req_body: ItemObject):
    myquery = { "username": req_body.username }
    try:
        info = users_db.find_one(myquery)
        cart = info["transaction"]
    except:
        return {
        "statusCode":400,
        "body": "invalid username"
        }
    try:
        price = items_db.find_one({"name":req_body.item})["price"]
    except:
        return {
        "statusCode":400,
        "body": "invalid item"
        }
    if req_body.item not in cart:
        cart[req_body.item] = (1,price)
    else:
        cart[req_body.item][0] +=1
    newvalues = { "$set": { "transaction": cart } }
    users_db.update_one(myquery,newvalues)
    items = []
    for item in sorted(cart):
        items.append({"name":item,"amount":cart[item][0],"price":cart[item][1]})
    return {
        "statusCode":200,
        "body": items
        }

@app.post("/addItem")
async def addItem(req_body: addItemObject):
    myitem = {"name":req_body.name,"price":req_body.price}
    items_db.insert_one(myitem)
    return {
        "statusCode":200,
        "body": f"add {req_body.name}"
        }
@app.post("/purchase")
async def purchase(req_body: purchaseObject):
    myquery = { "username": req_body.username }
    try:
        info = users_db.find_one(myquery)
        cart = info["transaction"]
    except:
        return {
        "statusCode":400,
        "body": "invalid username"
        }
    total = 0
    for k,(amount,price) in cart.items():
        total += amount*price

    #CLEAR TRANSACTION
    newvalues = { "$set": { "transaction": {} } }
    users_db.update_one(myquery,newvalues)
    return {
        "statusCode":200,
        "body": total
        }

@app.get("/view")
async def view():
    users = []
    items = []
    for user in users_db.find({},{ "_id": 0, "name": 1, "price": 1 }):
        users.append(user)
    for item in items_db.find({},{ "_id": 0, "name": 1, "price": 1 }):
        items.append(item)
    return {
        "statusCode":200,
        "body": {"users":users,"items":items}
        }

if __name__ == "__main__":
    uvicorn.run("main:app",host= "0.0.0.0", port = 8080)
