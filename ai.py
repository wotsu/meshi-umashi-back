import json
import os
import aiohttp #非同期通信ライブラリ
from google import genai

# --- Gemini API 設定 ---
API_KEY = os.environ.get("GEMINI_API_KEY", "") # どちらか
API_KEY = ""
if not API_KEY:
    print("警告: GEMINI_API_KEY が設定されていません。")

API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"

# --- JSONスキーマの定義 ---
# DBスキーマに合わせて英語のキーで出力するように強制する
# 'service' (接客) をスキーマから削除
EXPECTED_JSON_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "scores": {
            "type": "OBJECT",
            "properties": {
                "taste": { "type": ["NUMBER", "NULL"], "description": "おいしさ (1-5点 または null)" },
                "cleanliness": { "type": ["NUMBER", "NULL"], "description": "きれいさ (1-5点 または null)" },
                "price": { "type": ["NUMBER", "NULL"], "description": "コストパフォーマンス (1-5点 または null)" },
                "atmosphere": { "type": ["NUMBER", "NULL"], "description": "雰囲気 (1-5点 または null)" }
            },
            "required": ["taste", "cleanliness", "price", "atmosphere"]
        }
    },
    "required": ["scores"]
}


def build_system_prompt():
    """
    AIに指示するシステムプロンプトを構築します。
    """
    return """
あなたはプロの飲食店レビューアナリストです。
渡されたレビューテキストを読み、指定された「評価軸」に基づき、それぞれ1点から5点の5段階で採点してください。

# 評価軸
1.  **taste (おいしさ)**: 料理、食材の質、味付け、調理技術など。
2.  **cleanliness (きれいさ)**: 店内の清潔感、テーブル、床、トイレ、食器の衛生状態など。
3.  **price (コストパフォーマンス)**: 価格に対する料理の質や量、満足度、お得感。
4.  **atmosphere (雰囲気)**: 店内の内装、照明、BGM、客層、居心地の良さなど。

# 採点基準
- 5点: 非常に満足・素晴らしい
- 4点: 満足・良い
- 3点: 普通・一般的
- 2点: 不満・悪い
- 1点: 非常に不満・非常に悪い

# 注意事項
- レビューテキストから読み取れる情報のみに基づいて採点してください。
- 特定の評価軸について、レビュー内で全く言及されていない、または判断が難しい場合は、点数の代わりに `null` を出力してください。
- 必ず指定されたJSON形式(英語のキー: taste, cleanliness, price, atmosphere)で回答してください。
"""

async def analyze_review_text(review_text: str) -> dict:
    """
    レビューテキストをGemini APIに送信し、分析結果(JSON)を辞書として返します。
    """
    
    system_prompt = build_system_prompt()
    
    # Gemini APIへのリクエストペイロード
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"以下のレビューを分析してください。\n\nレビュー:\n```\n{review_text}\n```"}
                ]
            }
        ],
        "systemInstruction": {
            "parts": [
                {"text": system_prompt}
            ]
        },
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": EXPECTED_JSON_SCHEMA,
            "temperature": 0.2 # 安定した出力を得るために低めに設定
        }
    }

    # APIキーが設定されていない場合は例外を送出
    if not API_KEY:
        print("エラー: APIキーが設定されていません。ローカル環境の場合、環境変数 GEMINI_API_KEY を設定してください。")
        raise Exception("API_KEY is not set. Please set the GEMINI_API_KEY environment variable for local development.")

    # aiohttpを使って非同期でAPIリクエスト
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(API_URL, json=payload, headers={"Content-Type": "application/json"}) as response:
                
                if response.status != 200:
                    # APIからエラーが返ってきた場合
                    error_text = await response.text()
                    print(f"Gemini API Error: Status {response.status}, Body: {error_text}")
                    raise Exception(f"Gemini API request failed with status {response.status}")

                # 正常なレスポンス
                result = await response.json()
                
                # Geminiからのレスポンス構造を解析
                if (
                    "candidates" in result and
                    result["candidates"] and
                    "content" in result["candidates"][0] and
                    "parts" in result["candidates"][0]["content"] and
                    result["candidates"][0]["content"]["parts"]
                ):
                    # JSON文字列を取得
                    json_text = result["candidates"][0]["content"]["parts"][0]["text"]
                    # JSON文字列をパースして辞書に
                    parsed_json = json.loads(json_text)
                    return parsed_json
                else:
                    # 予期しないレスポンス形式
                    print(f"Unexpected Gemini response format: {result}")
                    raise Exception("Invalid response structure from Gemini API.")

        except aiohttp.ClientConnectorError as e:
            print(f"Connection Error: {e}")
            raise Exception(f"Failed to connect to Gemini API: {e}")
        except json.JSONDecodeError as e:
            # APIのレスポンスがJSONとしてパースできなかった場合
            print(f"JSON Decode Error: {e}. Response text was: {json_text}")
            raise Exception("Failed to decode JSON response from Gemini API.")
        except Exception as e:
            # その他のエラー
            print(f"Error in analyze_review_text: {e}")
            # エラーを再スローして、main.py側で処理できるようにする
            raise e

