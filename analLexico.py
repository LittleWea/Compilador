import re

def lexer(expresion):
    tokens = []
    # Definir patrones para los diferentes tokens
    patron_palabra = r'\b[a-zñA-ZÑ_][a-zñA-ZÑ0-9_]*\b'
    patron_cadena_entre_dos_simbolos = r'##[^#]+##'
    patron_comentario = r'#[^\n]*'
    patron_simbolo_aritmetico = r'[\+\-\*/\^\%]'
    patron_simbolo_aritmetico2 = r'\+\+|--'
    patron_numero_real = r'[-+]?\d+\.\d+'
    patron_numero_entero = r'[-+]?\d+'
    patron_simbolo_logico = r'[<>]=?'
    patron_simbolo_logico2 = r'[!=]='
    patron_parentesis = r'[\(\)]'
    patron_corchetes = r'[\[\]]'
    patron_llaves = r'[\{\}]'
    patron_punto = r'[\,\;]'
    patron_operadores_logicos = r'\|\||&&'
    patron_ignorar = r'[\n\s]+'
    patron_error = r'.'

    fila = 1
    columna = 1
    
    patron_general = '|'.join([
        patron_cadena_entre_dos_simbolos,
        patron_comentario,
        patron_palabra,
        patron_simbolo_aritmetico2,
        patron_simbolo_aritmetico,
        patron_numero_real,
        patron_numero_entero,
        patron_simbolo_logico,
        patron_simbolo_logico2,
        patron_parentesis,
        patron_corchetes,
        patron_llaves,
        patron_punto,
        patron_operadores_logicos,
        patron_ignorar,
        patron_error
    ])

    for match in re.finditer(patron_general, expresion):
        token = match.group().strip()
        columna = match.start() - expresion.rfind('\n', 0, match.start())
        start_pos = match.start()
        line = expresion.count('\n', 0, start_pos) + 1

        if token == '\n' or re.fullmatch(patron_ignorar, token):
            continue
        tokens.append((token, line, columna))

    tokens = [elemento for elemento in tokens if elemento[0] != '']

    return tokens

def tipoToken(expresion):
    patron_palabra = r'\b[a-zñA-ZÑ_][a-zñA-ZÑ0-9_]*\b'
    patron_cadena_entre_dos_simbolos = r'##[^#]+##'
    patron_com = r'#[^\n]*'
    patron_simbolo_aritmetico = r'[\+\-\*/\^\%\=]'
    patron_simbolo_aritmetico2 = r'\+\+|--'
    patron_numero_real = r'[-+]?\d+\.\d+'
    patron_numero_entero = r'[-+]?\d+'
    patron_simbolo_logico = r'[<>]=?'
    patron_simbolo_logico2 = r'[!=]='
    patron_parentesis = r'[\(\)]'
    patron_corchetes = r'[\[\]]'
    patron_llaves = r'[\{\}]'
    patron_punto = r'[\,\;]'
    patron_operadores_logicos = r'\|\||&&'

    patron_general = '|'.join([
            patron_cadena_entre_dos_simbolos,
            patron_com,
            patron_palabra,
            patron_simbolo_aritmetico,
            patron_simbolo_aritmetico2,
            patron_simbolo_logico2,
            patron_numero_real,
            patron_numero_entero,
            patron_com,
            patron_simbolo_logico,
            patron_parentesis,
            patron_corchetes,
            patron_llaves,
            patron_punto,
            patron_operadores_logicos
        ])

    if( (expresion == 'if') | (expresion == 'othewise') | (expresion == 'do') | (expresion == 'while') | 
       (expresion == 'switch') | (expresion == 'case') | (expresion == 'integer') | (expresion == 'double') | 
       (expresion == 'main') | (expresion == 'return') | (expresion == 'else') | (expresion == 'cin') | (expresion == 'cout')):
        return 'palabra reservada'
    elif(re.fullmatch(patron_cadena_entre_dos_simbolos, expresion)):
        return 'comentario'
    elif(re.fullmatch(patron_palabra, expresion)):
        return 'identificador'
    elif(re.fullmatch(patron_simbolo_aritmetico, expresion ) or re.fullmatch(patron_simbolo_aritmetico2, expresion)):
        return 'simbolo aritmetico'
    elif(re.fullmatch(patron_numero_real, expresion)):
        return 'numero real'
    elif(re.fullmatch(patron_numero_entero, expresion)):
        return 'numero entero'
    elif(re.fullmatch(patron_simbolo_logico, expresion) or re.fullmatch(patron_simbolo_logico2, expresion) ):
        return 'simbolo logico'
    elif(re.fullmatch(patron_parentesis, expresion)):
        return 'simbolo parentesis'
    elif(re.fullmatch(patron_corchetes, expresion)):
        return 'simbolo corchete'
    elif(re.fullmatch(patron_llaves, expresion)):
        return 'simbolo llave'
    elif(re.fullmatch(patron_punto, expresion)):
        return 'simbolo puntuacion'
    elif (re.fullmatch(patron_operadores_logicos, expresion)):
        return 'operador logico'
    elif (re.fullmatch(patron_general, expresion) == None):
        return 'error'
