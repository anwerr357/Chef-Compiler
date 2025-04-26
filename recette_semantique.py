class AnalyseurSemantique:
    def __init__(self):
        self.ingredients = set()

    def ajouter_ingredient(self, nom):
        if nom in self.ingredients:
            raise Exception(f"Erreur sémantique : ingrédient '{nom}' déjà déclaré.")
        self.ingredients.add(nom)

    def verifier_etape(self, ligne_etape):
        mots = ligne_etape.split()
        actions_connues = {"fondre", "ajouter", "mélanger", "cuire"}
        if not any(action in mots for action in actions_connues):
            raise Exception(f"Erreur sémantique : aucune action reconnue dans l'étape : '{ligne_etape}'")
        for action in actions_connues:
            if action in mots:
                index = mots.index(action)
                # print(index)
                # print(action)
                objets = mots[index + 1:]
                for objet in objets:
                    objet = objet.strip(",")
                    if objet.isdigit() or objet.endswith("min") or "°C" or "à" in objet:
                        continue
                    if objet not in self.ingredients:
                        raise Exception(f"Erreur sémantique : objet {objet} non déclaré comme ingrédient.")
                break

    def analyser(self, bloc_ingredients, bloc_etapes):
        for ligne in bloc_ingredients:
            parties = ligne.strip().split()
            if len(parties) >= 3:
                nom = " ".join(parties[2:])
                self.ajouter_ingredient(nom)
            else:
                nom = " ".join(parties[1:])
                self.ajouter_ingredient(nom)

        for etape in bloc_etapes:
            self.verifier_etape(etape)

# Main

