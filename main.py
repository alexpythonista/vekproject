from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from services import get_recommendations

app = FastAPI()


class ItemsRecommendation(BaseModel):
    uid: int
    products: List[int]


@app.get("/recommendations/{user_id}", response_model=ItemsRecommendation)
def recommendations(user_id: int) -> ItemsRecommendation:
    items = get_recommendations(user_id)
    return {
        "uid": user_id,
        "products": items
    }

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
