from anytree import Node, RenderTree

tokens = (
    'MAIN', 'INTEGER', 'DOUBLE', 'BOOLEAN', 'IDENTIFIER', 'NUMBER', 'REALNUMBER', 'BOOL', 'SUMDOUBLE', 'MINUSDOUBLE', 'SUM', 'MINUS', 'TIMES', 'DIVISION', 'MODULE', 'POW',
    'ASSIGN', 'PARLEFT','PARRIGHT', 'SQRLEFT', 'SQRRIGHT', 'KEYLEFT', 'KEYRIGHT', 'COMMA', 'DOTCOMMA', 'DOUBLEDOT', 'SINGLECOMMENT', 'MULTIPLECOMMENT', 
    'IF', 'OTHERWISE', 'FI', 'WHILE', 'DO', 'SWITCH', 'CASE', 'BREAK', 'RETURN', 'CIN', 'COUT', 'AND', 'OR', 'EQUALS', 'NOTEQUAL', 'LESS', 'LESSEQUAL', 
    'GREAT', 'GREATEQUAL'
)

# Regular expression patterns for tokens
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

# Ignore whitespace
t_ignore = '\t\n'

# Tabla de simbolos
symbol_table = {}

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
  
# Define a rule for handling errors
def t_error(t):
  t.lexer.skip(1)

# Definición de las clases para representar los nodos del AST

def p_program(p):
    '''program : main'''
    p[0] = Node('program', children=[p[1]])

def p_main(p):
    '''main : MAIN KEYLEFT declarations KEYRIGHT'''
    p[0] = Node('main', children=[p[3]])

def p_declarations(p):
    '''declarations : declarations declaration
                    | declaration'''
    if len(p) == 3:
        p[0] = Node('declarations', children=[p[1], p[2]])
    else:
        p[0] = Node('declarations', children=[p[1]])

def p_declaration(p):
    '''declaration : declaration_variable
                   | list_statements'''
    p[0] = Node('declaration', children=[p[1]])

def p_declaration_variable(p):
    '''declaration_variable : type variable DOTCOMMA'''
    p[0] = Node('declaration_variable', children=[p[1], p[2]])

def p_variable(p):
    '''variable : variable COMMA IDENTIFIER
                | IDENTIFIER'''
    if len(p) == 4:
        p[0] = Node('variable', children=[p[1], Node(p[3], parent=p[1])])
    else:
        p[0] = Node('variable', children=[Node(p[1])])

def p_type(p):
    '''type : BOOLEAN
            | INTEGER
            | DOUBLE'''
    p[0] = Node('type', children=[Node(p[1])])

def p_list_statements(p):
    '''list_statements : list_statements statement 
                       | empty'''
    if len(p) == 3:
        p[0] = Node('list_statements', children=[p[1], p[2]])
    else:
        p[0] = Node('list_statements')

def p_statement(p):
    '''statement : select_statement
                 | iteration_statement
                 | compound_statement
                 | cin_statement
                 | cout_statement
                 | assign_statement
                 | switch_statement'''
    p[0] = Node('statement', children=[p[1]])

def p_compound_statement(p):
   '''compound_statement : KEYLEFT list_statements KEYRIGHT'''
   p[0] = Node('compound_statement', children=[p[2]])

def p_assign_statement(p):
    '''assign_statement : IDENTIFIER ASSIGN sent_expression'''
    p[0] = Node('assign_statement', children=[Node(p[1]), p[3]])

def p_sent_expression(p):
    '''sent_expression : expression DOTCOMMA
                       | DOTCOMMA'''
    if len(p) == 3:
        p[0] = Node('sent_expression', children=[p[1]])
    else:
        p[0] = Node('sent_expression')

def p_select_statement(p):
    '''select_statement : IF PARLEFT expression PARRIGHT KEYLEFT list_statements KEYRIGHT
                        | IF PARLEFT expression PARRIGHT KEYLEFT list_statements KEYRIGHT OTHERWISE KEYLEFT list_statements KEYRIGHT'''
    if len(p) == 9:
        p[0] = Node('select_statement', children=[p[3], p[6]])
    else:
        p[0] = Node('select_statement', children=[p[3], p[6], p[10]])

def p_iteration_statement(p):
    '''iteration_statement : WHILE PARLEFT expression PARRIGHT KEYLEFT list_statements KEYRIGHT
                           | DO KEYLEFT list_statements KEYRIGHT WHILE PARLEFT expression PARRIGHT'''
    if len(p) == 8:
        p[0] = Node('iteration_statement', children=[p[3], p[6]])
    else:
        p[0] = Node('iteration_statement', children=[p[6], p[8]])

