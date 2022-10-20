from fastapi import FastAPI
from pydantic import BaseModel
from utils.classification import make_prediction
from collections import OrderedDict
from api_logger.logging import FastApiLogger
from pathlib import Path
from mock_transactions import TransactionInput

def _create_app() -> FastAPI:
    """ 
    Create Fast API app and set its logger

    Returns:
        FastAPI: The Fast API app
    """

    logging_config_path = Path("api_logger/logging_config.json")
    api = FastAPI()

    logger = FastApiLogger.make_logger(logging_config_path)
    api.logger = logger
    return api

app = _create_app()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post('/classify')
async def classify_transaction(transaction: TransactionInput):

    prediction = make_prediction(transaction)
    return {"prediction":prediction.tolist()}
    
