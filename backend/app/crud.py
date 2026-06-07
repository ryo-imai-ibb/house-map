"""
crud は Create / Read / Update / Delete の略.データに対する基本操作.

C: Create  作成する
R: Read    読み取る
U: Update  更新する
D: Delete  削除する

service.py や repository.py みたいな名前にすることもある.

HTTPException は crud.py ではなく main.py で 記述する.

crud.py
→ データ操作・内部処理

main.py
→ HTTP APIとして何を返すか

なので，crud.py はなるべくHTTPのことを知らない方がきれい.
"""
from app.database import get_connection
from app.schemas import PropertyCreate
from app.geocoding import geocode_address


def get_properties():
    """
    登録済み物件一覧をDBから取得する。

    SQLiteのpropertiesテーブルからSELECTして取得する。
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            source_url,
            address,
            latitude,
            longitude,
            created_at
        FROM properties
        ORDER BY id
        """
    )

    rows = cursor.fetchall()
    conn.close()

    properties = []
    for row in rows:
        property_data = {
            "id": row[0],
            "source_url": row[1],
            "address": row[2],
            "latitude": row[3],
            "longitude": row[4],
            "created_at": row[5],
        }
        properties.append(property_data)

    return properties


def create_property(property_data: PropertyCreate):
    """
    新しい物件をDBに保存する。

    SQLite対応後は、INSERT文でpropertiesテーブルに保存する。

    created_at はDB側の DEFAULT CURRENT_TIMESTAMP に任せる。
    そのため、INSERT文では created_at を指定しない。
    """

    latitude, longitude = geocode_address(property_data.address)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO properties (
            source_url,
            address,
            latitude,
            longitude
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            str(property_data.source_url),
            property_data.address,
            latitude,
            longitude,
        ),
    )

    conn.commit()

    new_property_id = cursor.lastrowid

    cursor.execute(
        """
        SELECT
            id,
            source_url,
            address,
            latitude,
            longitude,
            created_at
        FROM properties
        WHERE id = ?
        """,
        (new_property_id,),
    )

    row = cursor.fetchone()
    conn.close()

    new_property = {
        "id": row[0],
        "source_url": row[1],
        "address": row[2],
        "latitude": row[3],
        "longitude": row[4],
        "created_at": row[5],
    }

    return new_property

def get_property(property_id: int):
    """
    指定されたIDの物件をDBから1件取得する。

    SELECT文で properties テーブルから対象レコードを取得する。
    対象が存在しない場合は None を返す。
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            source_url,
            address,
            latitude,
            longitude,
            created_at
        FROM properties
        WHERE id = ?
        """,
        (property_id,),
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    property_data = {
        "id": row[0],
        "source_url": row[1],
        "address": row[2],
        "latitude": row[3],
        "longitude": row[4],
        "created_at": row[5],
    }

    return property_data

def update_property(property_id: int, property_data: PropertyCreate):
    """
    指定されたIDの物件情報を更新する。

    UPDATE文で properties テーブルの source_url と address を更新する。
    対象が存在しない場合は None を返す。

    注意:
    今は住所→緯度経度変換をまだ実装していないため、
    latitude / longitude は仮の固定値で更新する。
    """

    latitude, longitude = geocode_address(property_data.address)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE properties
        SET
            source_url = ?,
            address = ?,
            latitude = ?,
            longitude = ?
        WHERE id = ?
        """,
        (
            str(property_data.source_url),
            property_data.address,
            latitude,
            longitude,
            property_id,
        ),
    )

    updated_count = cursor.rowcount
    conn.commit()

    if updated_count == 0:
        conn.close()
        return None

    cursor.execute(
        """
        SELECT
            id,
            source_url,
            address,
            latitude,
            longitude,
            created_at
        FROM properties
        WHERE id = ?
        """,
        (property_id,),
    )

    row = cursor.fetchone()
    conn.close()

    updated_property = {
        "id": row[0],
        "source_url": row[1],
        "address": row[2],
        "latitude": row[3],
        "longitude": row[4],
        "created_at": row[5],
    }

    return updated_property

def delete_property(property_id: int):
    """
    指定されたIDの物件をDBから削除する。

    DELETE文で properties テーブルから対象レコードを削除する。
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM properties
        WHERE id = ?
        """,
        (property_id,),
    )

    deleted_count = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted_count