def p_switch_statement(p):
    '''switch_statement : SWITCH PARLEFT expression PARRIGHT KEYLEFT case_list KEYRIGHT'''
    p[0] = Node('switch_statement', children=[p[3], p[6]])

def p_case_list(p):
    '''case_list : case_list case_statement 
                 | case_statement'''
    if len(p) == 3:
        p[0] = Node('case_list', children=[p[1], p[2]])
    else:
        p[0] = Node('case_list', children=[p[1]])

def p_case_statement(p):
    '''case_statement : CASE facts DOUBLEDOT list_statements BREAK DOTCOMMA'''
    p[0] = Node('case_statement', children=[p[2], p[4]])

def p_cin_statement(p):
    '''cin_statement : CIN IDENTIFIER DOTCOMMA'''
    p[0] = Node('cin_statement', children=[Node(p[2])])

def p_cout_statement(p):
    '''cout_statement : COUT expression DOTCOMMA'''
    p[0] = Node('cout_statement', children=[p[2]])

def p_expression(p):
    '''expression : simple_expression relation_operator simple_expression 
                  | simple_expression'''
    if len(p) == 4:
        p[0] = Node('expression', children=[p[1], p[2], p[3]])
    else:
        p[0] = Node('expression', children=[p[1]])

def p_relation_operator(p):
    '''relation_operator : EQUALS
                         | NOTEQUAL
                         | LESS
                         | LESSEQUAL
                         | GREAT
                         | GREATEQUAL
                         | AND
                         | OR'''
    p[0] = Node('relation_operator', children=[Node(p[1])])

def p_simple_expression(p):
    '''simple_expression : simple_expression sum_operator term
                         | term'''
    if len(p) == 4:
        p[0] = Node('simple_expression', children=[p[1], p[2], p[3]])
    else:
        p[0] = Node('simple_expression', children=[p[1]])

def p_sum_operator(p):
    '''sum_operator : SUM
                    | MINUS'''
    p[0] = Node('sum_operator', children=[Node(p[1])])

def p_term(p):
    '''term : term mult_operator factor 
            | factor'''
    if len(p) == 4:
        p[0] = Node('term', children=[p[1], p[2], p[3]])
    else:
        p[0] = Node('term', children=[p[1]])

def p_mult_operator(p):
    '''mult_operator : TIMES
                     | DIVISION
                     | MODULE'''
    p[0] = Node('mult_operator', children=[Node(p[1])])

def p_factor(p):
    '''factor : factor pot_operator double_fact
              | double_fact'''
    if len(p) == 4:
        p[0] = Node('factor', children=[p[1], p[2], p[3]])
    else:
        p[0] = Node('factor', children=[p[1]])

def p_double_fact(p):
    '''double_fact : component double_op
                   | component'''
    if len(p) == 3:
        p[0] = Node('double_fact', children=[p[1], p[2]])
    else:
        p[0] = Node('double_fact', children=[p[1]])

def p_pot_operator(p):
    '''pot_operator : POW'''
    p[0] = Node('pot_operator', children=[Node(p[1])])

def p_double_op(p):
    '''double_op : SUMDOUBLE
                 | MINUSDOUBLE'''
    p[0] = Node('double_op', children=[Node(p[1])])

def p_component(p):
    '''component : PARLEFT expression PARRIGHT
                 | IDENTIFIER
                 | facts'''
    if len(p) == 4:
        p[0] = Node('component', children=[p[2]])
    else:
        p[0] = Node('component', children=[Node(p[1])])

def p_facts(p):
    '''facts : NUMBER
             | REALNUMBER
             | BOOL'''
    p[0] = str(p[1])  # Directly assign the value to the node


def p_empty(p):
    'empty : '
    p[0] = Node('empty')

# Error rule for syntax errors
def p_error(p):
    global errors
    if p:
        error_msg = f'Unexpected token: {p.value}'
        line = p.lineno
    else:
        error_msg = 'Unexpected end of input'
        line = 'EOF'
    errors.append((line, error_msg))

import ply.lex as lex
import ply.yacc as yacc

# Sample input to parse
data = '''
main {
    integer x;
    double y;
    if (x < 10) {
        y = 3.14;
    } otherwise {
        y = 2.71;
    }
}
'''

# Initialize lexer and parser
lexer = lex.lex()
parser = yacc.yacc()

# Parse the data
result = parser.parse(data, lexer=lexer)

# Render the tree
for pre, fill, node in RenderTree(result):
    print("%s%s" % (pre, node.name))