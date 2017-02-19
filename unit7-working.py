def evaluate(ast):
    #print "Entered evaluate:\n" + str(ast)
    market = {}  # person, verb, {merchandise,} amount
    buys = {}  # buy = amount, person, count
    sells = {}  # sell = amount, person, count
    for e in ast:
        #print "Evaluating " + str(e)
        if e[1] == 'has':
            market[e[0]] = e[2]                
        elif e[1] == 'buy':
            # Possible sanity check
            # Removed because buyer may sell something else and
            # then have sufficient funds later on...
            #if market[e[0]] < e[3]:
            #    print 'Transaction rejected - insufficient funds:\n' + \
            #        str(e) + '\n'
            #else:
                if e[2] not in buys:
                    buys[e[2]] = [e[3],e[0],1]
                else:
                    buys[e[2]][2] += 1
        elif e[1] == 'sell':
            if e[2] not in sells:
                sells[e[2]] = [e[3],e[0],1]
            else:
                sells[e[2]][2] += 1
        else:
            raise NameError('Undefined verb:  ' + e[1])
        #print "Market:\n" + str(market)
        #print "Buys:\n" + str(buys)
        #print "Sells:\n" + str(sells)
    settleup(market,buys,sells)
    #print "Exiting evaluate, market:\n" + str(market) + '\n\n'
    return market

def settleup(market,buys,sells):
    #print "\nEntered settleup:\n" + str(market) + '\n' + \
    #    str(buys) + '\n' + str(sells)
    recurse = False
    for buy in buys:  # buy = amount, person, count
        if buy in sells:  # sell = amount, person, count
            if buys[buy][0] == sells[buy][0]:  # possible trade found
                amount = buys[buy][0]
                if market[buys[buy][1]] < amount:  # Insufficient funds
                    # Buyer may sell something and have sufficeint funds
                    # later - continue iterating to next buy transaction
                    # skipping rest of transaction processing code
                    continue
                # Successful transaction, set recurse
                recurse = True
                # Deduct amount from buyer
                market[buys[buy][1]] -= amount
                # Add amount to seller
                market[sells[buy][1]] += amount
                # Decrement count for sell and remove if == 0
                sells[buy][2] -= 1
                if sells[buy][2] < 1:
                    del sells[buy]
                    #print "Sells now:  " + str(sells)
                # Decrement count for buy and remove if == 0
                buys[buy][2] -= 1
                if buys[buy][2] < 1:
                    del buys[buy]
                    #print "Buys now:  " + str(buys)
                    # Dictionary changed size, break out of loop
                    #print "Market now:  " + str(market)
                    break
    # If find a valid trade then recurse to check for another
    # Can have multiple equivalent buys and sells (count > 1)
    if recurse and buys and sells:
        settleup(market,buys,sells)
    #print "Exiting settleup..."

