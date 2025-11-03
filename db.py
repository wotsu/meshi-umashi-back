import sqlite3
import os


def init_db(db_path: str = "restaurants.db") -> sqlite3.Connection:
    """Initialize the SQLite database and create the restaurants table if it doesn't exist.
    
    Args:
        db_path: Path to the SQLite database file
        
    Returns:
        Connection to the SQLite database
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_name TEXT NOT NULL,
            taste INTEGER,
            cleanliness INTEGER,
            atmosphere INTEGER,
            price INTEGER,
            appeal_point TEXT,
            url TEXT,
            image_path TEXT
        )
    """)
    
    conn.commit()
    return conn


def add_restaurant_data(
    conn: sqlite3.Connection,
    store_name: str,
    taste: int | None = None,
    cleanliness: int | None = None,
    atmosphere: int | None = None,
    price: int | None = None,
    appeal_point: str | None = None,
    url: str | None = None,
    image_path: str | None = None,
) -> int:
    """データベースにレストラン情報を登録する。
    
    Args:
        conn: SQLiteデータベースへの接続
        store_name: 店名（必須）
        taste: おいしさ（オプション）
        cleanliness: 綺麗さ（オプション）
        atmosphere: 雰囲気（オプション）
        price: 価格（オプション）
        appeal_point: アピールポイント（オプション）
        url: URL（オプション）
        image_path: 画像のパス（オプション）
        
    Returns:
        登録されたレコードのID
    """
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO restaurants (
            store_name, taste, cleanliness, atmosphere, price, appeal_point, url, image_path
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (store_name, taste, cleanliness, atmosphere, price, appeal_point, url, image_path))
    
    conn.commit()
    return cursor.lastrowid


def get_all_restaurants(conn: sqlite3.Connection) -> list[dict]:
    """データベースからすべてのレストラン情報を取得する。
    
    Args:
        conn: SQLiteデータベースへの接続
        
    Returns:
        レストラン情報のリスト（各要素は辞書形式）
    """
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM restaurants")
    rows = cursor.fetchall()
    
    # 辞書形式に変換
    restaurants = []
    for row in rows:
        restaurants.append({
            "id": row["id"],
            "store_name": row["store_name"],
            "taste": row["taste"],
            "cleanliness": row["cleanliness"],
            "atmosphere": row["atmosphere"],
            "price": row["price"],
            "appeal_point": row["appeal_point"],
            "url": row["url"],
            "image_path": row["image_path"],
        })
    
    return restaurants


def close_db(conn: sqlite3.Connection) -> None:
    """Close the database connection.
    
    Args:
        conn: Connection to the SQLite database
    """
    conn.close()


if __name__ == "__main__":
    # データベースの初期化を実行
    conn = init_db()
    print("データベースが正常に作成されました。")
    close_db(conn)

