def nfsmtrim(edges, accepting, current=1, visited=None, working=None, newedges=None, newaccepting=None):
    if visited == None:
        visited = []
    if working == None:
        working = []
    if newedges == None:
        newedges = {}
    if newaccepting == None:
        newaccepting = []
    ##print "Entered nfsmtrim - current = " + str(current) + ", visisted = " + \
    ##    str(visited) + ", working = " + str(working)
    if current in accepting and visited != []:
        ##print "Found valid path!  (current - " + str(current) + " in accepting - " + str(accepting) + ")\n"
        # path valid, save accepting state
        if current not in newaccepting:
            newaccepting.append(current)
        ##print "newaccepting now = " + str(newaccepting)
        # place valid path elements into newedges
        for i in working:
            if (i[0],i[1]) not in newedges:
                newedges[(i[0],i[1])] = [i[2]]
            else:
                if i[2] not in newedges[(i[0],i[1])]:
                    newedges[(i[0],i[1])].append(i[2])
        ##print "newedges now = " + str(newedges)
    # May need to go through edge iteration twice when find a valid path forward
    # Or when returning from failed (results==False) recursion
    for count in range(1):
        if count == 0:
            ##print "edge iteration, first pass..."
            pass
        # Iterate through all edges
        for edge in edges:
            ##print "Evaluating edge " + str(edge) + ", current = " + str(current)
            if edge[0] == current:
                for nextstate in edges[edge]:
                    ##print "Evaluating nextstate " + str(nextstate) + " from " + \
                    ##    str(edges[edge])
                    # We've already gone here
                    if [edge[0],edge[1],nextstate] in visited:
                        ##print "Already been to this state!"
                        pass
                    else:
                        visited.append([edge[0],edge[1],nextstate])
                        working.append([edge[0],edge[1],nextstate])
                        ##print "(added) visited now = " + str(visited) + ", working = " + str(working)
                        # When recursively call nfsmtrim, must re-iterate through edges
                        # or else can miss a valid path - do by resetting count...
                        count -= 1
                        ##print "Decremented count..."
                        nfsmtrim(edges,accepting,nextstate,visited,working,newedges,newaccepting)
                        ##print "returned from nfsmtrim"
                        # check if path loops to valid state before discarding
                        if working != []:
                            chkpath = working.pop()
                            current = chkpath[0]
                            ##print "Changed current to popped value:  " + str(current)
                            for i,j in newedges:
                                if chkpath[2] == i:
                                    if (chkpath[0],chkpath[1]) not in newedges:
                                        newedges[(chkpath[0],chkpath[1])] = [chkpath[2]]
                                        ##print "Found valid path, updated newedges:  " + str(newedges)
                                        break
                                    else:
                                        if chkpath[2] not in newedges[(chkpath[0],chkpath[1])]:
                                            newedges[(chkpath[0],chkpath[1])].append(chkpath[2])
                                            ##print "Found valid path, updated newedges:  " + str(newedges)
                                            break
                            ##print "(popped) working:  " + str(chkpath)
                            # pop self-looping states too...
                            # keep repeating until no self-looping outer paths
                            #while True:
                            #    if working != []:
                            #        if working[len(working) - 1][0] == working[len(working) - 1][2]:
                            #            print "(popped) working:  " + str(working.pop())
                            #        else:
                            #            break
                            #    else:
                            #        break
                        else:
                            ##print "working empty!"
                            pass
                ##print "Made it through inner for loop"
        # End of inner loop
    # End of outer loop
    ##print "Made it through outer for loop"
    ##print "visited now = " + str(visited) + ", working now = " + str(working)
    ##print "current = " + str(current)
    if working == []:
        ##print "Returning (newedges,newaccepting) - " + str((newedges,newaccepting)) + "\n\n"
        return (newedges,newaccepting)
    else:
        ##print ""
        return None

