# grammar - List, list of rules
# upath - Dictionary, utterance paths through grammar rules
#           Key = path, result = value
def expand(grammar,upath=None):
    if upath == None:
        upath = {}
    print "Entered expand"
    upath['visited'] = []
    upath['paths'] = []
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
            if upath['finalpath'] == []:
                upath['finalpath'] = upath['currentpath'][:]
            upath['paths'].append([grammar[upath['seedrule']][0][:],upath['finalpath'][:],upath['currentresult'][:]])
            ##upath[tuple(upath['finalpath'])] = upath['currentresult'][:]
        # Always update visited so we don't keep retrying same path...
        upath['visited'].append(upath['finalpath'][:])
        return  # Exit procedure
    else:
        if upath['finalpath'] == []:
            upath['finalpath'] = upath['currentpath'][:]
        upath['currentpath'].pop()
        upath['currentrule'] = upath['currentpath'][len(upath['currentpath'])-1]
        return  # Get back to top level

