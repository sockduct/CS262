def unwind(stmt):
    # stmt:
    # 'assign' <var> (=) exp(s)
    # exp(s):
    #   binop (exp,op,exp)
    #   number <#>
    #   identifier <var>
    if stmt[0] == 'assign':
        return stmt[1], unwind(stmt[2])
    elif stmt[0] == 'binop':
        return unwind(stmt[1]),unwind(stmt[3])
    elif stmt[0] == 'number':
        return ()
    elif stmt[0] == 'identifier':
        return stmt[1]
    else:
        # Note:  Only valid for Python 2.x
        raise ValueError, "Error - unexpected value:  " + str(stmt[0])

def purge(seenexps,new):
    retflag = False
    while True:
        retflag = True
        for key in seenexps:
            if new in seenexps[key]:
                retflag = False
                del seenexps[key]
                break
        if retflag:
            return

def duplicate(seenexps,lhs,rhs):
    for key in seenexps:
        if rhs == seenexps[key] and key != lhs:
            return key
    return None

def optimize(ast):
    seenexps = {}
    # Enumerating this way doesn't work because can't change contents
    #for line in ast:
    for linenum in range(len(ast)):
        #print "\nEvaluating:  " + str(ast[linenum])
        #lhs,rhs = unwind(line)
        lhs,rhs = unwind(ast[linenum])
        #print "lhs,rhs = " + str(lhs) + ', ' + str(rhs)
        seenexps[lhs] = rhs
        #print "seenexps now = " + str(seenexps)
        purge(seenexps,lhs)
        #print "After purge, seenexps now = " + str(seenexps)
        newrhs = duplicate(seenexps,lhs,rhs)
        #print "After duplicate, newrhs = " + str(newrhs)
        if newrhs != None:
            #print "newrhs not none, updating line in ast..."
            #line[2] = ('identifier',newrhs)
            #ast[linenum][2] = ('identifier',newrhs)
            ast[linenum] = (ast[linenum][0],ast[linenum][1],('identifier',newrhs))
            #print "ast now = " + str(ast)
    #print '\n'
    return ast

