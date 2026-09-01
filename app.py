import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from google import genai

app = FastAPI()

# Gemini APIキーの取得（Renderの環境変数から読み込みます）
api_key = os.environ.get("GEMINI_API_KEY")


@app.get("/", response_class=HTMLResponse)
async def index():
    # 1番目のアプリ用の、FastAPIで動くシンプルなHTML画面です
    return """
    <html>
        <head><title>雲カメラ AI (FastAPI)</title></head>
        <body style="text-align: center; font-family: sans-serif; padding-top: 50px;">
            <h1>📸 雲カメラ AI (FastAPI版)</h1>
            <p>写真をアップロードすると、AIが雲の名前を判定します。</p>
            <form action="/analyze" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept="image/*" required><br><br>
                <button type="submit" style="padding: 10px 20px;">AIで解析する</button>
            </form>
        </body>
    </html>
    """

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    if not api_key:
        raise HTTPException(status_code=500, detail="Gemini APIキーが設定されていません。")
    
    try:
        client = genai.Client(api_key=api_key)
        image_bytes = await file.read()
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                {'mime_type': 'image/jpeg', 'data': image_bytes},
                "この画像に写っている雲の種類を特定し、その特徴と天気の変化を分かりやすく日本語で150文字程度で解説してください。"
            ]
        )
        return {"result": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI解析エラー: {str(e)}")
