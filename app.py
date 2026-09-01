import os
import mimetypes
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from google import genai
from google.genai import types

app = FastAPI()

# 🔑 修正ポイント1：イコールを1つ（=）にして、環境変数からAPIキーを取得
api_key = os.environ.get("GEMINI_API_KEY")

# 🌐 スマホでアクセスしたときに表示される「表画面（HTML）」
@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>雲カメラ AI (FastAPI)</title>
        </head>
        <body style="text-align: center; font-family: sans-serif; padding-top: 50px;">
            <h1>📸 雲カメラ AI (FastAPI版)</h1>
            <p>写真を撮影またはアップロードすると、AIが雲の名前を判定します。</p>
            <br>
            <form action="/analyze" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept="image/*" required><br><br><br>
                <button type="submit" style="padding: 12px 24px; font-size: 16px;">AIで解析する</button>
            </form>
        </body>
    </html>
    """

# 🤖 ボタンが押されたときに裏側でGeminiを動かす処理
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    if not api_key:
        raise HTTPException(status_code=500, detail="Gemini APIキーが設定されていません。")
    
    try:
        # 修正ポイント2：スマホから送信された画像データを読み込む
        image_bytes = await file.read()
        mime_type, _ = mimetypes.guess_type(file.filename)
        if not mime_type:
            mime_type = "image/jpeg"
            
        client = genai.Client(api_key=api_key)
        
        # 以前のコードの「判定の質問内容」をそのまま引き継いでいます
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                "この空の雲の種類を判定し、明日の天気予報の確率を日本語で答えてください。"
            ],
        )
        
        # 結果を画面に返す
        return HTMLResponse(content=f"""
        <html>
            <body style="text-align: center; font-family: sans-serif; padding-top: 50px; padding-horizontal: 20px;">
                <h2>--- AIからの判定結果 ---</h2>
                <p style="font-size: 18px; line-height: 1.6; max-width: 600px; margin: 0 auto; text-align: left;">
                    {response.text.replace(chr(10), '<br>')}
                </p>
                <br><br>
                <a href="/" style="font-size: 16px;">ともかくもう一度撮影する</a>
            </body>
        </html>
        """)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"エラーが発生しました: {str(e)}")
