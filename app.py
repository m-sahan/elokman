from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# AnythingLLM API URL ve anahtar
ANYTHINGLLM_API_URL = "https://0gjqsimv.rpcl.host/api/workspace/e-lokman/stream-chat"
API_KEY = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJhZG1pbiIsImlhdCI6MTc0MTg1OTc2NSwiZXhwIjoxNzQ0NDUxNzY1fQ.m2A2fvLU_nsgxIN0rt93K5z96HUr2ZCkdavDu4_DDLU",
"Content-Type": "application/json"

@app.route('/')
def home():
    return "Flask çalışıyor! Chat için /chat rotasını kullanın (POST isteği)."

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"reply": "Mesaj boş olamaz."}), 400

        # AnythingLLM'ye istek gönder
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        response = requests.post(ANYTHINGLLM_API_URL, json={"message": user_message}, headers=headers, timeout=10)
        response.raise_for_status()
        
        llm_response = response.json()
        print(f"AnythingLLM yanıtı: {llm_response}")
        reply = llm_response.get("reply", "Yanıt alınamadı.")
        return jsonify({"reply": reply})
    
    except requests.exceptions.RequestException as e:
        error_msg = f"AnythingLLM hatası: {str(e)}"
        print(error_msg)
        return jsonify({"reply": error_msg}), 500
    except Exception as e:
        error_msg = f"Genel hata: {str(e)}"
        print(error_msg)
        return jsonify({"reply": error_msg}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
