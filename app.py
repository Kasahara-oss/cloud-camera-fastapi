import mimetypes
import os
from google import genai
from google.genai import types

# Gemini APIキーの取得（Renderの環境変数から読み込みます）
API_KEY == os.environ.get("GEMINI_API_KEY")

# 2. 写真の読み込み設定
image_path = "cloud_photo.jpg"

# ファイルが存在するかチェック
if not os.path.exists(image_path):
  print(
      f"エラー: '{image_path}' が見つかりません。同じフォルダに画像を置いてください。"
  )
  exit()

# 画像の形式（jpegやpngなど）を自動判別
mime_type, _ = mimetypes.guess_type(image_path)

with open(image_path, "rb") as f:
  image_bytes = f.read()

# 3. AIクライアントの初期化
client = genai.Client(api_key=API_KEY)
print("Gemini（無料枠）に雲の写真を送信中...（数秒かかります）")

try:
  # 4. 無料のFlashモデルで画像と質問を送信
  response = client.models.generate_content(
      model="gemini-2.5-flash",
      contents=[
          types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
          (
              "この空の雲の種類を判定し、明日の天気予報の確率を"
              "日本語で答えてください。"
          ),
      ],
  )

  # 5. 判定結果を表示
  print("\n--- AIからの判定結果 ---")
  print(response.text)

except Exception as e:
  print(f"\nエラーが発生しました: {e}")
