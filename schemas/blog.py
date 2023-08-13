def blogDict(blog) -> dict:
    return {
        "id":str(blog["_id"]),
        "title":blog["title"],
        "desc":blog["desc"],
        "is_active":blog["is_active"],
    }

def blogList(blog) -> list:
    return [blogDict(blog) for blog in blog]