"""
今までは crud.py が以下を全部実行。

DBに保存する
DBから取得する
住所から緯度経度を決める

しかし, 本来の crud.py の責務はDB操作。したがって緯度経度の処理は分けるのがきれい.

crud.py
→ DB操作

geocoding.py
→ 住所から緯度経度を取得する処理
"""
import os

import requests
from dotenv import load_dotenv


load_dotenv() # .env ファイルを読み込む処理


def geocode_address(address: str) -> tuple[float, float]:
    """
    住所を緯度・経度に変換する関数。

    Google Geocoding API に住所を渡し、
    返ってきた位置情報から latitude / longitude を取り出す。

    Args:
        address: 住所文字列

    Returns:
        tuple[float, float]: 緯度, 経度

    Raises:
        RuntimeError: APIキーが未設定、またはGeocodingに失敗した場合
    """

    api_key = os.getenv("GOOGLE_MAPS_API_KEY")

    if api_key is None:
        raise RuntimeError("GOOGLE_MAPS_API_KEY is not set")

    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        "address": address,
        "key": api_key,
        "language": "ja", # 日本語で住所を渡すので、レスポンスも日本語にするためのパラメータ
        "region": "jp", # 日本の住所であることをAPIに伝えるためのパラメータ。これもレスポンスの精度向上に寄与する。
    }

    response = requests.get(endpoint, params=params, timeout=10) # HTTP GETリクエスト
    response.raise_for_status()

    data = response.json() # Googleから返ってきたJSONを、Pythonの辞書として扱えるようにしている

    if data["status"] != "OK":
        raise RuntimeError(f"Geocoding failed: {data['status']}")

    location = data["results"][0]["geometry"]["location"]

    latitude = location["lat"]
    longitude = location["lng"]

    return latitude, longitude