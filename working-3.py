# grammar - List, list of rules
# upath - Dictionary, utterance paths through grammar rules
#           Key = path, result = value
def expand(grammar,upath=None):
    if upath == None:
        upath = {}
    print "Entered expand"
    upath['visited'] = []
    for i in range(len(grammar)):
        print "\nIterating through lhs, currently - rule #" + str(i) + " - " + \
            str(grammar[i])
        count = 0
        upath['morepaths'] = 1
        while upath['morepaths'] and count < 10 >= 1:
            upath['seedrule'] = i
            upath['currentrule'] = i
            upath['currentresult'] = []
            upath['currentpath'] = [i]
            upath['finalpath'] = []
            upath['savemorepaths'] = []
            upath['validpath'] = True
            count += 1
            print "calling bldupath, upath['morepaths'] = " + str(upath['morepaths'])
            bldupath(grammar,grammar[i][0],upath)
            print "returning from bldupath, upath = " + str(upath)
        # End of while
        print "End of iteration " + str(i) + ", upath now = " + str(upath)

# grammar - List, list of rules
# element - String, LHS string to match
def lhsmatches(grammar,element):
    lhsrules = []
    for rulein in range(len(grammar)):
        if grammar[rulein][0] == element:
            lhsrules.append((grammar[rulein][0],grammar[rulein][1],rulein))
    print "\nEntered lhsmatches with element = " + str(element) + ", returning " \
        + "lhsrules = " + str(lhsrules)
    return lhsrules

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
    for rhs in grammar[upath['currentrule']][1]:
        # How many LHS matches for current RHS?
        upath['morepaths'] = len([rule[0] for rule in grammar if rule[0] == rhs])
        if upath['morepaths'] >= 1:  # Non-terminal
            for lhs in lhsmatches(grammar,rhs):
                upath['morepaths'] -= 1
                if upath['currentpath']+[lhs[2]] not in upath['visited']:
                    # New path, mark valid
                    upath['validpath'] = True
                    upath['currentpath'].append(lhs[2])
                    upath['currentrule'] = lhs[2]
                    # Save morepaths...
                    upath['savemorepaths'].append(upath['morepaths'])
                    bldupath(grammar,lhs[0],upath,level)
                    # Restore morepaths...
                    upath['morepaths'] = upath['savemorepaths'].pop()
                    print "\nReturned from bldupath recursive call, upath now = " + \
                        str(upath)
                    break  # Only want one match
                    # But need loop to try different paths for next iteration
                else:  # Already been down this path
                    # Path now invalid until successfully recurse...
                    upath['validpath'] = False
        else:  # Terminal
            upath['currentresult'].append(rhs)
    # End of for
    if upath['currentrule'] == upath['seedrule']:
        # Only add new utterance/sentence and rule path if valid
        if upath['validpath']:
            upath[tuple(upath['finalpath'])] = upath['currentresult'][:]
        # Always update visited so we don't keep retrying same path...
        upath['visited'].append(upath['finalpath'][:])
        return  # Exit procedure
    else:
        if upath['finalpath'] == []:
            upath['finalpath'] = upath['currentpath'][:]
        upath['currentpath'].pop()
        upath['currentrule'] = upath['currentpath'][len(upath['currentpath'])-1]
        return  # Get back to top level





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
                            # Set flag
                            upath['newpath'] = True
                            # Recurse to derive terminals
                            bldupath(grammar,symbol,upath,level)
                        else:
                            print "Avoided recursion, path already taken..."
                # Collect symbol into results:
                upath['currentresult'] += [symbol]
            # End of iterating through rhs
            print "Reached the bottom - upath before = " + str(upath)
            if upath['newpath']:
                print "new path!"
                # Add current grammar rule to currentpath
                upath['currentpath'].append(upath['currentrule'])
                # Save rule path to visited
                upath['visited'].append(upath['currentpath'][:])
                # Create a new key/value pair from currentpath and currentresult
                upath[tuple(upath['currentpath'])] = upath['currentresult'][:]
                # Unset flag
                upath['newpath'] = False
            # Pop currentresult since returning (from recursion level)
            upath['currentresult'].pop()
            # Save rule path to visited
            upath['visited'].append(upath['currentpath'][:])
            # Pop currentpath since returning (from recursion level)
            upath['currentpath'].pop()
            # Reset currentrule to last rule of currentpath
            upath['currentrule'] = upath['currentpath'][len(upath['currentpath'])-1]
            print "Reached the bottom - upath after = " + str(upath) + "\n"
            return








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

