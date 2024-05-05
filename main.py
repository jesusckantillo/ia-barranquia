from fastapi import FastAPI
from routers import text_routes

#
app = FastAPI()
app.include_router(text_routes.router)
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
 