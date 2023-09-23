import contextlib
from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

app = FastAPI()
db_client = MongoClient("mongodb://localhost:27017/")
db = db_client["courses"]

sorting_matrix = {
        'date': [('date', -1)], # date, descending
        'rating': [('rating.total', -1), ('rating.count', -1)], # rating, descending, then rating count, ascending
        'name': [('name', 1)] # name, ascending
    }

@app.get("/courses")
def get_courses(sort_by: str = 'date', domain: str = None):
    sort_criteria = sorting_matrix[sort_by]
    query = {}
    if domain:
        query = {'domain': domain}
    try:
            courses = db["courses"].find(query, {'name': 1, 'date': 1, 'description': 1, 'domain':1,'rating':1,'_id': 0}).sort(sort_criteria)
    except:
        raise HTTPException(status_code=500, detail="Internal server error")
    return list(courses)

@app.get("/courses/{course_id}")
def get_course_by_id():
    pass

@app.get("/courses/{course_id}/{chapter_id}")
def get_chapter_by_id():
    pass

@app.post("/rate/courses/{course_id}/{chapter_id}")
def rate_chapter():
    pass
