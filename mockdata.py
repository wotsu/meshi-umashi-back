from db import init_db, add_restaurant_data, close_db

def add_mock_data():
    conn = init_db()
    add_restaurant_data(conn, "太一商店", 5, 3, 4, 4, "濃厚極太麺", "https://taichi-shouten.com/", "test1.jpg")
    add_restaurant_data(conn, "華さん食堂", 4, 4, 3, 5, "安くておいしい定食", "https://www.hen-takeout.com/hanasansyokudou.html", "test2.jpg")
    add_restaurant_data(conn, "横浜家系ラーメン 麺一家", 3, 4, 4, 3, "鉄板チャーハンがおいしい", "https://www.tnc.co.jp/store/shop/archives/40705", "test3.jpg")
    add_restaurant_data(conn, "吉利", 5, 5, 5, 5, "美味しい中華がたくさん食べれる！", "https://kichiri.favy.jp/", "test4.jpg")
    close_db(conn)

if __name__ == "__main__":
    add_mock_data()