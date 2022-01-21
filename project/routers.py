from celery.result import AsyncResult
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from schemas import Item
from worker import create_task


app = APIRouter()

@app.post("/tasks")
def run_request(item: Item):
    """
    ## Parsing the page to get unique tags with nested elements count

    Body Parameters
    ----------
    param: {"url": "HttpURL"}

    Returns
    -------
    str task_id
    """
    task = create_task.delay(item.url)
    return JSONResponse({"task_id": task.id})

@app.get("/tasks/{task_id}")
def get_result(task_id):
    """
    ## Getting the result of the analysis

    Path Parameters
    ----------
    param: str task_id

    Returns
    -------
    JSON result.
    When an error occurs, the status and description are displayed.
    #### example:
                {
                  "html": {
                    "count": 1,
                    "nested": 633
                  },
                  "head": {
                    "count": 1,
                    "nested": 40
                  },
                  "body": {
                    "count": 1,
                    "nested": 591
                  }
               }
    """
    task_result = AsyncResult(task_id)
    if task_result.failed():
        status_code, msg = (','.join(task_result.result.args)).split(' ',1)
        raise HTTPException(int(status_code), msg)
    return task_result.result

