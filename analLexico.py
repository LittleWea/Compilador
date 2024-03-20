import re

def lexer(expresion):
    tokens = []
    # Definir patrones para los diferentes tokens
    patron_palabra = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
    patron_simbolo_aritmetico = r'[\+\-\*/\^]'
    patron_numero_real = r'[-+]?\d+\.\d+'
    patron_numero_entero = r'[-+]?\d+'
    patron_simbolo_logico = r'[<>!=]=?'
    patron_parentesis = r'[\(\)]'
    patron_corchetes = r'[\[\]]'
    patron_llaves = r'[\{\}]'
    
    # Patrón general para ignorar saltos de línea y espacios
    patron_ignorar = r'\s+'

    # Combinar todos los patrones
    patron_general = '|'.join([patron_palabra, patron_simbolo_aritmetico, patron_numero_real,
                               patron_numero_entero, patron_simbolo_logico, patron_parentesis,
                               patron_corchetes, patron_llaves, patron_ignorar])

    # Iterar sobre las coincidencias en la expresión
    for match in re.finditer(patron_general, expresion):
        token = match.group().strip()
        # Descartar saltos de línea y espacios
        if token == '\n' or re.fullmatch(patron_ignorar, token):
            continue
        tokens.append(token)
    
    tokens = [elemento for elemento in tokens if elemento != '']

    return tokens
