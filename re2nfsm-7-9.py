# Libraries
##################################################
import ply.yacc as yacc
import ply.lex as lex


# Tokens:
##################################################
# single characters  #  a       
# regexp1 regexp2    #  ab
# regexp *           #  a*
# regexp1 | regexp2  #  a|b
# ( regexp )         #  (a|b)* -- same as (?:a|b) 

# My Lexer
##################################################
tokens = ( 
    'ANCHAR',    # Alphanumeric character (a-z, A-Z, 0-9)
    'STAR',     # * (Asterix)
    'PIPE',     # |
    'LPAREN',   # (
    'RPAREN',   # )
#    'REGEXP',   # Regular Expression String
)

t_STAR = r'\*'
t_PIPE = r'\|'
t_LPAREN = r'\('
t_RPAREN = r'\)'

#def t_REGEXP(t):
#    r'[a-zA-Z0-9*|()]+'
#    return t

def t_ANCHAR(t):
    r'[a-zA-Z0-9]'
    return t

t_ignore = '\t\v\r'

def t_newline(t):
    r'\n'
    t.relexer.lineno += 1

def t_error(t):
    print "Regexp Lexer:  Illegal character " + t.value[0]
    t.relexer.skip(1)


def myrelexer(input_string):
    relexer.input(input_string)
    result = [ ] 
    while True:
        tok = relexer.token()
        if not tok:
            break
        result = result + [(tok.type, tok.value)]
    return result
##################################################
# End of my Lexer
##################################################


# My Parser
##################################################

# Grammar:
##################################################
# RESTR = Regular Expression String
# E = Regexp Element
# ANC = AlphaNumeric Character (A-Z, a-z, 0-9)
# SCP = Single ANC or Parenthesis
##################################################
# RESTR --> E RESTR
# RESTR --> 
# E --> E*
# E --> (E)
# E --> E|E
# E --> ANC E
# E --> ANC
##################################################
# Bugs:
# Can't handle: '((a)(b))'
##################################################

# Parse tree (AST)
##################################################
# ('CharZeroPlus',char)
# ('CharDisjuncChar',charset)
# ('ParenSet',charset)
# ('ANChar',char)

start = 'R'  # Starting symbol in our grammar

def p_R(p):
    'R : E R'
    p[0] = [p[1]] + p[2]

def p_R_empty(p):
    'R : '
    p[0] = []

def p_ESTAR(p):
    'E : E STAR'
    p[0] = ('CharZeroPlus',[p[1]])

def p_EPAREN(p):
    'E : LPAREN E RPAREN'
    p[0] = ('ParenSet',[p[2]])

def p_EPIPE(p):
    'E : E PIPE E'
    p[0] = ('CharDisjuncChar',[p[1],p[3]])

def p_EANE(p):
    'E : ANCHAR E'
    #p[0] = p[1],[p[2]]
    #p[0] = ['ANChar',p[1]] + [p[2]]
    #p[0] = ('ANChar',p[1]) + p[2]  # ('ANChar','a','ANChar','b',...)
    #p[0] = ('ANChar',p[1]) + (p[2])  # Same as above
    #p[0] = ('ANChar',p[1]) + [p[2]]  # Error, can't concat tuple + list
    #p[0] = ('ANChar',p[1]),[p[2]]  # [(('ANChar', 'a'), [(('ANChar', 'b'),...
    p[0] = ('ANChar',p[1],[p[2]])

def p_EAN(p):
    'E : ANCHAR'
    #p[0] = [p[1]]
    p[0] = ('ANChar',p[1])

#def p_SCPESCPPAREN(p):
#    'SCP : LPAREN E SCP RPAREN'
#    p[0] = ('ParenSet',[p[2],p[3]])

#def p_SCPEPAREN(p):
#    'SCP : LPAREN E RPAREN'
#    p[0] = ('ParenSet',[p[2]])

#def p_SCAlphaNum(p):
#    'SCP : ANCHAR'
#    p[0] = ('ANChar',p[1])

def p_error(p):
    print "Syntax error in input!"

def myreparser(input_string):
    relexer.input(input_string) 
    parse_tree = reparser.parse(input_string)
    return parse_tree
##################################################
# End of my Parser
##################################################
    

# My Interpreter
##################################################

# Parse tree (AST)
##################################################
# ('CharZeroPlus',char)
# ('CharDisjuncChar',charset)
# ('ParenSet',charset)
# ('ANChar',char)

