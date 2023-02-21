from fastapi import FastAPI
from poster import main_task
app = FastAPI()


@app.get("/")
def index():
    return "Hello World"


@app.post('/__space/v0/actions')
async def run_post():
    main_task()
    return {"message": "OK"}
