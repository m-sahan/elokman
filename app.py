from flask import Flask, request, jsonify
import requests  # AnythingLLM API çağırmak için

app = Flask(__name__)

# AnythingLLM API URL (kendi AnythingLLM sunucunun URL'sini ekle)
ANYTHINGLLM_API_URL = " https://0gjqsimv.rpcl.host"

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")

    # AnythingLLM'ye istek gönder
    response = requests.post(ANYTHINGLLM_API_URL, json={"message": user_message})
    llm_reply = response.json().get("reply", "Yanıt alınamadı.")

    return jsonify({"reply": llm_reply})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
