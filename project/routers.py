from celery.result import AsyncResult
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from schemas import Item
from worker import create_task


app = APIRouter()

@app.post("/tasks")
def run_request(item: Item):
    task = create_task.delay(item.url)
    return JSONResponse({"task_id": task.id})

@app.get("/tasks/{task_id}")
def get_result(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)
