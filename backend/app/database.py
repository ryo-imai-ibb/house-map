import sqlite3

DATABASE_PATH = "properties.db"


def get_connection():
    """
    SQLiteデータベースへの接続を作る関数。

    sqlite3.connect(DATABASE_PATH) により、
    properties.db というSQLiteファイルに接続する。

    ファイルが存在しない場合は、自動で作成される。
    """
    return sqlite3.connect(DATABASE_PATH)


def init_db():
    """
    アプリ起動時に必要なテーブルを作成する関数。

    CREATE TABLE IF NOT EXISTS を使うことで、
    すでにテーブルが存在する場合は何もしない。

    注意:
    既存テーブルにカラムを追加したい場合、
    CREATE TABLE IF NOT EXISTS だけでは反映されない。

    今回は学習用なので、created_at追加後は properties.db を削除して
    テーブルを作り直す。
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_url TEXT NOT NULL,
            address TEXT NOT NULL,
            rent TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        )
        """
    )

    conn.commit()
    conn.close()
