from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # Cross-Origin Resource Sharing desteği

# API Key Ayarları
genai.configure(api_key='AIzaSyBXekNRn2DCqsHN6op2x1XwkOxSg7IlM9U')

# Gemini Modeli Yükleme
model = genai.GenerativeModel(
    'gemini-1.5-pro-latest',
    generation_config={
        "max_output_tokens": 1100,  # Maksimum 1000 token sınırı
        "temperature": 0.7,  # Yaratıcılık seviyesi
        "top_p": 1  # Olasılık kümeleme
    }
)

@app.route('/generate', methods=['POST'])
def generate_response():
    try:
        data = request.json
        prompt = data.get('prompt', '')
        
        # Gemini'den yanıt alma
        response = model.generate_content(prompt)
        
        return jsonify({
            'status': 'success',
            'response': response.text
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
