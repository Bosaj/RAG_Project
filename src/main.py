from fastapi import FastAPI
from routes import base,data
import logging
logging.basicConfig(level=logging.DEBUG)


app = FastAPI()
app.include_router(base.base_router)
app.include_router(data.data_router)