from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# CORS için daha kapsamlı bir çözüm
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    response.headers.add('Access-Control-Max-Age', '3600')
    # OPTIONS istekleri için hızlı yanıt
    if request.method == 'OPTIONS':
        return response
    return response

# OPTIONS istekleri için endpoint
@app.route('/chat', methods=['OPTIONS'])
def options():
    return '', 200

# AnythingLLM API URL ve anahtar
ANYTHINGLLM_API_URL = "https://0gjqsimv.rpcl.host/api/workspace/e-lokman/chat"
API_KEY = "K5K0TNA-D604WTM-P3D20RE-BSYP2B1"

@app.route('/')
def home():
    return "Flask çalışıyor! Chat için /chat rotasını kullanın (POST isteği)."

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Debug için request bilgilerini yazdır
        print(f"Gelen istek: {request.method} - Headers: {request.headers}")
        print(f"İstek JSON: {request.json}")
        
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"response": "Mesaj boş olamaz."}), 400

        # AnythingLLM'ye istek gönder
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        print(f"AnythingLLM'ye gönderilen istek: {user_message}")
        response = requests.post(ANYTHINGLLM_API_URL, json={"message": user_message}, headers=headers, timeout=30)
        
        # API yanıtını logla
        print(f"AnythingLLM status kodu: {response.status_code}")
        print(f"AnythingLLM yanıt headers: {response.headers}")
        
        try:
            llm_response = response.json()
            print(f"AnythingLLM JSON yanıtı: {llm_response}")
            reply = llm_response.get("reply", "Yanıt alınamadı.")
        except Exception as e:
            print(f"JSON parse hatası: {str(e)}")
            print(f"Ham yanıt: {response.text}")
            reply = "Yanıt formatı beklendiği gibi değil."
            
        return jsonify({"response": reply})
    
    except requests.exceptions.RequestException as e:
        error_msg = f"AnythingLLM hatası: {str(e)}"
        print(error_msg)
        return jsonify({"response": error_msg}), 500
    except Exception as e:
        error_msg = f"Genel hata: {str(e)}"
        print(error_msg)
        return jsonify({"response": error_msg}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
