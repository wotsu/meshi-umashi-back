# test_ai.py
import asyncio
from ai import analyze_review_text, search_restaurant
from db import init_db, close_db # db モジュールからインポート

async def main():
    conn = None  # conn を None で初期化
    try:
        conn = init_db()
        
        review = "料理がとてもおいしくて、雰囲気も落ち着いていた。ただ少し高かった。"
        result = await analyze_review_text(review, conn)
        print("レビュー分析結果:", result)

        request = "めちゃくちゃおしゃれで雰囲気のいいカフェを探している"
        match = await search_restaurant(request, conn)
        print("検索リクエスト分析:", match)

    except Exception as e:
        print(f"テスト実行中にエラーが発生しました: {e}")
    
    finally:
        # conn が正常に初期化されていた場合のみクローズする
        if conn:
            close_db(conn)
            print("データベース接続をクローズしました。")

if __name__ == "__main__":
    asyncio.run(main())