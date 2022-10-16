from fastapi import FastAPI
from pydantic import BaseModel
from utils.classification import make_prediction
from collections import OrderedDict

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

class TransactionInput(BaseModel):
    amount: int
    hour: int
    tag: str



@app.post('/classify')
async def classify_transaction(transaction: TransactionInput):
    input_dict = {
    "amount": transaction.amount,
    "hour": transaction.hour,
    "tag": transaction.tag
    }
    return make_prediction(input_dict)
    
