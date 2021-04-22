from fastapi import FastAPI,Body
import uvicorn
from pydantic import BaseModel
import os
from typing import Optional
from pymongo


class LoginObject(BaseModel):
    username : str 
    password : str

class ItemObject(BaseModel):
    name : str
    mount : Optional[int] = None

class  addItemObject(BaseModel):
    username : str
    item : list[ItemObject]

class purchaseObject(BaseModel):
    username: str
    
app = FastAPI()

@app.post("/login")
async def (req_body : LoginObject = Body(...)):
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    blob_client = blob_service_client.get_blob_client(container="username", blob=f"{req_body.username}.txt")
    password_blob=blob_client.download_blob().readall()
    if req_body.password == password_blob:
        return {
        "statusCode":200,
        "body": "Login Successful"
        }
    return {
        "statusCode":400,
        "body": f"invalid username:{req_body.username} or  password:{req_body.password}"
        }

@app.post("/addItem")
async def ()

@app.post("/purchase")


if __name__ == "__main__":
    uvicorn.run("main:app",host= "0.0.0.0", port = 8080)
