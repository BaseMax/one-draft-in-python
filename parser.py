import scanner
import ply.yacc as yacc

tokens=scanner.tokens
start='program'
# program=None

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('left','POWER'),
    ('right','UMINUS')
)

def p_program(p):
    '''
    program : module includes global_statements
    '''
    if p[1] == None:
        p[1]="main"
    p[0]={'module':p[1],'includes':p[2],'statements':p[3],}
    # program=p[0]

def p_global_statements(p):
    '''
    global_statements : global_statements global_statement
                      | global_statement
                      |
    '''
    if p[0]==None:
        p[0]=[]
    if len(p) == 3:
        p[1].append(p[2])
        p[0]=p[1]
    elif len(p) == 2:
        p[0].append(p[1])
    else:
        p[0]=[]

def p_global_statement(p):
    '''
    global_statement : function
                     | const_variable
    '''
    p[0]=p[1]

def p_const_variable(p):
    '''
    const_variable : CONST ID EQUALS expr
    '''
    p[0]={'type':'define','prefix':'const','name':p[2],'value':p[4]}

def module(p):
    '''
    module : MODULE ID
           |
    '''
    if len(p) == 3:
        p[0]=p[2]
    else:
        p[0]=None

def p_includes(p):
    '''
    includes : includes include
            | include
            |
    '''
    if p[0]==None:
        p[0]=[]
    if len(p) == 3:
        p[1].append(p[2])
        p[0]=p[1]
    elif len(p) == 2:
        p[0].append(p[1])
    else:
        p[0]=[]

def p_include(p):
    '''
    include : include ids
    '''
    p[0]=p[2]

def p_ids(p):
    '''
    ids : ids COMMA package_name
        | package_name
    '''
    if p[0]==None:
        p[0]=[]
    if len(p) == 4:
        p[1].append(p[3])
        p[0]=p[1]
    elif len(p) == 2:
        p[0].append(p[1])

def p_package_name(p):
    '''
    package_name : package_name PERIOD ID
                 | ID
    '''
    if p[0]==None:
        p[0]=[]
    if len(p) == 4:
        p[1].append(p[3])
        p[0]=p[1]
    elif len(p) == 2:
        p[0].append(p[1])

def p_function(p):
    '''
    function : ID LPAREN arguments RPAREN statements_block
    '''
    p[0]={
        'type':'function_define',
        'name':p[1],
        'arguments':p[3],
        'body':p[5],
    }

def p_arguments(p):
    '''
    arguments : arguments COMMA argument
              | argument
              |
    '''
    if p[0]==None:
        p[0]=[]
    if len(p) == 4:
        p[1].append(p[3])
        p[0]=p[1]
    elif len(p) == 2:
        p[0].append(p[1])


def p_prefix_datatype(p):
    '''
    prefix_datatype : MUT
    '''
    p[0]=p[1]

def p_datatype(p):
    '''
    datatype : package_name
             | LBRACKET RBRACKET datatype
    '''
    if len(p) == 2:
        p[0]={"type":"type","value":p[1]}
    elif len(p) == 4:
        p[0]={"type":"array","value":p[3],}

def p_datatype_map(p):
    '''
    datatype : MAP LBRACKET datatype RBRACKET datatype
    '''
    p[0]={"type":"map","index":p[3],"value":p[5],}

def p_argument(p):
    '''
    argument : datatype package_name
    '''
    p[0]={'type':p[1],'name':p[2],}

def p_statements_block_may(p):
    '''
    statements_block_may : statements_block
                         | statement
    '''
    if len(p) == 1:
        p[0]=[]
    else:
        p[0]=p[1]

def p_statements_block(p):
    '''
    statements_block : LBRACE statements RBRACE
                     | LBRACE RBRACE
    '''
    if len(p) == 3:
        p[0]=[]
    else:
        p[0]=p[2]

def p_statements(p):
    '''
    statements : statements statement
               | statement
    '''
    if p[0]==None:
        p[0]=[]
    if len(p) == 3:
        p[1].append(p[2])
        p[0]=p[1]
    elif len(p) == 2:
        p[0].append(p[1])

