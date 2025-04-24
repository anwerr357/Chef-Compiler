from recipeAnalyser import analyser_sante_recette
import re
from recette_lexer import lexer
from recette_parser import parser
def lexer_recette(text):
    tokens = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        elif line.startswith("RECETTE"):
            tokens.append(("RECETTE", line.split(" ", 1)[1]))
        elif line == "INGRÉDIENTS":
            tokens.append(("SECTION", "INGRÉDIENTS"))
        elif line == "ÉTAPES":
            tokens.append(("SECTION", "ÉTAPES"))
        else:
            tokens.append(("TEXT", line))
    return tokens
def parser_recette(tokens):
    nom = None
    ingredients = []
    etapes = []
    mode = None
    section_found = {"INGRÉDIENTS": False, "ÉTAPES": False}

    for token in tokens:
        type_, value = token
        if type_ == "RECETTE":
            if nom:
                raise ValueError("❌ Deux recettes détectées.")
            nom = value
        elif type_ == "SECTION":
            if value not in section_found:
                raise ValueError(f"❌ Section inconnue : {value}")
            section_found[value] = True
            mode = value
        elif type_ == "TEXT":
            if mode == "INGRÉDIENTS":
                ingredients.append(value)
            elif mode == "ÉTAPES":
                etapes.append(value)
            else:
                raise ValueError(f"❌ Texte trouvé en dehors d'une section valide : {value}")

    if not nom:
        raise ValueError("❌ La recette n'a pas de nom.")
    if not section_found["INGRÉDIENTS"]:
        raise ValueError("❌ Section INGRÉDIENTS manquante.")
    if not section_found["ÉTAPES"]:
        raise ValueError("❌ Section ÉTAPES manquante.")
    if not ingredients:
        raise ValueError("❌ Aucun ingrédient listé.")
    if not etapes:
        raise ValueError("❌ Aucune étape de préparation.")

    return {
        "nom": nom,
        "ingrédients": ingredients,
        "etapes": etapes
    }
def afficher_recette(recette):
    with open("analyse.txt", "w", encoding="utf-8") as f:
        f.write(f"\n🍽️ Préparation de la recette : \n")
        f.write(f"{recette['nom']} \n")
        f.write("\n🧂 Ingrédients :\n")
        for ingredient in recette['ingrédients']:
            f.write(f" - {ingredient} \n")
        f.write("\n👨‍🍳 Étapes :")
        for index, etape in enumerate(recette['etapes'], start=1):
            f.write(f"Étape {index} : {etape} \n")



if __name__ == "__main__":
    with open("recette.txt", encoding="utf-8") as f:
        recette = f.read()
    recette = parser.parse(recette, lexer=lexer)
    afficher_recette(recette)
    analyser_sante_recette(recette)
