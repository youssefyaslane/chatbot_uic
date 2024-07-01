from flask import Flask, request, jsonify, render_template
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
import torch
import pandas as pd

from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Chemin vers le modèle sauvegardé
model_path = r'C:\Users\user\Desktop\Projetechnique\mypython\model'

# Charger le modèle et le tokenizer
model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(model_path)

# Charger le DataFrame avec les réponses
chemin_fichier_drive = r'C:\Users\user\Desktop\data (1).xlsx'

# Charger le fichier Excel dans un DataFrame
df = pd.read_excel(chemin_fichier_drive)

# Assurez-vous que les colonnes attendues sont présentes
if 'Tag' not in df.columns or 'response' not in df.columns:
    raise ValueError("Les colonnes 'Tag' et 'response' sont nécessaires dans le fichier Excel.")

# Créer une pipeline de classification de texte
classifier = pipeline('text-classification', model=model, tokenizer=tokenizer)

@app.route('/')
def home():
    return 'hello '

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data.get('text')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Faire une prédiction
    response = classifier(text)
    
    reply = ".عذراً، لم أتمكن من فهم رسالتك بشكل كامل. يُرجى إعادة كتابتها بشكل واضح أو بطريقة مختلفة حتى أتمكن من مساعدتك بشكل أفضل. شكراً لتفهمك وتعاونك"

    if response and response[0]['score'] >= 0.7:
        tag = response[0]['label']
        print(f"Predicted tag: {tag}")
        print(f"Prediction score: {response[0]['score']}")
        
        # Debug: Print all tags from DataFrame
        print("Tags in DataFrame:", df['Tag'].tolist())

        # Recherchez la réponse associée au tag dans le DataFrame
        matched_row = df[df['Tag'].str.strip().str.lower() == tag.strip().lower()]
        print(f"Matched row: {matched_row}")

        if not matched_row.empty:
            reply = matched_row['response'].values[0]
    
    return jsonify({'reply': reply}), 200

if __name__ == '__main__':
    app.run(debug=True)
