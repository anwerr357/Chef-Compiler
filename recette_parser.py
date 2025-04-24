import ply.yacc as yacc
from recette_lexer import tokens

def p_recette(p):
    '''recette : RECETTE section_ingredients section_etapes'''
    p[0] = {
        "nom": p[1],
        "ingrédients": p[2],
        "etapes": p[3]
    }

def p_section_ingredients(p):
    '''section_ingredients : SECTION ingredients'''
    if p[1] != "INGRÉDIENTS":
        raise SyntaxError("Attendu : INGRÉDIENTS")
    p[0] = p[2]

def p_ingredients(p):
    '''ingredients : TEXT ingredients
                   | TEXT'''
    p[0] = [p[1]] + (p[2] if len(p) == 3 else [])

def p_section_etapes(p):
    '''section_etapes : SECTION etapes'''
    if p[1] != "ÉTAPES":
        raise SyntaxError("Attendu : ÉTAPES")
    p[0] = p[2]

def p_etapes(p):
    '''etapes : TEXT etapes
              | TEXT'''
    p[0] = [p[1]] + (p[2] if len(p) == 3 else [])

def p_error(p):
    if p:
        print(f"Erreur syntaxique à: {p.value}")
    else:
        print("Erreur syntaxique en fin de fichier")

parser = yacc.yacc()
