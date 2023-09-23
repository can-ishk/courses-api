# Courses API

### Tech Stack
> Python, FastAPI
> MongoDB Atlas
> Docker

### API Endpoints

- #### GET - /courses/
    returns all available courses.
- #### GET - /courses/{course_id}/
    returns course by course id.
- #### GET - /courses/{course_id}/{chapter_id}
    returns chapter by course id and chapter id.
- #### POST - /rate/courses/{course_id}/{chapter_id}?rating={rating}
    returns all available courses. Rating can be 1 or -1. (default is 1.)
    