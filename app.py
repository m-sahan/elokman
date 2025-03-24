import os
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import google.generativeai as genai
from dotenv import load_dotenv
import logging
from datetime import datetime

# Ortam değişkenlerini yükle
load_dotenv()

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)
logger = logging.getLogger(__name__)

# Flask uygulamasını oluştur
app = Flask(__name__)

# CORS ayarları
ALLOWED_ORIGINS = [
    'https://0gjqsimv.rpcl.host',  # Repocloud URL
    'https://elokman.onrender.com',  # Render URL
    'http://localhost:5000',  # Yerel geliştirme
    'http://127.0.0.1:5000'
]

CORS(app, resources={
    r"/generate": {
        "origins": ALLOWED_ORIGINS,
        "methods": ["POST"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Rate Limiting ayarları
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per day", "30 per hour"]
)

# Gemini API Konfigürasyonu
try:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    if not GEMINI_API_KEY:
        raise ValueError("Gemini API Key bulunamadı")
    
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Gemini Modeli Yapılandırması
    model = genai.GenerativeModel(
        'gemini-1.5-pro-latest',
        generation_config={
            "max_output_tokens": 1000,  # Maksimum token sınırı
            "temperature": 0.7,  # Yaratıcılık seviyesi
            "top_p": 1  # Olasılık kümeleme
        }
    )
except Exception as config_error:
    logger.error(f"Gemini API Konfigürasyon Hatası: {config_error}")
    raise

# Güvenlik için input sanitization
def sanitize_input(text):
    # Temel input temizleme
    max_length = 500  # Maksimum girdi uzunluğu
    return text[:max_length].strip()

@app.route('/generate', methods=['POST'])
@limiter.limit("10 per minute")
def generate_response():
    # Origin kontrolü
    origin = request.headers.get('Origin')
    if origin not in ALLOWED_ORIGINS:
        logger.warning(f"Yetkisiz origin girişimi: {origin}")
        abort(403, description="Yetkisiz erişim")

    try:
        # JSON veri kontrolü
        if not request.is_json:
            abort(400, description="JSON formatında veri gönderin")
        
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        
        # Prompt doğrulaması
        if not prompt:
            abort(400, description="Prompt boş olamaz")
        
        # Input sanitization
        clean_prompt = sanitize_input(prompt)
        
        # Gemini'den yanıt alma
        response = model.generate_content(clean_prompt)
        
        # Yanıt log'lama
        logger.info(f"Başarılı yanıt - Prompt uzunluğu: {len(clean_prompt)}")
        
        return jsonify({
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'response': response.text,
            'prompt_length': len(clean_prompt)
        }), 200
    
    except genai.types.generation_types.BlockedPromptException as block_error:
        logger.error(f"Engellenen prompt: {block_error}")
        return jsonify({
            'status': 'error',
            'message': 'İçerik politikalarına aykırı içerik'
        }), 400
    
    except Exception as e:
        logger.error(f"Bilinmeyen hata: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Sunucu tarafında bir hata oluştu'
        }), 500

# Genel hata yakalayıcılar
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'status': 'error',
        'message': str(error.description)
    }), 400

@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        'status': 'error',
        'message': 'Erişim reddedildi'
    }), 403

@app.errorhandler(429)
def ratelimit_handler(error):
    return jsonify({
        'status': 'error',
        'message': 'Çok fazla istek. Lütfen bekleyin.'
    }), 429

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
