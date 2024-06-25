from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget
from anytree import Node, RenderTree
import ply.lex as lex
import ply.yacc as yacc

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

t_ignore = '\t\n'

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

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

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
        p[1].children = list(p[1].children) + [Node(p[3])]
        p[0] = p[1]
    else:
        p[0] = Node(p[1])

def p_type(p):
    '''type : BOOLEAN
            | INTEGER
            | DOUBLE'''
    p[0] = Node(p[1])

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
                 | switch_statement'''
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
    p[0] = Node(p[1])

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
    p[0] = Node(p[1])

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
    p[0] = Node(p[1])

def p_factor(p):
    '''factor : factor pot_operator component
              | component'''
    if len(p) == 4:
        p[0] = Node(p[2], children=[p[1], p[3]])
    else:
        p[0] = p[1]

def p_pot_operator(p):
    '''pot_operator : POW'''
    p[0] = Node(p[1])

def p_component(p):
    '''component : PARLEFT expression PARRIGHT
                 | IDENTIFIER
                 | facts'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = Node(p[1])

def p_facts(p):
    '''facts : NUMBER
             | REALNUMBER
             | BOOL'''
    p[0] = Node(str(p[1]))

def p_empty(p):
    'empty : '
    p[0] = Node('empty')

errors = []

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
   

lexer = lex.lex()
parser = yacc.yacc()

data = '''
main {
    integer x,y,z;
    double a,b,c;
    #suma=45;
    x=32.32;
    x=23;
    y=2+3-1;
    z=y+7;
    y=y+1;
    a=24.0+4-1/3*2+34-1;
    x=(5-3)*(8/2);
    y=5+3-2*4/7-9;
    z=8/2+15*4;
    y=14.54;;
    if(2>3) {
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

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle('AST Viewer')
        self.setGeometry(100, 100, 800, 600)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setColumnCount(1)
        self.tree_widget.setHeaderLabels(['AST'])

        self.build_tree(result, None)

        layout = QVBoxLayout()
        layout.addWidget(self.tree_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def build_tree(self, node, parent_item):
        if node is None:
            return
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
    result = parser.parse(data, lexer=lexer)
    return result