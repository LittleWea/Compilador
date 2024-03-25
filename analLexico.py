import re

def lexer(expresion):
    tokens = []
    # Definir patrones para los diferentes tokens
    patron_palabra = r'\b[a-zA-Z_@][a-zA-Z0-9_@]*\b'
    patron_cadena_entre_dos_simbolos = r'##[^#]+##'
    patron_com = r'#[^\n]*'
    patron_simbolo_aritmetico = r'[\+\-\*/\^\%]'
    patron_numero_real = r'[-+]?\d+\.\d+'
    patron_numero_entero = r'[-+]?\d+'
    patron_simbolo_logico = r'[<>!=]=?'
    patron_parentesis = r'[\(\)]'
    patron_corchetes = r'[\[\]]'
    patron_llaves = r'[\{\}]'
    patron_punto = r'[\,\;]'
    patron_operadores_logicos = r'\|\||&&'
    patron_objeto = r'\b[a-zA-Z_@]\.[a-zA-Z0-9_@]*\b'

    # Patrón general para ignorar saltos de línea y espacios
    patron_ignorar = r'\s+'

    # Combinar todos los patrones
    patron_general = '|'.join([
        patron_cadena_entre_dos_simbolos,
        patron_palabra,
        patron_simbolo_aritmetico,
        patron_numero_real,
        patron_numero_entero,
        patron_com,
        patron_simbolo_logico,
        patron_parentesis,
        patron_corchetes,
        patron_llaves,
        patron_punto,
        patron_operadores_logicos,
        patron_objeto,
        patron_ignorar
    ])

    # Iterar sobre las coincidencias en la expresión
    for match in re.finditer(patron_general, expresion):
        token = match.group().strip()
        # Descartar saltos de línea y espacios
        if token == '\n' or re.fullmatch(patron_ignorar, token):
            continue
        tokens.append(token)

    tokens = [elemento for elemento in tokens if elemento != '']

    return tokens

def tipoToken( expresion):
    patron_palabra = r'\b[a-zA-Z_@][a-zA-Z0-9_@]*\b'
    patron_com = r'#[^\n]*'
    patron_cadena_entre_dos_simbolos = r'##[^#]+##'
    patron_simbolo_aritmetico = r'[\+\-\*/\^\%]'
    patron_numero_real = r'[-+]?\d+\.\d+'
    patron_numero_entero = r'[-+]?\d+'
    patron_simbolo_logico = r'[<>!=]=?'
    patron_parentesis = r'[\(\)]'
    patron_corchetes = r'[\[\]]'
    patron_llaves = r'[\{\}]'
    patron_objeto = r'\b[a-zA-Z_@]\.[a-zA-Z0-9_@]*\b'
    patron_punto = r'[\,\;]'
    patron_operadores_logicos = r'\|\||&&'
    if( (expresion == 'if') | (expresion == 'othewise') | (expresion == 'do') | (expresion == 'while') | 
       (expresion == 'switch') | (expresion == 'case') | (expresion == 'integer') | (expresion == 'double') | 
       (expresion == 'main') | (expresion == 'return')|(expresion == 'else')):
        return 'palabra reservada'
    elif(re.fullmatch(patron_cadena_entre_dos_simbolos, expresion)):
        return 'comentario'
    elif(re.fullmatch(patron_com, expresion)):
        return 'comentario'
    elif(re.fullmatch(patron_palabra, expresion)):
        return 'identificador'
    elif(re.fullmatch(patron_simbolo_aritmetico, expresion)):
        return 'simbolo aritmetico'
    elif(re.fullmatch(patron_numero_real, expresion)):
        return 'numero real'
    elif(re.fullmatch(patron_numero_entero, expresion)):
        return 'numero entero'
    elif(re.fullmatch(patron_simbolo_logico, expresion)):
        return 'sibolo logico'
    elif(re.fullmatch(patron_parentesis, expresion)):
        return 'simbolo parentesis'
    elif(re.fullmatch(patron_corchetes, expresion)):
        return 'simbolo corchete'
    elif(re.fullmatch(patron_llaves, expresion)):
        return 'simbolo llave'
    elif(re.fullmatch(patron_punto, expresion)):
        return 'simbolo puntuacion'
    elif(re.fullmatch(patron_operadores_logicos, expresion)):
        return 'operador logico'
    elif(re.fullmatch(patron_objeto, expresion)):
        return 'objeto con funcion'
