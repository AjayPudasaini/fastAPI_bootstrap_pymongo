from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from config.db import conn
from models.blog import Blog
from schemas.blog import blogDict, blogList

templates = Jinja2Templates(directory="templates")

router = APIRouter()

db = conn["my_test_db"]
collection = db["blog"]

@router.get("/", response_class=HTMLResponse)
def read_root(request:Request):
    blogs = blogList(collection.find({"is_active":True}))
    return templates.TemplateResponse("index.html", {"request": request, "blogs":blogs})

@router.get("/create", response_class=HTMLResponse)
def get_form(request:Request):
    return templates.TemplateResponse("blog_create.html", {"request": request})

@router.post("/create-blog", response_class=HTMLResponse)
async def create_blog(request: Request):
    try:
        form = await request.form()
        is_active = form.get("is_active") == "false"
        blog_data = {
            "title": form.get("title"),
            "desc": form.get("desc"),
            "is_active": is_active
        }
        collection.insert_one(blog_data)
        return RedirectResponse(url="/", status_code=303)
        # success_message = "success."
        # return templates.TemplateResponse("index.html", {"request": request, "message": success_message}, status_code=303)
    except Exception as e:
        error_message = "Failed to create blog."
        return templates.TemplateResponse("blog_create.html", {"request": request, "message": error_message})


@router.get("/blog/{id}", response_class=HTMLResponse)
def blog_detail(request:Request, id:str):
    try:
        blog = blogDict(collection.find_one({"_id": ObjectId(id)})) 
        if blog:
            return templates.TemplateResponse("blog_detail.html", {"request": request, "blog": blog})
        else:
            return HTTPException(status_code=404, detail="Blog not found")
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Server Issues. {e}")

@router.get("/update/{id}", response_class=HTMLResponse)
def get_update_form(request:Request, id:str):
    try:
        blog = blogDict(collection.find_one({"_id": ObjectId(id)})) 
        if blog:
            return templates.TemplateResponse("blog_update.html", {"request": request, "blog": blog})
        else:
            return HTTPException(status_code=404, detail="Blog not found")
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Server Issues. {e}")

@router.post("/update-blog/{id}", response_class=HTMLResponse) # using post method because html forms doesn't support put or patch method
async def update_blog(request:Request, id:str):
    try:
        filter_query = {"_id": ObjectId(id)}
        form = await request.form()
        is_active = form.get("is_active") == "true"
        blog_data = {
            "$set":{
                "title": form.get("title"),
                "desc": form.get("desc"),
                "is_active": is_active
            }
        }
        collection.update_one(filter_query, blog_data)
        return RedirectResponse(url=f"/blog/{id}", status_code=303)
    except Exception as e:
        error_message = "Failed to create blog."
        return templates.TemplateResponse("blog_update.html", {"request": request, "message": error_message})
    
@router.post("/delete-blog/{id}", response_class=HTMLResponse)
def delete_blog(request:Request, id:str):
    try:
        filter_query = {"_id": ObjectId(id)}
        collection.delete_one(filter_query)
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        error_message = "Failed to delete blog"
        return templates.TemplateResponse("blog_detail.html", {"request": request, "message": error_message})
