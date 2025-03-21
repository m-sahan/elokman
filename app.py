from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS  # CORS ekleyin

app = Flask(__name__)
CORS(app)  # CORS'u etkinleştirin

# AnythingLLM API URL ve anahtar
ANYTHINGLLM_API_URL = "https://0gjqsimv.rpcl.host/api/workspace/e-lokman/chat"
API_KEY = "K5K0TNA-D604WTM-P3D20RE-BSYP2B1"  # Bearer kısmını çıkardım

@app.route('/')
def home():
    return "Flask çalışıyor! Chat için /chat rotasını kullanın (POST isteği)."

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"response": "Mesaj boş olamaz."}), 400  # reply -> response

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
        return jsonify({"response": reply})  # reply -> response
    
    except requests.exceptions.RequestException as e:
        error_msg = f"AnythingLLM hatası: {str(e)}"
        print(error_msg)
        return jsonify({"response": error_msg}), 500  # reply -> response
    except Exception as e:
        error_msg = f"Genel hata: {str(e)}"
        print(error_msg)
        return jsonify({"response": error_msg}), 500  # reply -> response

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
