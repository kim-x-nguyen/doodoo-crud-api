from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response
from pydantic import BaseModel, validator
from random import randrange



description = """
This is just an example CRUD API

## Items

You can **read items**, **add items**, **update items** and **delete items**

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI(
    title="FastAPI Example",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None

    @validator("rating")
    def check_rating(cls, v):
        if v is None:
            return v
        if not 0 <= v <= 5:
            raise ValueError("Rating must be between 0 and 5")
        return v
    
    @validator("title")
    def check_title(cls, v):
        if len(v) < 3:
            raise ValueError("Title must be at least 3 characters long")
        return v
    
    @validator("content")
    def check_content(cls, v):
        if len(v) < 3:
            raise ValueError("Content must be at least 3 characters long")
        return v
    
    @validator("published")
    def check_published(cls, v):
        if v is None:
            return v
        if not isinstance(v, bool):
            raise ValueError("Published must be a boolean")
        return v


my_posts = [
    {"title": "Hello World", "content": "This is my first post",
        "published": True, "rating": 5, "id": 1},
    {"title": "Hello World 2", "content": "This is my second post",
     "published": True, "rating": 5, "id": 2},
    {"title": "Hello World 3", "content": "This is my third post",
     "published": True, "rating": 5, "id": 3},
    {"title": "Hello World 4", "content": "This is my fourth post",
        "published": True, "rating": 5, "id": 4},
]


@app.get("/")
async def root():
    return my_posts


@app.get("/items/latest")
async def get_latest_items():
    return my_posts[-1]


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    for post in my_posts:
        if post["id"] == item_id:
            return post
    raise HTTPException(status_code=404, detail="Item not found", headers={
                        "X-Error": "Item not found"})


@app.post("/items/", status_code=422)
async def create_item(post: Post):
    if(post):
        post_dict = post.dict()
        post_dict["id"] = randrange(0, 100000000)
        my_posts.append(post_dict)
        return {"data": post_dict}

@app.put("/items/{item_id}")
async def update_item(item_id: int, post: Post):
    for post_dict in my_posts:
        if post_dict["id"] == item_id:
            post_dict.update(post.dict())
            return {"data": post_dict}
    raise HTTPException(status_code=404, detail="Item not found", headers={
                        "X-Error": "Item not found"})


@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    for post in my_posts:
        if post["id"] == item_id:
            my_posts.remove(post)
            return Response(status_code=204, content="Item deleted")
    raise HTTPException(status_code=404, detail="Item not found", headers={
                        "X-Error": "Item not found"})
