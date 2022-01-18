from fastapi import APIRouter

from schemas import Item


app = APIRouter()

@app.post("/tasks")
def run_task(item: Item):
    return item