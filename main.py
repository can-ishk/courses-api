from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()
Mongo_URI = os.getenv('MONGO_URI')

app = FastAPI()
db_client = MongoClient(Mongo_URI)
db = db_client["sharedDatabase"]

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
            courses = db["courses"].find(query, {'_id': 0, 'chapters':0}).sort(sort_criteria)
    except:
        raise HTTPException(status_code=500, detail="Internal server error")
    if not courses:
        raise HTTPException(status_code=404, detail="Courses not found")
    return list(courses)

@app.get("/courses/{course_id}")
def get_course_by_id(course_id: str):
    try:
         course = db.courses.find_one({'_id': ObjectId(course_id)}, {'_id': 0})
    except:
         raise HTTPException(status_code=500, detail="Internal server error")
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.get("/courses/{course_id}/{chapter_id}")
def get_chapter_by_id(course_id: str, chapter_id: str):
    course = get_course_by_id(course_id)
    chapter = None
    if len(course['chapters']) > int(chapter_id):
        chapter = course['chapters'][int(chapter_id)]
    else:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter

@app.post("/rate/courses/{course_id}/{chapter_id}")
def rate_chapter(course_id:str, chapter_id:str, rating: int):
    course = get_course_by_id(course_id)
    if len(course['chapters']) <= int(chapter_id):
        raise HTTPException(status_code=404, detail="Chapter not found")
    if rating not in [1, -1]:
        raise HTTPException(status_code=400, detail="Rating must be -1 or 1")
    course['chapters'][int(chapter_id)]['rating']['total'] += rating
    course['chapters'][int(chapter_id)]['rating']['count'] += 1
    course['rating']['total'] += rating
    course['rating']['count'] += 1
    try:
        db.courses.update_one({'_id': ObjectId(course_id)}, {"$set": course})
    except:
        raise HTTPException(status_code=500, detail="Internal server error")
    return course
    
