from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import google.generativeai as genai


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Gemini API Anahtarı ve URL
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyBXekNRn2DCqsHN6op2x1XwkOxSg7IlM9U")
GEMINI_API_URL = f"https://0gjqsimv.rpcl.host/workspace/e-lokman/{GEMINI_API_KEY}"

@app.route('/')
def home():
    return "Flask çalışıyor! Gemini Chat için /chat rotasını kullanın (POST isteği)."

@app.route('/chat', methods=['POST', 'OPTIONS'])
@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'success'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response

    try:
        # 'contents' içinde kullanıcı mesajını alın
        user_message = request.json.get("contents", [{}])[0].get("parts", [{}])[0].get("text", "")
        
        if not user_message:
            return jsonify({"reply": "Mesaj boş olamaz."}), 400

        # Gemini API'ye istek gönder
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "contents": [
                {"role": "user", "parts": [{"text": user_message}]}
            ],
            "generationConfig": {
                "maxOutputTokens": 1200
            }
        }

        response = requests.post(GEMINI_API_URL, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()
        reply = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Yanıt alınamadı.")
        return jsonify({"reply": reply})

    except requests.exceptions.RequestException as e:
        return jsonify({"reply": f"Gemini API hatası: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"reply": f"Genel hata: {str(e)}"}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