def p_statement(p):
    '''
    statement : statement_if
              | statement_define
              | statement_while
              | statement_for
              | statement_for_each
              | statement_match
              | statement_expr
    '''
    p[0]=p[1]

def p_statement_define(p):
    '''
    statement_define : prefix_datatype ID datatype EQUALS expr
                     | ID datatype EQUALS expr
    '''
    if len(p) == 6:
        p[0]={'type':'define','prefix':p[1],'data':p[3],'name':p[2],'value':p[5],}
    else:
        p[0]={'type':'define','prefix':None,'data':p[2],'name':p[1],'value':p[4],}

def p_statement_if(p):
    '''
    statement_if : IF expr statements_block
    '''
    p[0]={'name':'if','clause':p[2],'body':p[3],}

def p_statement_while(p):
    '''
    statement_while : WHILE expr statements_block
    '''
    p[0]={'name':'while','clause':p[2],'body':p[3],}

def p_statement_for(p):
    '''
    statement_for : FOR
    '''
    p[0]={'name':'for',}

def p_statement_for_each(p):
    '''
    statement_for_each : FOR ID
    '''
    p[0]={'name':'foreach',}

def p_statement_match(p):
    '''
    statement_match : MATCH
    '''
    p[0]={'name':'match',}

def p_statement_expr(p):
    '''
    statement_expr : expr
    '''
    p[0]={'name':'expression','value':p[1],}

def p_expr_binary(p):
    '''
    expr : expr PLUS expr
         | expr MINUS expr
         | expr TIMES expr
         | expr DIVIDE expr
         | expr POWER expr
         | relexpr
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {'type':'operator','left':p[1],'op':p[2],'right':p[3],}

def p_expr_number(p):
    '''
    expr : INTEGER
         | FLOAT
    '''
    p[0] = {'type':'number','value':p[1],}

def p_expr_bool(p):
    '''
    expr : TRUE
         | FALSE
    '''
    p[0] = {'type':'bool','value':p[1],}


def p_expr_variable(p):
    '''
    expr : variable
    '''
    p[0] = p[1]

def p_expr_group(p):
    '''
    expr : LPAREN expr RPAREN
    '''
    p[0] = {'type':'group','value':p[2],}


def p_expr_unary(p):
    '''
    expr : MINUS expr %prec UMINUS
    '''
    p[0] = {'type':'unary','value':p[2],}

# Relational expressions
def p_relexpr(p):
    '''
    relexpr : expr LT expr
            | expr LE expr
            | expr GT expr
            | expr GE expr
            | expr EQUALS EQUALS expr
            | expr NE expr
    '''
    if len(p) == 5:
        p[0] = {'type':'relation','left': p[1],'op':'==','right':p[4],}
    else:
        p[0] = {'type':'relation','left': p[1],'op':p[2],'right':p[3],}

# Variables
def p_variable(p):
    '''
    variable : ID
    '''
    p[0] = {'type':'id','value': p[1],}

def p_variable_other(p):
    '''
    variable : function_call
    '''
    p[0] = p[1]

def p_variable_object(p):
    '''
    variable : variable PERIOD variable
    '''
    p[0] = {'type':'object','parent':p[1],'value': p[3],}

def p_function_call(p):
    '''
    function_call : ID LPAREN function_arguments RPAREN
    '''
    p[0] = {'type':'call','name': p[1],'arguments':p[3],}

def p_function_arguments(p):
    '''
    function_arguments : function_arguments COMMA function_argument
                       | function_argument
                       |
    '''
    if p[0]==None:
        p[0]=[]
    if len(p) == 4:
        p[1].append(p[3])
        p[0]=p[1]
    elif len(p) == 2:
        p[0].append(p[1])

def p_function_argument(p):
    '''
    function_argument : expr
    '''
    p[0]={'type':'value','value':p[1],}


def p_error(p):
    print('Parser error \'%s\'' % p.value)

