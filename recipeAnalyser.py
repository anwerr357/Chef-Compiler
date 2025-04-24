# recipeAnalyser.py
import ollama
from textwrap import fill
import time
import openai
from dotenv import load_dotenv
import os

load_dotenv()
def analyser_sante_recette(recette):
    ingredients = recette["ingrédients"]  
    prompt = f"""
Tu es un assistant en nutrition. Analyse cette recette et donne une estimation des calories, lipides, sucres et protéines.
Dis aussi si la recette est saine ou non. Voici la recette :

Nom : {recette['nom']}
Ingrédients : {', '.join(ingredients)}
Étapes : {" ".join(recette['etapes'])}
"""
    API_KEY = os.getenv("API_KEY")
    #together ai key 
    openai.api_key = API_KEY
    openai.api_base = "https://api.together.xyz/v1"
    try:
        start = time.time()
        response = openai.ChatCompletion.create(
            model="meta-llama/Llama-3-8b-chat-hf",
            messages=[{"role": "user", "content": prompt}]
            )

        end = time.time()
        print(f"\n⏱️ Temps d'exécution : {end - start:.2f} secondes")
        print("\n🧠 Analyse santé de la recette :\n")
        with open("analyse.txt", "a", encoding="utf-8") as f:
            f.write("🧠 Analyse santé de la recette :\n\n")
            f.write(response["choices"][0]["message"]["content"])
    except Exception as e:
        print("❌ Erreur lors de l’analyse avec le modèle IA :", e)

