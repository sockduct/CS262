import ply.lex as lex
import ply.yacc as yacc

tokens = ('BAR','STAR','LPAREN','RPAREN','LETTER')  # Our tokens

# What the tokens look like, escaped for safety
t_BAR   = r'\|'
t_STAR  = r'\*'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Token rules
def t_LETTER(t):
    r'[A-Za-z0-9]'
    return t

t_ignore = ' \t\v\r'

def t_error(t):
    print "Lexer: unexpected character " + t.value[0]
    t.lexer.skip(1)

# precedence ordering
start = 're'
precedence = (
    ('left','BAR'),
    ('left','CONCAT'),
    ('left','STAR'),
)

def p_re_letter(p):
    're : LETTER %prec CONCAT'
    p[0] = ('letter',p[1])

def p_re_concat(p):
    're : re re %prec CONCAT'
    p[0] = ('concat',p[1],p[2])

def p_re_bar(p):
    're : re BAR re'
    p[0] = ('bar',p[1],p[3])

def p_re_star(p):
    're : re STAR'
    p[0] = ('star',p[1])

def p_re_paren(p):
    're : LPAREN re RPAREN'
    p[0] = p[2]

def p_error(p):
    raise SyntaxError

def interpret(ast):  # goal here is to create a nfsm out of an ast
    global state_counter
    start_state = 1
    accepting = [2]
    state_counter = 3
    edges = {}
    def add_edge(a,b,l):  # helper function to add edges
        if (a,l) in edges:
            edges[(a,l)] = [b] + edges[(a,l)]
        else:
            edges[(a,l)] = [b]
    def new_state():  # helper function to add a new state
        global state_counter
        x = state_counter
        state_counter = state_counter + 1
        return x
    def walk(re,here,goal):  # helper function to walk the ast
        retype = re[0]
        if retype == 'letter':  # see a plain letter, that's a transition we have to take
            add_edge(here,goal,re[1])
        elif retype == 'concat':  # see concat then we have to take both, in order
            mid = new_state()
            walk(re[1],here,mid)
            walk(re[2],mid,goal)
        elif retype == 'bar':  # a bar means we go from the current state to two different
            walk(re[1],here,goal)
            walk(re[2],here,goal)
        elif retype == 'star':  # and a star will have a loop back to the current state
            walk(re[1],here,here)
            add_edge(here,goal,None)
        else:
            print 'OOPS' + re
    walk(ast,start_state,accepting[0])
    return (edges,accepting,start_state)

lexer = lex.lex() 
parser = yacc.yacc() 

def re_to_nfsm(re_string): 
        # Feel free to overwrite this with your own code. 
        lexer.input(re_string)
        parse_tree = parser.parse(re_string, lexer=lexer) 
        return interpret(parse_tree) 

