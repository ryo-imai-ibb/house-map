from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

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

@app.get("/properties/{property_id}", response_model=Property)
def get_property(property_id: int):
    property_data = crud.get_property(property_id)

    if property_data is None:
        raise HTTPException(status_code=404, detail="property not found")

    return property_data

@app.post("/properties", response_model=Property) # このAPIのレスポンスは Property の形で返しますという意味
def create_property(property_data: PropertyCreate): # POSTで送られてきたJSONを property_data という変数で受け取るという意味
    try:
        return crud.create_property(property_data)
    except RuntimeError as e: # RuntimeError そのままだと、FastAPI側では 500 Internal Server Error　となり原因が分かりづらい
        raise HTTPException(status_code=400, detail=str(e)) # ユーザー入力側の問題として 400

@app.put("/properties/{property_id}", response_model=Property)
def update_property(property_id: int, property_data: PropertyCreate):
    try:
        updated_property = crud.update_property(property_id, property_data)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if updated_property is None:
        raise HTTPException(status_code=404, detail="property not found")

    return updated_property

@app.delete("/properties/{property_id}") # {property_id} はURLの一部で、実際の値はAPI呼び出しのときに指定される。例えば /properties/123 なら property_id は 123 になる。
def delete_property(property_id: int):
    deleted_count = crud.delete_property(property_id)

    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="property not found")

    return {"message": "property deleted"}
