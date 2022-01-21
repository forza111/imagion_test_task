from celery.result import AsyncResult
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

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
    if task_result.failed():
        status_code, msg = (','.join(task_result.result.args)).split(' ',1)
        raise HTTPException(int(status_code), msg)
    return task_result.result

