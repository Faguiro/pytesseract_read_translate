from flask import Flask, render_template, request, jsonify, url_for 
from notification import notify


import pytesseract
from langdetect import detect
from googletrans import Translator

app = Flask(__name__)

app.static_folder = 'static'

from PIL import Image, ImageEnhance, ImageFilter

def preprocess_image(image):
    # Ajusta o contraste
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)

    # Aplica uma filtragem para realçar as bordas
    image = image.filter(ImageFilter.EDGE_ENHANCE)

    # Binariza a imagem (converte para preto e branco)
    image = image.convert("L")

    # Ajusta o limiar para binarização
    threshold = 200
    image = image.point(lambda p: p > threshold and 255)

    # Redimensiona a imagem para uma altura específica (opcional)
    target_height = 1500
    aspect_ratio = image.width / image.height
    target_width = int(target_height * aspect_ratio)
    image = image.resize((target_width, target_height))

    return image

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/extract", methods=["POST"])
def extract():
    try:
        file = request.files["image"]

        # Verifica se o arquivo é uma imagem válida
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            return jsonify({"error": "Formato de arquivo não suportado"}), 400

        image = Image.open(file).convert("RGB")

        # Pré-processa a imagem para melhorar a qualidade do OCR
        preprocessed_image = preprocess_image(image)
        text = pytesseract.image_to_string(preprocessed_image)

        # Detecta o idioma do texto extraído
        lang = detect(text)

        # Traduz o texto para português, inglês, alemão e espanhol
        translator = Translator()
        translations = {
            "pt": translator.translate(text, dest="pt").text,
            "en": translator.translate(text, dest="en").text,
            "de": translator.translate(text, dest="de").text,
            "es": translator.translate(text, dest="es").text
        }

        # Cria um dicionário com as versões em diferentes idiomas e o idioma detectado
        result = {"text": text, "lang": lang, "translations": translations}

        notify("Extracted Text", text, duration=10)

        # Retorna o resultado como um JSON
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
