from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dispatcher.apis.dispatcher_api import dispatcher_api

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_origins=["*"],
)


@app.get("/ping")
def ping():
    return {"message": "PING"}


app.include_router(dispatcher_api)
