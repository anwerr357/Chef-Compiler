from recetteAnalyse import analyser_sante_recette
import re
from recette_lexer import lexer
from recette_parser import parser
from recette_semantique import AnalyseurSemantique

def analyser_lexical_recette(texte):
    jetons = []
    for ligne in texte.splitlines():
        ligne = ligne.strip()
        if not ligne or ligne.startswith("#"):
            continue
        elif ligne.startswith("RECETTE"):
            jetons.append(("RECETTE", ligne.split(" ", 1)[1]))
        elif ligne == "INGRÉDIENTS":
            jetons.append(("SECTION", "INGRÉDIENTS"))
        elif ligne == "ÉTAPES":
            jetons.append(("SECTION", "ÉTAPES"))
        else:
            jetons.append(("TEXTE", ligne))
    return jetons

def analyser_syntaxique_recette(jetons):
    nom = None
    ingredients = []
    etapes = []
    mode = None
    sections_trouvees = {"INGRÉDIENTS": False, "ÉTAPES": False}

    for jeton in jetons:
        type_, valeur = jeton
        if type_ == "RECETTE":
            if nom:
                raise ValueError("❌ Deux recettes détectées.")
            nom = valeur
        elif type_ == "SECTION":
            if valeur not in sections_trouvees:
                raise ValueError(f"❌ Section inconnue : {valeur}")
            sections_trouvees[valeur] = True
            mode = valeur
        elif type_ == "TEXTE":
            if mode == "INGRÉDIENTS":
                ingredients.append(valeur)
            elif mode == "ÉTAPES":
                etapes.append(valeur)
            else:
                raise ValueError(f"❌ Texte trouvé en dehors d'une section valide : {valeur}")

    if not nom:
        raise ValueError("❌ La recette n'a pas de nom.")
    if not sections_trouvees["INGRÉDIENTS"]:
        raise ValueError("❌ Section INGRÉDIENTS manquante.")
    if not sections_trouvees["ÉTAPES"]:
        raise ValueError("❌ Section ÉTAPES manquante.")
    if not ingredients:
        raise ValueError("❌ Aucun ingrédient listé.")
    if not etapes:
        raise ValueError("❌ Aucune étape de préparation.")

    return {
        "nom": nom,
        "ingrédients": ingredients,
        "étapes": etapes
    }

def afficher_recette(recette):
    with open("analyse.txt", "w", encoding="utf-8") as f:
        f.write(f"\n🍽️ Préparation de la recette : \n")
        f.write(f"{recette['nom']} \n")
        f.write("\n🧂 Ingrédients :\n")
        for ingredient in recette['ingrédients']:
            f.write(f" - {ingredient} \n")
        f.write("\n👨‍🍳 Étapes :\n")
        for index, etape in enumerate(recette['etapes'], start=1):
            f.write(f"Étape {index} : {etape} \n")

def lire_recette(fichier):
    with open(fichier, "r", encoding="utf-8") as f:
        lignes = f.readlines()

    bloc_ingredients = []
    bloc_etapes = []
    section_courante = None

    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne:
            continue  # ignorer les lignes vides
        if ligne.startswith("INGRÉDIENTS"):
            section_courante = "ingredients"
            continue
        elif ligne.startswith("ÉTAPES"):
            section_courante = "etapes"
            continue
        elif ligne.startswith("RECETTE"):
            continue  # ignorer l'en-tête de la recette

        if section_courante == "ingredients":
            bloc_ingredients.append(ligne)
        elif section_courante == "etapes":
            bloc_etapes.append(ligne)

    return bloc_ingredients, bloc_etapes

if __name__ == "__main__":
    with open("recette.txt", encoding="utf-8") as f:
        contenu_recette = f.read()
    recette = parser.parse(contenu_recette, lexer=lexer)
    print("✅ Analyse lexicale et syntaxique réussie.")
    afficher_recette(recette)
    ingredients, etapes = lire_recette("recette.txt")
    
    analyseur = AnalyseurSemantique()
    analyseur.analyser(ingredients, etapes)
    print("✅ Analyse sémantique réussie.")
    
    analyser_sante_recette(recette)
