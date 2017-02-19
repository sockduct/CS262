# grammar - List, list of rules
# upath - Dictionary, utterance paths through grammar rules
#           Key = path, result = value
def expand(grammar,upath=None):
    if upath == None:
        upath = {}
    print "Entered expand"
    for i in range(len(grammar)):
        print "\nIterating through lhs, currently - rule #" + str(i) + " - " + \
            str(grammar[i])
        upath['currentrule'] = i
        upath['currentresult'] = []
        upath['currentpath'] = []
        upath['visited'] = []
        print bldupath(grammar,grammar[i][0],upath)

# grammar - List, list of rules
# current - string, working element
# upath - Dictionary, utterance paths through grammar rules
#           Key = path, result = value
# level - List, one element recursion depth counter to prevent infinite recursion
def bldupath(grammar,current,upath,level=None):
    if level == None:
        level = 1
    else:
        level += 1
    assert level < 10
    print "\nEntered bldupath - current = " + str(current) + ", upath = " + str(upath) \
        + ", Level = " + str(level)
    # Iterate through grammar rules sequentially to find a rule # for current
    for j in range(len(grammar)):
        # Does current match rule lhs?
        if grammar[j][0] == current:
            # Found valid rule #
            # Iterate through rule rhs:
            for symbol in grammar[j][1]:
                print "looking at symbol (" + str(symbol) + "), lhs = " + \
                    str([rule[0] for rule in grammar if rule[0] == symbol])
                # Iterate through rules - need rule #
                for k in range(len(grammar)):
                    # Does symbol match rule lhs?
                    if grammar[k][0] == symbol:
                        # Yes - symbol is non-terminal
                        # Before recursing, make sure we haven't been here already
                        if upath['currentpath']+[upath['currentrule']] not in upath['visited']:
                            # Save rule #
                            upath['currentpath'].append(upath['currentrule'])
                            # Change currentrule to just selected one
                            upath['currentrule'] = k
                            # Recurse to derive terminals
                            bldupath(grammar,symbol,upath,level)
                        else:
                            print "Avoided recursion, path already taken..."
                # Collect symbol into results:
                upath['currentresult'] += [symbol]
            # End of iterating through rhs
            print "Finished iterating through rhs for rule"
    print "Reached the bottom - upath before = " + str(upath)
    # Add current grammar rule to currentpath
    upath['currentpath'].append(upath['currentrule'])
    # Save rule path to visited
    upath['visited'].append(upath['currentpath'])
    # Create a new key/value pair from currentpath and currentresult
    upath[tuple(upath['currentpath'])] = upath['currentresult'][:]
    # Pop currentresult since returning (from recursion level)
    upath['currentresult'].pop()
    # Pop currentpath since returning (from recursion level)
    upath['currentpath'].pop()
    # Result currentrule to last rule of currentpath
    upath['currentrule'] = upath['currentpath'][len(upath['currentpath'])-1]
    print "Reached the bottom - upath after = " + str(upath) + "\n"








            if current in visited:
                print "current in visited - returning..."
                return []
            else:
                new_visited = visited + [current]
                for rhs in [rule[1] for rule in grammar if rule[0] == current]:
                    print "Iterating through rhs in helper, currently = " + str(rhs)
                    result = []
                    for symbol in rhs:
                        print "Iterating through symbol in helper, currently = " + \
                            str(symbol)
                        result = result + helper(grammar,symbol,new_visited)
                    return result
                print "Fell through..."
                return []
        print helper(grammar,lhs,[])



def cfgempty(grammar,symbol,visited):
    # Base case
    # 1) non-terminal, visited this before, return None
    # 2) terminal, return terminal
    # Recursive case
    # Go through symbols with rules, substitue, recurse
    # If returned result not null, return string
    if symbol in visited:
        # no infinite loops!
        return None
    # Is symbol a terminal? (any matches mean no...)
    elif not any([ rule[0] == symbol for rule in grammar ]):
        return [symbol]
    else:
        new_visited = visited + [symbol] # update visited
        # consider every rewrite rule "symbol --> RHS" (ie rules[1])
        for rhs in [r[1] for r in grammar if r[0] == symbol]:
            # check if every part of RHS is non-empty a terminal
            if all([None != cfgempty(grammar,r,new_visited) for r in rhs]):
                result = [] # gather up result
                for r in rhs:
                    result = result + cfgempty(grammar,r,new_visited)
                return result
    return None # no luck

