from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# AnythingLLM API URL (boşluğu kaldırdım, doğruysa bunu kullan)
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

        # AnythingLLM'ye istek gönder
        response = requests.post(ANYTHINGLLM_API_URL, json={"message": user_message})
        response.raise_for_status()  # Hata varsa (örneğin 404, 500) exception fırlatır
        
        # AnythingLLM'den gelen yanıtı al
        llm_reply = response.json().get("reply", "Yanıt alınamadı.")
        return jsonify({"reply": llm_reply})
    
    except requests.exceptions.RequestException as e:
        # AnythingLLM'ye ulaşılamazsa veya hata dönerse
        return jsonify({"reply": f"Üzgünüm, AnythingLLM'den yanıt alınamadı: {str(e)}"}), 500
    except Exception as e:
        # Genel hata durumu
        return jsonify({"reply": f"Bir hata oluştu: {str(e)}"}), 500

if __name__ == '__main__':
    # Render'ın dinamik portunu kullan
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
