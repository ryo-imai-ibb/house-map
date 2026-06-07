from pydantic import BaseModel, Field, HttpUrl

class PropertyCreate(BaseModel):
    """
    POST /properties のリクエストボディを表すモデル。

    Pydantic を使うことで、以下を FastAPI/Pydantic 側に任せられる。

    - source_url が存在するか
    - address が存在するか
    - source_url が str か
    - address が str か

    つまり、以前書いていた以下の処理は不要になる。

        source_url = property_data.get("source_url")
        address = property_data.get("address")

        if not source_url:
            raise HTTPException(status_code=400, detail="source_url is required")

        if not address:
            raise HTTPException(status_code=400, detail="address is required")

    注意:
    source_url: str / address: str だけでは、空文字 "" は弾けない。
    空文字も弾きたい場合は Field(min_length=1) などの追加制約を使う。
    """
    source_url: HttpUrl # source_url はURL形式である必要がある
    address: str = Field(min_length=1) # address は文字列 かつ 1文字以上である必要がある
    rent: str = Field(min_length=1) # rent は文字列 かつ 1文字以上である必要がある

class Property(PropertyCreate):
    """
    APIが返す物件データを表すモデル。

    PropertyCreate は「登録時にユーザーから受け取るデータ」。
    Property は「登録後にシステムが返すデータ」。

    PropertyCreate には source_url と address だけがある。
    Property はそれに加えて、システム側で付与する以下の値を持つ。

    - id
    - latitude
    - longitude
    - created_at

    class Property(PropertyCreate) と書くことで、
    PropertyCreate の項目を引き継げる。
    """

    id: int
    latitude: float
    longitude: float
    created_at: str