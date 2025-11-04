from fastapi import FastAPI
from ai import search_restaurant
from db import init_db, close_db
import uvicorn
from pydantic import BaseModel

app = FastAPI()

class SearchRequest(BaseModel):
    query: str

@app.get("/api/search/")
async def search_restaurants(search_request: SearchRequest):
    conn = init_db()
    search_result = await search_restaurant(search_request.query, conn)
    close_db(conn)
    return search_result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
