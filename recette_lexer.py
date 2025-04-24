import ply.lex as lex

tokens = (
    'RECETTE',
    'SECTION',
    'TEXT',
    'NEWLINE',
)

t_ignore = ' \t'

def t_RECETTE(t):
    r'RECETTE\s+.+'
    t.value = t.value.split(' ', 1)[1]
    return t

def t_SECTION(t):
    r'INGRÉDIENTS|ÉTAPES'
    return t

def t_TEXT(t):
    r'[^\n]+'
    return t

def t_NEWLINE(t):
    r'\n+'
    pass

def t_error(t):
    print(f"Caractère illégal : {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()
    