def reinterpret(ast,startnode=None,nextnodes=None,edges=None):
    if startnode == None:
        startnode = [1]
    if nextnodes == None:
        nextnodes = [1]
    if edges == None:
        edges = {}
    print "\nEntered reinterpret, ast:\n" + str(ast)
    if isinstance(ast,tuple):
        ast = [ast]
        print "\nModified ast:\n" + str(ast)
    for node in ast:
        nodetype = node[0]
        payload = node[1]
        if len(node) >= 3:
            recurse = True
            nextpayload = node[2]
        else:
            recurse = False
        print str(nodetype) + ':  ' + str(payload)
        if nodetype == 'CharZeroPlus':
            if payload[0][0] == 'ANChar':
            #    if len(nextnodes) == 1:
            #        #edges[(nextnodes[0],payload[0][1])] = [nextnodes[0],nextnodes[0]+1]
                    edges[(nextnodes[0],payload[0][1])] = [nextnodes[0]]
                    edges[(nextnodes[0],None)] = [nextnodes[0] + 1]
                    nextnodes[0] += 1
                # Assuming we're reconverging nextnodes back to one nextnode
            #    else:
            #        for nextnode in nextnodes:
            #            edges[(nextnode,payload[0][1])] = [nextnode,nextnode+1]
            #            edges[(nextnode,None)] = [nextnode + 1]
            #            nextnodes[0] += 1
            else:
                # Save start
                charzeroplusstart = nextnodes[0]
                reinterpret(payload,startnode,nextnodes,edges)
                # Link end back to beginning since (x)* and transition forward
                edges[(nextnodes[0],None)] = [charzeroplusstart,nextnodes[0]+1]
                # Allow skipping sequence (zero or more...)
                edges[(charzeroplusstart,None)] = [nextnodes[0] + 1]
                nextnodes[0] += 1
        elif nodetype == 'CharDisjuncChar':
            # payload = [[x]|[y]], split up left half and right half:
            payload1 = payload[0]
            payload2 = payload[1]
            # Save starting pointer:
            chardisjuncstart = nextnodes[0]
            reinterpret(payload1,startnode,nextnodes,edges)
            # Save nextnodes pointer:
            chardisjuncend1 = nextnodes[0]
            # Add saved starting pointer to nextnodes for edge insertion
            nextnodes.append(chardisjuncstart)
            reinterpret(payload2,startnode,nextnodes,edges)
            # Save nextnodes pointer:
            chardisjuncend2 = nextnodes[0]
            # Use epsilon transition to re-integrate two branches from above
            edges[(chardisjuncend1,None)] = [nextnodes[0] + 1]
            edges[(chardisjuncend2,None)] = [nextnodes[0] + 1]
            nextnodes[0] += 1
            #if payload[0][0] == 'ANChar':
            #    edges[(nextnodes[0],payload[0][1])] = [nextnodes[0] + 1]
            #    edges[(nextnodes[0],payload[1][1])] = [nextnodes[0] + 2]
            #    nextnodes[0] += 1
            #    nextnodes.append(nextnodes[0]+2)
            #else:
            #    reinterpret(payload,startnode,nextnodes,edges)
        elif nodetype == 'ParenSet':
            # Cases:
            #   (x+)
            #   (x+)*
            #   (x+|y+)
            #   (x+|y+)*
            #   ((x+))...
            #if payload[0][0] == 'ANChar':
            #
            # Mark start of parenset:
            parensetstart = nextnodes[:]
            #
            reinterpret(payload,startnode,nextnodes,edges)
            #
            # End of parenset
            #while payload[0][0] == 'ANChar':
            #    edges[(nextnodes[0],payload[0][1])] = [nextnodes[0] + 1]
            #    nextnodes[0] += 1
            #    del payload[0]
            #    if not payload:
            #        break
            #else:
            #    reinterpret(payload,startnode,nextnodes,edges)
        elif nodetype == 'ANChar':
            #ancelts = iter(node)
            #print 'node:  ' + str(node)
            #for anode,achar in zip(ancelts,ancelts):
                #print 'anode,achar = ' + str(anode) + ', ' + str(achar)
                #if anode != 'ANChar':
                    #raise NameError('Undefined verb:  ' + e[1])
                    # Note:  Only valid for Python 2.x
                    #raise ValueError, "Error - expecting 'ANChar', found value:  " + str(anode)
                #else:
                    #edges[(nextnodes[0],achar)] = [nextnodes[0] + 1]
                    # nextnodes = [#] - standard behavior
                    if len(nextnodes) == 1:
                        edges[(nextnodes[0],payload)] = [nextnodes[0] + 1]
                        nextnodes[0] += 1
                    # nextnodes = [#1,#2] - start at #2 then advance to #1
                    # This support disjunction case
                    else:
                        edges[(nextnodes[1],payload)] = [nextnodes[0] + 1]
                        # After using nextnodes[1], remove it
                        nextnodes.pop()
                        nextnodes[0] += 1
                    if recurse:
                        reinterpret(nextpayload,startnode,nextnodes,edges)
        else:
            #raise NameError('Undefined verb:  ' + e[1])
            # Note:  Only valid for Python 2.x
            raise ValueError, "Error - unexpected value:  " + str(node[0])
    return (edges,startnode,nextnodes)

##################################################
# End of my Interpreter
##################################################

def printedges(edges,start,end):
    for edge in sorted(edges):
        if list(set(edges[edge]).intersection(end)):
            print str(edge) + ':  ' + str(edges[edge]) + '\t<<END>>'
        else:
            print str(edge) + ':  ' + str(edges[edge])


# Global
##################################################
relexer = lex.lex()
reparser = yacc.yacc() 


