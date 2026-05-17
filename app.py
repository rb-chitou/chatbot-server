from flask import Flask, request, jsonify
  from flask_cors import CORS
  import requests
  import os

  app = Flask(__name__)
  CORS(app)

  MISTRAL_KEY = os.environ.get("MISTRAL_API_KEY")
  MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"

  SYSTEM_PROMPT = """Tu es l'assistant du jeu mobile Minivilles (adaptation de 
  Machi Koro).
  Réponds en français ou anglais selon la langue de l'utilisateur. Sois concis 
  et amical.

  RÈGLES : 2 à 4 joueurs. Champ de blé (1) + Boulangerie (2-3) + 3 pièces au 
  départ.
  Tour : 1) Lancer les dés  2) Collecter revenus  3) Acheter une carte 
  (facultatif)
  Ordre des effets : Rouge → Vert → Bleu → Violet. Victoire : 5 monuments 
  construits.
  
  MONUMENTS : Port (2), Gare (4), Centre Commercial (10), Parc (16), Tour Radio 
  (22), Aéroport (30)
  ÉTABLISSEMENTS : Chalutier (bleu,8), Pizzeria (rouge,7), Restaurant 
  (rouge,9-10), Moonster Soda (rouge,7), Entreprise Travaux (vert,4-5-6)"""

  @app.route("/api/chat", methods=["POST"])
  def chat():
      if not MISTRAL_KEY:
          return jsonify({"error": "Clé API manquante"}), 500
      data = request.get_json()
      messages = data.get("messages", [])
      payload = {
          "model": "mistral-small-latest",               
          "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
          "max_tokens": 300
      }
      try:
          resp = requests.post(                          
              MISTRAL_URL,
              headers={"Authorization": f"Bearer {MISTRAL_KEY}", "Content-Type":
   "application/json"},
              json=payload, timeout=15
          )
          return jsonify(resp.json()), resp.status_code  
      except Exception as e:
          return jsonify({"error": str(e)}), 500

  @app.route("/health", methods=["GET"])
  def health():
      return jsonify({"status": "ok"})                   

  if __name__ == "__main__":
      port = int(os.environ.get("PORT", 5000))
      app.run(host="0.0.0.0", port=port)

