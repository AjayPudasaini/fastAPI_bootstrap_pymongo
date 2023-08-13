from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
# from pymongo import MongoClient
from routers.blog import router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# conn = MongoClient("mongodb://localhost:27017")
# db = conn["testdb"]
# collection = db["students"]


# @app.get("/", response_class=HTMLResponse)
# def read_root(request:Request):
#     students = collection.find({})
#     for i in students:
#         print("l20",i, type(i))

#     return templates.TemplateResponse("index.html", {"request": request})


# @app.get("/items/{item_id}")
# def items(item_id):
#     return{"Hello":"World", "items":item_id}

app.include_router(router)