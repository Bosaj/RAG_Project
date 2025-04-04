from fastapi import FastAPI
app = FastAPI()

@app.get("/welcom")
def welcome():
    return{

        "message":"Hello World!"
    }
