def nfsmtrim(edges, accepting, current=1, visited=None, working=None, newedges=None, newaccepting=None, level=None):
    if visited == None:
        visited = []
    if working == None:
        working = []
    if newedges == None:
        newedges = {}
    if newaccepting == None:
        newaccepting = []
    if level == None:
        level = [1]
    else:
        level[0] += 1
    print "Entered nfsmtrim - current = " + str(current) + ", visisted = " + \
        str(visited) + ", working = " + str(working) + ", level = " + str(level[0])
    if current in accepting and visited != []:
        print "Found valid path!  (current - " + str(current) + " in accepting - " + str(accepting) + ")\n"
        return True
    else:
        # May need to go through edge iteration twice when find a valid path forward
        # Or when returning from failed (results==False) recursion
        for count in range(2):
            if count == 0:
                print "edge iteration, first pass..."
            else:
                print "edge iteration, second pass..."
            # Iterate through all edges
            for edge in edges:
                print "Evaluating edge " + str(edge) + ", current = " + str(current)
                if edge[0] == current:
                    for nextstate in edges[edge]:
                        print "Evaluating nextstate " + str(nextstate) + " from " + \
                            str(edges[edge])
                        # We've already gone here
                        if [edge[0],edge[1],nextstate] in visited:
                            print "Already been to this state!"
                            pass
                        else:
                            visited.append([edge[0],edge[1],nextstate])
                            working.append([edge[0],edge[1],nextstate])
                            print "(added) visited now = " + str(visited) + ", working = " + str(working)
                            if nfsmtrim(edges,accepting,nextstate,visited,working,newedges,newaccepting,level):
                                level[0] -= 1
                                print "returned from nfsmtrim True!  Level = " + str(level[0])
                                # path valid, save accepting state
                                current = nextstate
                                if current not in newaccepting:
                                    newaccepting.append(current)
                                print "newaccepting now = " + str(newaccepting)
                                # place valid path elements into newedges
                                for i in working:
                                    if (i[0],i[1]) not in newedges:
                                        newedges[(i[0],i[1])] = [i[2]]
                                    else:
                                        if i[2] not in newedges[(i[0],i[1])]:
                                            newedges[(i[0],i[1])].append(i[2])
                                print "newedges now = " + str(newedges)
                            else:
                                level[0] -= 1
                                print "returned from nfsmtrim False, level = " + str(level[0])
                                # check if path loops to valid state before discarding
                                if working != []:
                                    chkpath = working.pop()
                                    current = chkpath[0]
                                    print "Changed current to popped value:  " + str(current)
                                    for i,j in newedges:
                                        if chkpath[2] == i:
                                            if (chkpath[0],chkpath[1]) not in newedges:
                                                newedges[(chkpath[0],chkpath[1])] = [chkpath[2]]
                                                print "Found valid path, updated newedges:  " + str(newedges)
                                                break
                                            else:
                                                if chkpath[2] not in newedges[(chkpath[0],chkpath[1])]:
                                                    newedges[(chkpath[0],chkpath[1])].append(chkpath[2])
                                                    print "Found valid path, updated newedges:  " + str(newedges)
                                                    break
                                    print "(popped) working:  " + str(chkpath)
                                else:
                                    print "working empty!"
                    print "Made it through inner for loop"
            # End of inner loop
        # End of outer loop
        print "Made it through outer for loop"
        print "visited now = " + str(visited) + ", working now = " + str(working)
        print "current = " + str(current) + ", level = " + str(level)
        if level[0] == 1:
            print "Returning (newedges,newaccepting) - " + str((newedges,newaccepting)) + "\n\n"
            return (newedges,newaccepting)
        else:
            print ""
            return False

#----------------------------------------------------------------------------------------------------

def nfsmtrim(edges, accepting): 
    # Write your code here.
    print "Entered nfsmtrim with edges = " + str(edges) + ", accepting = " + str(accepting)
    newedges = {}
    newaccepting = []
    visited = nfsmaccepts(edges,accepting)
    print "visited = " + str(visited)
    for i in range(len(visited)):
        for j in range(len(visited[i]['path'])):
            if (visited[i]['path'][j][0],visited[i]['path'][j][1]) not in newedges:
                newedges[(visited[i]['path'][j][0],visited[i]['path'][j][1])] = \
                    [visited[i]['path'][j][2]]
        print "visited[i]['accepting'] = " + str(visited[i]['accepting'])
        newaccepting.append(visited[i]['accepting'])
    print "Leaving nfsmtrim with (newedges,newaccepting) = " + str((newedges,newaccepting)) + "\n\n"
    return (newedges,newaccepting)

print nfsmtrim(edges,accepting)

