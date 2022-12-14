import sys
sys.path.insert(0, "..")

reserved = {
    "int": "INTDCL",
    "float": "FLOATDCL",
    "print": "PRINT",
    "boolean": "BOOLDCL",
    "true": "BOOLVAL",
    "false": "BOOLVAL",
    "while": "WHILE",
    "for": "FOR",
    "if": "IF",
    "else": "ELSE",
    "and": "AND",
    "or": "OR",
    ">": "GREATER",
    "<": "LESSER",
    "<=": "LESSEQUAL",
    ">=": "MOREEQUAL",
    "==": "EQUAL",
    "!=": "NOTEQUAL"
}


tokens = [
    'NAME', 'INUMBER', 'FNUMBER',
]
tokens.extend(reserved.values())

literals = ['=', '+', '-', '^', '/', '*', ';', '(', ')', '{', '}']
operators = ['=', '+', '-', '^', '/', '*']

# Tokens

def t_NAME(t):
    r'[a-zA-Z_]+[a-zA-Z0-9]*' #r'[a-eg-hj-oq-z]'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t



def t_FNUMBER(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules



class Node:
    
    # childrens = None
    # type = None

    def __init__(self):
        self.childrens = []
        self.type = ''
        self.val = ''

    def print(self, lvl = 0):
        r = (' ' * lvl) + self.type + ":" + str(self.val)
        print(r)
        #print(self.childrens)
        for c in self.childrens:
            c.print(lvl+1)
        

# dictionary of names
symbolsTable = {
    "table" : {},
    "parent" : None,
}
abstractTree = None


def p_prog(p):
    'prog : stmts'
    global abstractTree
    abstractTree = Node()
    abstractTree.type = 'root'
    abstractTree.childrens.extend(p[1])

def p_statements_recursion(p):
    '''stmts : statement stmts
             | statement '''
    stmt = p[1]
    if len(p) == 3:
        stmts = [ stmt ]
        stmts.extend(p[2])
        p[0] = stmts
    else: 
        p[0] = [ stmt ]
    
def p_dcl_declare_int(p):
    '''statement : INTDCL NAME ";" 
                 | INTDCL NAME "=" expression ";" '''
    if (len(p) == 4):
        symbolsTable["table"][p[2]] = { "type": "INT", "value":0}
        n = Node()
        n.type = "INT_DLC"
        n.val = p[2]
        p[0] = n
    else:
        symbolsTable["table"][p[2]] = { "type": "INT", "value": p[4] }
        n = Node()
        n.type = "INT_DLC"
        n.val = p[2]
        n2 = Node()
        n2.type = "ASIGN"
        n2.childrens.append(n)
        n2.childrens.append(p[4])
        p[0] = n2

def p_statement_declare_float(p):
    '''statement : FLOATDCL NAME ";"
                 | FLOATDCL NAME "=" expression ";" '''
   
    if (len(p) == 4):
        symbolsTable["table"][p[2]] = { "type": "FLOAT", "value":0 }
        n = Node()
        n.type = "FLOAT_DLC"
        n.val = p[2]
        p[0] = n
    else: 
        symbolsTable["table"][p[2]] = { "type": "FLOAT", "value": p[4] }
        n = Node()
        n.type = "FLOAT_DLC"
        n.val = p[2]
        n2 = Node()
        n2.type = "ASIGN"
        n2.childrens.append(n)
        n2.childrens.append(p[4])
        p[0] = n2
        

def p_statement_declare_bool(p):
    '''statement : BOOLDCL NAME ";"
                 | BOOLDCL NAME "=" boolexp ";" '''

    if (len(p) == 4):
        symbolsTable["table"][p[2]] = { "type": "BOOL", "value": False }
        n = Node()
        n.type = "BOOL_DLC"
        n.val = p[2]
        p[0] = n
    else:
        symbolsTable["table"][p[2]] = { "type": "BOOL", "value": p[4] }
        n = Node()
        n.type = "BOOL_DLC"
        n.val = p[2]
        n2 = Node()
        n2.type = "ASIGN"
        n2.childrens.append(n)
        n2.childrens.append(p[4])
        p[0] = n2

def p_statement_print(p):
    'statement : PRINT expression ";"'
    n = Node()
    n.type = 'PRINT'
    n.childrens.append(p[2])
    p[0] = n

def p_statement_while(p):
    '''statement : WHILE "(" boolexp ")" "{" stmts "}" '''
    n = Node()
    n.type = "WHILE"
    n.childrens.append(p[3])
    n.childrens.extend(p[6])
    p[0] = n

def p_statement_for(p):
    '''statement : FOR "(" statement boolexp ";" statement ")" "{" stmts "}" '''
    n = Node()
    n.type = "FOR"
    n.childrens.append(p[3])
    n.childrens.append(p[4])
    n.childrens.append(p[6])
    n.childrens.extend(p[9])
    p[0] = n

def p_statement_if(p):
    'statement : IF "(" boolexp ")" "{" stmts "}"'
    n = Node()
    n.type = 'IF'
    n2 = Node()
    n2.childrens = p[6]
    n.childrens.append(p[3])
    n.childrens.append(n2)
    p[0] = n

def p_statement_if_else(p):
    'statement : IF "(" boolexp ")" "{" stmts "}" ELSE "{" stmts "}"'
    n = Node()
    n.type = 'IF'
    n2 = Node()
    n2.childrens = p[6]
    n3 = Node()
    n3.type = 'ELSE'
    n3.childrens = p[10]
    n.childrens.append(p[3])
    n.childrens.append(n2)
    n.childrens.append(n3)
    p[0] = n



def p_statement_assign(p):
    'statement : NAME "=" expression ";"'
    if p[1] not in symbolsTable["table"]:
        print ( "You must declare a variable before using it")
    n = Node()
    n.type = 'ASIGN'
    ##n.childrens.append(p[1])
    if p[1] in symbolsTable["table"]:
        n1 = Node()
        n1.type = 'ID'
        n1.val = p[1]
        n.childrens.append(n1)
    else: 
        print("Error undeclared variable")


    n.childrens.append(p[3])
    p[0] = n

def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '^' expression
                  | expression '/' expression
                  | expression '*' expression'''

    if p[2] == '+':
        n = Node()
        n.type = '+'
        n.childrens.append(p[1])
        n.childrens.append(p[3])
        p[0] = n
    elif p[2] == '-':
        n = Node()
        n.type = '-'
        n.childrens.append(p[1])
        n.childrens.append(p[3])
        p[0] = n
    elif p[2] == '^':
        n = Node()
        n.type = '^'
        n.childrens.append(p[1])
        n.childrens.append(p[3])
        p[0] = n
    elif p[2] == '/':
        n = Node()
        n.type = '/'
        n.childrens.append(p[1])
        n.childrens.append(p[3])
        p[0] = n
    elif p[2] == '*':
        n = Node()
        n.type = '*'
        n.childrens.append(p[1])
        n.childrens.append(p[3])
        p[0] = n
    
def p_expression_boolop(p):
    '''boolexp : boolexp AND boolexp
               | boolexp OR boolexp'''

    if p[2] == 'and':
        n = Node()
        n.type = 'and'
        n.childrens.append(p[1])
        n.childrens.append(p[3])
        p[0] = n
    elif p[2] == 'or':
        n = Node()
        n.type = 'or'
        n.childrens.append(p[1])
        n.childrens.append(p[3])
        p[0] = n

def p_expression_inumber(p):
    "expression : INUMBER"
    n = Node()
    n.type = 'INUMBER'
    n.val = int(p[1])
    p[0] = n



def p_expression_fnumber(p):
    "expression : FNUMBER"
    n = Node()
    n.type = 'FNUMBER'
    n.val = float(p[1])
    p[0] = n

def p_expression_boolval(p):
    "expression : boolexp"
    p[0] = p[1]

def p_bool_expression(p):
    "boolexp : BOOLVAL"
    n = Node()
    n.type = 'BOOLVAL'
    n.val = (p[1] == 'true')
    p[0] = n


def p_expression_compare(p):
    '''boolexp : expression GREATER expression
                  | expression LESSER expression
                  | expression MOREEQUAL expression
                  | expression LESSEQUAL expression
                  | expression EQUAL expression
                  | expression NOTEQUAL expression'''

    if p[2] == '>':
        n = Node()
        n.type = '>'
        n.childrens.append(p[1])
        n.childrens.append(p[3])
        p[0] = n
    elif p[2] == '<':
        n = Node()
        n.type = '<'
        n.childrens.append(p[1])
        n.childrens.append(p[3])
        p[0] = n
    elif p[2] == '>=':
        n = Node()
        n.type = '>='
        n.childrens.append(p[1])
        n.childrens.append(p[3])
        p[0] = n
    elif p[2] == '<=':
        n = Node()
        n.type = '<='
        n.childrens.append(p[1])
        n.childrens.append(p[3])
        p[0] = n
    elif p[2] == '==':
        n = Node()
        n.type = '=='
        n.childrens.append(p[1])
        n.childrens.append(p[3])
        p[0] = n
    elif p[2] == '!=':
        n = Node()
        n.type = '!='
        n.childrens.append(p[1])
        n.childrens.append(p[3])
        p[0] = n

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
parser = yacc.yacc()


f = open("code.txt")
content = f.read()
yacc.parse(content)


abstractTree.print()
varCounter = 0
labelCounter = 0
def genTAC(node):
    global varCounter
    global labelCounter
    if ( node.type == "ASIGN" ):
        print(node.childrens[0].val  + " := " + genTAC(node.childrens[1]) )
    elif ( node.type == "INUMBER"):
        return str(node.val)
    elif ( node.type == "BOOLVAL"):
        return str(node.val)
    elif ( node.type == "FNUMBER"):
        return str(node.val)
    elif (node.type == "ID"):
        return str(node.val)
    elif ( node.type in operators):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter +1
        print( tempVar + " := " + genTAC(node.childrens[0]) + " + " + genTAC(node.childrens[1]))
        return tempVar
    elif ( node.type in ["and", "or"] ):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter +1
        print( tempVar + " := " + genTAC(node.childrens[0]) + " " + node.type + " " + genTAC(node.childrens[1]))
        return tempVar
    elif ( node.type in [">", "<", ">=", "<=", "==", "!="] ):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter +1
        print( tempVar + " := " + genTAC(node.childrens[0]) + " " + node.type + " " + genTAC(node.childrens[1]))
        return tempVar
    elif ( node.type == "WHILE" ):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter +1
        print ( tempVar + " := !" + genTAC(node.childrens[0]))
        label1 = "L" + str(labelCounter)
        label2 = "L" + str(labelCounter+1)
        labelCounter = labelCounter + 2
        print(label1 + ":")
        print("gotoLabelIf " + tempVar + " " + label2)
        genTAC(node.childrens[1])
        print("gotoLabelIf True "+ label1)
        print(label2 + ":")
    elif ( node.type == "FOR" ):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter +1
        genTAC(node.childrens[0])
        print ( tempVar + " := !" + genTAC(node.childrens[1]))
        label1 = "L" + str(labelCounter)
        label2 = "L" + str(labelCounter+1)
        labelCounter = labelCounter + 3
        print(label1 + ":")
        print("gotoLabelIf " + tempVar + " " + label2)
        genTAC(node.childrens[3])
        genTAC(node.childrens[2])
        print("gotoLabelIf True "+ label1)
        print(label2 + ":")
    elif ( node.type == "PRINT"):
        print( "PRINT " + genTAC(node.childrens[0]))
    elif ( node.type == "IF" ):
        tempVar = "t" + str(varCounter)
        varCounter = varCounter +1
        print ( tempVar + " := !" + str(node.childrens[0].val))
        tempLabel = "l" + str(labelCounter)
        labelCounter = labelCounter + 1
        print ( "gotoLabelIf " + tempVar + " " + tempLabel)
        genTAC(node.childrens[1])
        print ( tempLabel)
    else:
        for child in node.childrens:
            genTAC(child)
    

print ("\ntac:\n")
genTAC(abstractTree)


#Some examples
# for ( i = 0; i < 3; i++){
#     stamentes
# }
# i := 0
# t1 = i < 3
# t0 = !t1
# gotoLabelif t0 Label1

# staments
# i = i + 1
# Label1



# while ( condicion ) {
#     staments
# }
# WHILE
# t1 = condicion
# t0 = !t1
# gotoLabelif t0 Label1

# staments

# Label1
