from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.schemas import PropertyCreate, Property
from app import crud
from app.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPIアプリの起動時・終了時に実行する処理を書く場所。

    yield より前:
        アプリ起動時に1回だけ実行される。
        今回はDBテーブルを初期化する。

    yield より後:
        アプリ終了時に1回だけ実行される。
        今回は特に何もしない。
    """

    init_db()
    yield

app = FastAPI(lifespan=lifespan) # このFastAPIアプリは、起動時・終了時の処理として lifespan を使いますという意味
    
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/properties", response_model=list[Property])
def get_properties():
    return crud.get_properties()

@app.post("/properties", response_model=Property) # このAPIのレスポンスは Property の形で返しますという意味
def create_property(property_data: PropertyCreate): # POSTで送られてきたJSONを property_data という変数で受け取るという意味
    return crud.create_property(property_data)
