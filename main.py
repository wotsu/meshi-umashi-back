from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/api/search/")
async def search_restaurants():
    // ai.pyの関数ができたら書く
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
