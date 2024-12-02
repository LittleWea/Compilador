from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget
from anytree import Node, RenderTree
import ply.lex as lex
import ply.yacc as yacc
import hashlib

class Simbolo:
    def __init__(self, nombre, tipo, valor=None):
        self.nombre = nombre
        self.tipo = tipo
        self.valor = valor
        self.lineas = []

    def __repr__(self):
        return f"Simbolo(nombre={self.nombre}, tipo={self.tipo}, valor={self.valor}, lineas={self.lineas})"

class TablaDeSimbolos:
    def __init__(self):
        # El diccionario almacenará los símbolos
        self.tabla = {}

    def agregar_simbolo(self, nombre, tipo, valor=None):
        if nombre not in self.tabla:
            self.tabla[nombre] = Simbolo(nombre, tipo, valor)

    def obtener_simbolo(self, nombre):
        return self.tabla.get(nombre, None)

    def existe_simbolo(self, nombre):
        return nombre in self.tabla

    def actualizar_valor(self, nombre, valor):
        if nombre in self.tabla:
            self.tabla[nombre].valor = valor
        
    def actualizar_lineas(self, nombre, linea):
        if nombre in self.tabla:
            self.tabla[nombre].lineas.append(linea)

    def mostrar_tabla(self):
        for nombre, simbolo in self.tabla.items():
            print(f"{nombre}: {simbolo}")

    def mostrar_hash(self):
        data = ""
        for nombre, simbolo in self.tabla.items():
            data += f"{nombre}:{simbolo}" 
        print("a!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(data)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return data

# Ejemplo de uso de la tabla de símbolos
tabla_simbolos = TablaDeSimbolos()
tabla_simbolos_lineas = TablaDeSimbolos()

errorSem = []

compSymb = ['<', '<=', '==', '>', '>=', '!=', '&&', '||']

artSymb = ['*', '^', '+', '-', '/', '%']

stNames = ['While', 'If', 'Block', 'DoWhile', 'IfElse', 'Program', 'Main', 'integer', 'VarDecl', 'Variables', 'double', 'Cin', 'Cout', 'Assign']

tokens = (
    'MAIN', 'INTEGER', 'DOUBLE', 'BOOLEAN', 'IDENTIFIER', 'NUMBER', 'REALNUMBER', 'BOOL', 'SUMDOUBLE', 'MINUSDOUBLE', 'SUM', 'MINUS', 'TIMES', 'DIVISION', 'MODULE', 'POW',
    'ASSIGN', 'PARLEFT', 'PARRIGHT', 'SQRLEFT', 'SQRRIGHT', 'KEYLEFT', 'KEYRIGHT', 'COMMA', 'DOTCOMMA', 'DOUBLEDOT', 'SINGLECOMMENT', 'MULTIPLECOMMENT', 
    'IF', 'OTHERWISE', 'FI', 'WHILE', 'DO', 'SWITCH', 'CASE', 'BREAK', 'RETURN', 'CIN', 'COUT', 'AND', 'OR', 'EQUALS', 'NOTEQUAL', 'LESS', 'LESSEQUAL', 
    'GREAT', 'GREATEQUAL'
)

t_SUM = r'\+'
t_SUMDOUBLE = r'\+\+'
t_TIMES = r'\*'
t_POW = r'\^'
t_MINUS = r'\-'
t_MINUSDOUBLE = r'\-\-'
t_DIVISION = r'/'
t_MODULE = r'\%'
t_LESS = r'<'
t_LESSEQUAL = r'<='
t_EQUALS = r'=='
t_GREAT = r'>'
t_GREATEQUAL = r'>='
t_NOTEQUAL = r'!='
t_ASSIGN = r'='
t_PARRIGHT = r'\)'
t_PARLEFT = r'\('
t_SQRRIGHT = r'\]'
t_SQRLEFT = r'\['
t_KEYRIGHT = r'\}'
t_KEYLEFT = r'\{'
t_COMMA = r','
t_DOTCOMMA = r';'
t_DOUBLEDOT = r':'

def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

def t_MAIN(t):
    r'main'
    return t

def t_INTEGER(t):
    r'integer'
    return t

def t_DOUBLE(t):
    r'double'
    return t

def t_BOOLEAN(t):
    r'boolean'
    return t

def t_BOOL(t):
    r'true|false'
    return t

def t_IF(t):
    r'if'
    return t

def t_OTHERWISE(t):
    r'otherwise'
    return t

def t_FI(t):
    r'fi'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_DO(t):
    r'do'
    return t

def t_SWITCH(t):
    r'switch'
    return t

def t_CASE(t):
    r'case'
    return t

def t_BREAK(t):
    r'break'
    return t

def t_RETURN(t):
    r'return'
    return t

def t_CIN(t):
    r'cin'
    return t

def t_COUT(t):
    r'cout'
    return t

def t_AND(t):
    r'&&'
    return t

def t_OR(t):
    r'\|\|'
    return t

def t_IDENTIFIER(t):
    r'[a-zñA-ZÑ_][a-zñA-ZÑ0-9_]*'
    global tabla_simbolos_lineas
    if tabla_simbolos_lineas.existe_simbolo(t.value):
        tabla_simbolos_lineas.actualizar_lineas(t.value, t.lineno)
    else:
        tabla_simbolos_lineas.agregar_simbolo(t.value, None, None)
        tabla_simbolos_lineas.actualizar_lineas(t.value, t.lineno)
    return t

def t_REALNUMBER(t):
    r'\d+\.\d+'
    return t

def t_NUMBER(t):
    r'\d+'
    return t

def t_MULTIPLECOMMENT(t):
    r'\#\#(.|\n)*?\#\#'
    pass

def t_SINGLECOMMENT(t):
    r'\#[^\n]*'
    pass

def t_error(t):
    t.lexer.skip(1)

def p_program(p):
    '''program : main'''
    p[0] = Node('Program', children=[p[1]])

def p_main(p):
    '''main : MAIN KEYLEFT declarations KEYRIGHT'''
    p[0] = Node('Main', children=p[3].children)

def p_declarations(p):
    '''declarations : declarations declaration
                    | declaration'''
    if len(p) == 3:
        p[0] = Node('Declarations', children=list(p[1].children) + [p[2]])
    else:
        p[0] = Node('Declarations', children=[p[1]])

def p_declaration(p):
    '''declaration : declaration_variable
                   | statement'''
    p[0] = p[1]

def p_declaration_variable(p):
    '''declaration_variable : type variable DOTCOMMA'''
    p[0] = Node('VarDecl', children=[p[1], p[2]])

def p_variable(p):
    '''variable : variable COMMA IDENTIFIER
                | IDENTIFIER'''
    if len(p) == 4:
        p[0] = Node('Variables', children=list(p[1].children) + [Node(p[3])])
    else:
        p[0] = Node('Variables', children=[Node(p[1])])

def p_type(p):
    '''type : BOOLEAN
            | INTEGER
            | DOUBLE'''
    p[0] = Node(p[1], tipo = p[1])

def p_statements(p):
    '''statements : statements statement
                  | statement'''
    if len(p) == 3:
        p[0] = Node('Statements', children=list(p[1].children) + [p[2]])
    else:
        p[0] = Node('Statements', children=[p[1]])

def p_statement(p):
    '''statement : compound_statement
                 | assign_statement
                 | select_statement
                 | iteration_statement
                 | cin_statement
                 | cout_statement
                 | switch_statement
                 | doublefacts'''
    p[0] = p[1]

def p_compound_statement(p):
   '''compound_statement : KEYLEFT statements KEYRIGHT'''
   p[0] = Node('Block', children=p[2].children)

def p_assign_statement(p):
    '''assign_statement : IDENTIFIER ASSIGN expression DOTCOMMA'''
    p[0] = Node('Assign', children=[Node(p[1]), p[3]])

def p_select_statement(p):
    '''select_statement : IF PARLEFT expression PARRIGHT compound_statement
                        | IF PARLEFT expression PARRIGHT compound_statement OTHERWISE compound_statement'''
    if len(p) == 6:
        p[0] = Node('If', children=[p[3], p[5]])
    else:
        p[0] = Node('IfElse', children=[p[3], p[5], p[7]])

def p_iteration_statement(p):
    '''iteration_statement : WHILE PARLEFT expression PARRIGHT compound_statement
                           | DO compound_statement WHILE PARLEFT expression PARRIGHT DOTCOMMA'''
    if len(p) == 6:
        p[0] = Node('While', children=[p[3], p[5]])
    else:
        p[0] = Node('DoWhile', children=[p[2], p[5]])

def p_switch_statement(p):
    '''switch_statement : SWITCH PARLEFT expression PARRIGHT KEYLEFT case_list KEYRIGHT'''
    p[0] = Node('Switch', children=[p[3]] + list(p[6].children))

def p_case_list(p):
    '''case_list : case_list case_statement 
                 | case_statement'''
    if len(p) == 3:
        p[0] = Node('Cases', children=list(p[1].children) + [p[2]])
    else:
        p[0] = Node('Cases', children=[p[1]])

def p_case_statement(p):
    '''case_statement : CASE facts DOUBLEDOT statements BREAK DOTCOMMA'''
    p[0] = Node('Case', children=[p[2]] + list(p[4].children))

def p_cin_statement(p):
    '''cin_statement : CIN IDENTIFIER DOTCOMMA'''
    p[0] = Node('Cin', children=[Node(p[2])])

def p_cout_statement(p):
    '''cout_statement : COUT expression DOTCOMMA'''
    p[0] = Node('Cout', children=[p[2]])

def p_expression(p):
    '''expression : simple_expression relation_operator simple_expression
                  | simple_expression'''
    if len(p) == 4:
        p[0] = Node(p[2], children=[p[1], p[3]])
    else:
        p[0] = p[1]

def p_relation_operator(p):
    '''relation_operator : EQUALS
                         | NOTEQUAL
                         | LESS
                         | LESSEQUAL
                         | GREAT
                         | GREATEQUAL
                         | AND
                         | OR'''
    p[0] = p[1]

def p_simple_expression(p):
    '''simple_expression : simple_expression sum_operator term
                         | term'''
    if len(p) == 4:
        p[0] = Node(p[2], children=[p[1], p[3]])
    else:
        p[0] = p[1]

def p_sum_operator(p):
    '''sum_operator : SUM
                    | MINUS'''
    p[0] = str(p[1])

def p_term(p):
    '''term : term mult_operator factor 
            | factor'''
    if len(p) == 4:
        p[0] = Node(p[2], children=[p[1], p[3]])
    else:
        p[0] = p[1]

def p_mult_operator(p):
    '''mult_operator : TIMES
                     | DIVISION
                     | MODULE'''
    p[0] = str(p[1])

def p_factor(p):
    '''factor : factor pot_operator component
              | component'''
    if len(p) == 4:
        p[0] = Node(p[2], children=[p[1], p[3]])
    else:
        p[0] = p[1]

def p_pot_operator(p):
    '''pot_operator : POW'''
    p[0] = str(p[1])

def p_doublefacts(p):
    '''doublefacts : IDENTIFIER SUMDOUBLE DOTCOMMA
                   | IDENTIFIER MINUSDOUBLE DOTCOMMA'''
    if p[2] == '++':
        p[0] = Node('Assign', children=[Node(p[1]), Node('+', children=[Node(p[1]), Node('1')])])
    elif p[2] == '--':
        p[0] = Node('Assign', children=[Node(p[1]), Node('-', children=[Node(p[1]), Node('1')])])


def p_component(p):
    '''component : PARLEFT expression PARRIGHT
                 | IDENTIFIER
                 | facts
                 | doublefacts'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = Node(p[1])

def p_facts(p):
    '''facts : NUMBER
             | REALNUMBER
             | BOOL'''
    p[0] = str(p[1])

def p_empty(p):
    'empty : '
    p[0] = Node('empty')

errors = []
'''def save_errors_to_file(errors, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for error in errors:
            file.write(f"Line {error[0]}: {error[1]}\n")
'''
def p_error(p):
    global errors
    if p:
        error_msg = f'Unexpected token: {p.value}'
        line = p.lineno
        print("Syntax error at token", p.type, line)
         # Just discard the token and tell the parser it's okay.
        parser.errok()
    else:
        error_msg = 'Unexpected end of input'
        line = 'EOF'
        print("Syntax error at EOF")
    errors.append((line, error_msg)) 
    #save_errors_to_file(errors, "syntax_errors.txt")
   

lexer = lex.lex()
parser = yacc.yacc()

data = '''
main {
    integer x,y,z;
    y=2^3;
    #suma=45;
    x=32.32;
    x=23;
    y=2+3-1;
    double a,b,c,x;
    z=y+7;
    y=y+1;
    a=24.0+4-1/3*2+34-1;
    x=(5-3)*(8/2);
    y=5+3-2*4/7-9;
    z=8/2+15*4;
    y=14.54;
    y=a+b;
    if((4>2) || (40>50) ) {
        x=4+66;
        y=a+3;
    }
    otherwise {
        \n
        y=y+1;
    }
    x=3+4;
    do {
        y=(y+1)*2+1;
    } while(x>7);
    x=6+8/9*8/3;   
    cin x; 
    y++;
    mas=36/7; 
    double mas;
    mas=36/7; 
    while(y==5){
        while(y==0){
            cout mas;
            cin mas;
        }
    }
    
}
'''

result = parser.parse(data, lexer=lexer)



def register_error(varia, message):
    errorSem.append(f'{varia}: {message}')

def returnreslineas(text):
    lexer = lex.lex()
    parser = yacc.yacc()
    global tabla_simbolos_lineas
    tabla_simbolos_lineas = TablaDeSimbolos()

    parser.parse(text, lexer=lexer)

    tabla_simbolos_lineas.mostrar_tabla()

    return tabla_simbolos_lineas

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle('AST Viewer')
        self.setGeometry(100, 100, 800, 600)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setColumnCount(1)
        self.tree_widget.setHeaderLabels(['AST'])

        self.build_everything(result, None)

        returnreslineas(data)

        tabla_simbolos.mostrar_tabla()

        layout = QVBoxLayout()
        layout.addWidget(self.tree_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def build_everything(self, node, parent_item):
        if node is None:
            return
        self.give_annotations(node)
        self.give_types(node)
        self.update_lines()
        self.assign_values(node)
        self.build_tree(node, None)
        for error in errorSem:
            print(error)
    
    def give_annotations(self, node):
        if(node.name == 'VarDecl'):
            node.tipo = node.children[0].tipo
        elif (node.name == 'Variables'):
            node.tipo = node.parent.tipo
            #guardar en la tabla de simbolos
            for child in node.children:
                if(tabla_simbolos.existe_simbolo(child.name) == False):
                    child.tipo = node.tipo
                    tabla_simbolos.agregar_simbolo(child.name, child.tipo, 0)
                else:
                    if tabla_simbolos.obtener_simbolo(child.name).tipo != node.tipo:
                        child.valor = 'Error de Declaracion de Tipo'
                        register_error(child.name, child.valor)
                        
        elif(node.name not in compSymb) and (node.name not in artSymb) and (node.name not in stNames):
            if(tabla_simbolos.existe_simbolo(node.name) == True):
                node.tipo = tabla_simbolos.obtener_simbolo(node.name).tipo
        for child in node.children:
            self.give_annotations(child)

    def give_types(self, node):
        for child in node.children:
            self.give_types(child)
        try:
            numero = int(node.name)
            node.tipo = 'integer'
            node.valor = numero
        except ValueError:
            try:
                numero = float(node.name)
                node.tipo = 'double'
                node.valor = numero
            except ValueError:
                for child in node.children:
                    if child.tipo == 'Error':
                        node.tipo = 'Error'
                        node.valor = None
                        register_error(node.name, 'Error en nodo anterior')
                        return
                if node.name in compSymb:
                    node.tipo = 'boolean'
                elif node.name in artSymb:
                    for child in node.children:
                        if child.tipo == 'double':
                            node.tipo = 'double'
                            break
                        else:
                            node.tipo = 'integer'
                elif node.name == 'Assign':
                    node.tipo = node.children[0].tipo

    def update_lines(self):
        for nombre, simbolo in tabla_simbolos.tabla.items():
            if(tabla_simbolos_lineas.obtener_simbolo(nombre)):
                tabla_simbolos.obtener_simbolo(nombre).lineas = tabla_simbolos_lineas.obtener_simbolo(nombre).lineas

    def assign_values(self, node):
        for child in node.children:
            self.assign_values(child)
        
        for child in node.children:
            if child.tipo == 'Error':
                node.valor = 'Error'
                register_error(node.name, 'Error en nodo anterior')
        if node.valor != 'Error' and node.tipo != 'Error':
            if node.name in compSymb:
                operator_1 = 0
                if tabla_simbolos.existe_simbolo(node.children[0].name) == True:
                    node.children[0].valor = tabla_simbolos.obtener_simbolo(node.children[0].name).valor

                operator_1 = node.children[0].valor

                operator_2 = 0
                if tabla_simbolos.existe_simbolo(node.children[1].name) == True:
                    node.children[1].valor = tabla_simbolos.obtener_simbolo(node.children[1].name).valor
                operator_2 = node.children[1].valor

                if node.name == '<':
                    node.valor = operator_1 < operator_2
                if node.name == '<=':
                    node.valor = operator_1 <= operator_2
                if node.name == '==':
                    node.valor = operator_1 == operator_2
                if node.name == '>=':
                    node.valor = operator_1 >= operator_2
                if node.name == '>':
                    node.valor = operator_1 > operator_2
                if node.name == '!=':
                    node.valor = operator_1 != operator_2
                if node.name == '&&':
                    node.valor = operator_1 and operator_2
                if node.name == '||':
                    node.valor = operator_1 or operator_2

            elif node.name in artSymb:
                operator_1 = 0
                if tabla_simbolos.existe_simbolo(node.children[0].name) == True:
                    operator_1 = tabla_simbolos.obtener_simbolo(node.children[0].name).valor
                else:
                    operator_1 = node.children[0].valor

                operator_2 = 0
                if tabla_simbolos.existe_simbolo(node.children[1].name) == True:
                    operator_2 = tabla_simbolos.obtener_simbolo(node.children[1].name).valor
                else:
                    operator_2 = node.children[1].valor

                if node.name == '+':
                    node.valor = operator_1 + operator_2
                if node.name == '-':
                    node.valor = operator_1 - operator_2
                if node.name == '*':
                    node.valor = operator_1 * operator_2
                if node.name == '/':
                    node.valor = operator_1 / operator_2
                if node.name == '^':
                    node.valor = operator_1 ** operator_2
                if node.name == '%':
                    node.valor = operator_1 % operator_2

                if node.tipo == 'integer':
                    if node.parent.children[0].tipo == 'integer':
                        node.valor = round(node.valor)
                if node.tipo == 'double':
                    if node.parent.children[0].tipo == 'integer':
                        node.valor = round(node.valor)
            elif node.name == 'Assign':
                if tabla_simbolos.existe_simbolo(node.children[0].name) == True:
                    if(node.children[0].tipo == node.children[1].tipo):
                        tabla_simbolos.actualizar_valor(node.children[0].name, node.children[1].valor)
                        node.children[0].valor = node.children[1].valor
                    elif node.children[0].tipo == 'double':
                        node.children[0].valor = float(node.children[1].valor)
                        tabla_simbolos.actualizar_valor(node.children[0].name, node.children[1].valor)
                    else:
                        node.children[0].valor = 'Error de asignacion'
                        register_error(node.children[0].name, 'Error de asignacion')
                else: 
                    node.children[0].valor = 'Variable no declarada'
                    node.children[0].tipo = 'Error'
                    register_error(node.children[0].name, 'Variable no declarada')
            elif tabla_simbolos.existe_simbolo(node.name):
                node.valor = tabla_simbolos.obtener_simbolo(node.name).valor


    def build_tree(self, node, parent_item):
        if node is None:
            return
        print(node)
        item = QTreeWidgetItem([str(node.name)])
        if parent_item is None:
            self.tree_widget.addTopLevelItem(item)
        else:
            parent_item.addChild(item)
        for child in node.children:
            self.build_tree(child, item)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


def returnres(text):
    result = parser.parse(text, lexer=lexer)
    global errors
    errores = errors
    total = []
    total.append(errores)
    total.append(result)
    return total



