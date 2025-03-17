from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# AnythingLLM API URL
ANYTHINGLLM_API_URL = "https://0gjqsimv.rpcl.host"

@app.route('/')
def home():
    return "Flask çalışıyor! Chat için /chat rotasını kullanın (POST isteği)."

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Kullanıcı mesajını al
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"reply": "Mesaj boş olamaz."}), 400

        # AnythingLLM'ye istek gönder ve hata kontrolü yap
        response = requests.post(ANYTHINGLLM_API_URL, json={"message": user_message}, timeout=10)
        response.raise_for_status()  # 4xx veya 5xx hatalarında exception fırlatır
        
        # Yanıtı al ve logla
        llm_response = response.json()
        print(f"AnythingLLM yanıtı: {llm_response}")  # Render loglarında görünür
        reply = llm_response.get("reply", "Yanıt alınamadı.")
        return jsonify({"reply": reply})
    
    except requests.exceptions.RequestException as e:
        error_msg = f"AnythingLLM hatası: {str(e)}"
        print(error_msg)  # Render loglarında görünür
        return jsonify({"reply": error_msg}), 500
    except Exception as e:
        error_msg = f"Genel hata: {str(e)}"
        print(error_msg)
        return jsonify({"reply": error_msg}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
