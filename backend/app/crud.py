"""
crud は Create / Read / Update / Delete の略.データに対する基本操作.

C: Create  作成する
R: Read    読み取る
U: Update  更新する
D: Delete  削除する

service.py や repository.py みたいな名前にすることもある。
"""
from app.database import get_connection
from app.schemas import PropertyCreate


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

    latitude = 35.689634
    longitude = 139.692101

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