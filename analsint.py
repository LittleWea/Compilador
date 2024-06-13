# analsint.py

# Importa las funciones necesarias del módulo lexer
from analLexico import lexer, tipoToken
class SyntaxError(Exception):
    def __init__(self, mensaje, fila, columna):
        super().__init__(mensaje)
        self.fila = fila
        self.columna = columna
# Función para consumir un token esperado
def consume_token(tokens, expected_token):
    if tokens and tokens[0][0] == expected_token:
        tokens.pop(0)
        return True
    return False

# Funciones correspondientes a cada símbolo no terminal de la gramática
def programa(tokens):
    if consume_token(tokens, "main"):
        if consume_token(tokens, "{"):
            lista_declaracion(tokens)
            if consume_token(tokens, "}"):
                return True
    # Si no se cumple alguna parte de la gramática, lanzar una excepción SyntaxError
    raise SyntaxError("Error en el análisis sintáctico", tokens[0].fila, tokens[0].columna)

def lista_declaracion(tokens):
    while True:
        if not declaracion(tokens):
            break

def declaracion(tokens):
    return declaracion_variable(tokens) or lista_sentencias(tokens)

def declaracion_variable(tokens):
    if tipo(tokens):
        if identificador(tokens):
            if consume_token(tokens, ";"):
                return True
    return False

def identificador(tokens):
    if consume_token(tokens, "id"):
        while consume_token(tokens, ","):
            if not consume_token(tokens, "id"):
                return False
        return True
    return False

def tipo(tokens):
    return consume_token(tokens, "integer") or consume_token(tokens, "double")

def lista_sentencias(tokens):
    while True:
        if not sentencia(tokens):
            break

def sentencia(tokens):
    return seleccion(tokens) or iteracion(tokens) or repeticion(tokens) or sent_in(tokens) or sent_out(tokens) or asignacion(tokens)

def asignacion(tokens):
    if consume_token(tokens, "="):
        if sent_expresion(tokens):
            return True
    return False

def sent_expresion(tokens):
    if expresion(tokens):
        if consume_token(tokens, ";"):
            return True
    return False

def seleccion(tokens):
    if consume_token(tokens, "if"):
        if expresion(tokens):
            if sentencia(tokens):
                if consume_token(tokens, "end"):
                    return True
    return False

def iteracion(tokens):
    if consume_token(tokens, "while"):
        if expresion(tokens):
            if sentencia(tokens):
                if consume_token(tokens, "end"):
                    return True
    return False

def repeticion(tokens):
    if consume_token(tokens, "do"):
        if sentencia(tokens):
            if consume_token(tokens, "while"):
                if expresion(tokens):
                    return True
    return False

def sent_in(tokens):
    if consume_token(tokens, "cin"):
        if consume_token(tokens, "id"):
            if consume_token(tokens, ";"):
                return True
    return False

def sent_out(tokens):
    if consume_token(tokens, "cout"):
        if expresion(tokens):
            if consume_token(tokens, ";"):
                return True
    return False

def expresion(tokens):
    if expresion_simple(tokens):
        if relacion_op(tokens):
            if expresion_simple(tokens):
                return True
        return True  # La expresión puede ser solo un término
    return False

def relacion_op(tokens):
    return consume_token(tokens, "<") or consume_token(tokens, "<=") or consume_token(tokens, ">") or consume_token(tokens, ">=") or consume_token(tokens, "==") or consume_token(tokens, "!=")

def expresion_simple(tokens):
    if termino(tokens):
        while suma_op(tokens):
            if not termino(tokens):
                return False
        return True
    return False

def suma_op(tokens):
    return consume_token(tokens, "+") or consume_token(tokens, "-")

def termino(tokens):
    if factor(tokens):
        while mult_op(tokens):
            if not factor(tokens):
                return False
        return True
    return False

def mult_op(tokens):
    return consume_token(tokens, "*") or consume_token(tokens, "/") or consume_token(tokens, "%")

def factor(tokens):
    if componente(tokens):
        while pot_op(tokens):
            if not componente(tokens):
                return False
        return True
    return False

def pot_op(tokens):
    return consume_token(tokens, "++") or consume_token(tokens, "--")

def componente(tokens):
    if consume_token(tokens, "("):
        if expresion(tokens):
            if consume_token(tokens, ")"):
                return True
    elif consume_token(tokens, "numero"):
        return True
    elif consume_token(tokens, "id"):
        return True
    return False

# Función principal de análisis sintáctico
def analisis_sintactico(tokens):
    """
    Realiza el análisis sintáctico de una lista de tokens.

    Parameters:
        tokens (list): Una lista de tokens generados por el analizador léxico.

    Returns:
        bool: True si el análisis sintáctico es exitoso, False de lo contrario.
    """
    if programa(tokens):
        if not tokens:
            return True
    return False

# tokens es una lista de tokens generados por el analizador léxico

        