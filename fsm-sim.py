# FSM Simulation

edges = {(1, 'a') : 2,
         (2, 'a') : 2,
         (2, '1') : 3,
         (3, '1') : 3}

accepting = [3]

def fsmsim(string, current, edges, accepting):
    ##print "Entering fsmsim"
    ##print "string = " + string + ", current = " + str(current)
    if string == "":
        return current in accepting
    else:
        letter = string[0]
        ##print "letter = " + str(letter)
        string = string[1:]
        ##print "string = " + string
        # QUIZ: You fill this out!
        # Is there a valid edge?
    if (current,letter) in edges:
        current = edges[(current,letter)]
        ##print "current = " + str(current)
        return fsmsim(string,current,edges,accepting)
        # If so, take it.
        # If not, return False.
    else:
        return False
        # Hint: recursion.


print fsmsim("aaa111",1,edges,accepting)
# >>> True

