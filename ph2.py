MAX_LEN = 4

def extractPhrase(alignment, etext, ftext):
    if alignment == None:
        return None

    maxelen = 0
    maxflen = 0
    for align in alignment:
        if align[0] > maxelen:
            maxelen = align[0]
        if align[1] > maxflen:
            maxflen = align[1]
    maxelen = maxelen + 1
    maxflen = maxflen + 1

    #talign = [][]
    talign = [[True for x in xrange(maxflen)] for x in xrange(maxelen)]

    for align in alignment:
        talign[align[0]][align[1]] = False

    #tleft = [][][]
    tleft = [[[True for x in xrange(maxflen)] for x in xrange(maxelen)] for x in xrange(maxelen)]
    for i in range(maxelen):
        z = i + MAX_LEN
        if z > maxelen:
            z = maxelen
        for j in range(i, z):
            for k in range(maxflen):
                if j == i and k == 0:
                    tleft[i][j][k] = talign[j][k]
                elif k == 0:
                    tleft[i][j][k] = talign[j][k] and tleft[i][j-1][k]
                elif j == i:
                    tleft[i][j][k] = talign[j][k] and tleft[i][j][k-1]
                else:
                    tleft[i][j][k] = talign[j][k] and tleft[i][j-1][k] and tleft[i][j][k-1]

    #tdown = [][][]
    tdown = [[[True for x in xrange(maxelen)] for x in xrange(maxflen)] for x in xrange(maxflen)]
    for i in range(maxflen):
        z = i + MAX_LEN
        if z > maxflen:
            z = maxflen
        for j in range(i, z):
            for k in range(maxelen-1, -1, -1):
                if j == i and k == maxelen-1:
                    tdown[i][j][k] = talign[k][j]
                elif k == maxelen-1:
                    tdown[i][j][k] = talign[k][j] and tdown[i][j-1][k]
                elif j == i:
                    tdown[i][j][k] = talign[k][j] and tdown[i][j][k+1]
                else:
                    tdown[i][j][k] = talign[k][j] and tdown[i][j-1][k] and tdown[i][j][k+1]

    #tright = [][][]
    tright = [[[True for x in xrange(maxflen)] for x in xrange(maxelen)] for x in xrange(maxelen)]
    for i in range(maxelen-1, -1, -1):
        z = i - MAX_LEN
        if z < -1:
            z = -1
        for j in range(i, z, -1):
            for k in range(maxflen-1, -1, -1):
                if j == i and k == maxflen-1:
                    tright[i][j][k] = talign[j][k]
                elif k == maxflen-1:
                    tright[i][j][k] = talign[j][k] and tright[i][j+1][k]
                elif j == i:
                    tright[i][j][k] = talign[j][k] and tright[i][j][k+1]
                else:
                    tright[i][j][k] = talign[j][k] and tright[i][j+1][k] and tright[i][j][k+1]

    #tup = [][][]
    # print maxelen
    tup = [[[True for x in xrange(maxelen)] for x in xrange(maxflen)] for x in xrange(maxflen)]
    for i in range(maxflen-1, -1, -1):
        z = i - MAX_LEN
        if z < -1:
            z = -1
        for j in range(i, z, -1):
            for k in range(maxelen):
                #print i, j, k
                if j == i and k == 0:
                    tup[i][j][k] = talign[k][j]
                elif k == 0:
                    tup[i][j][k] = talign[k][j] and tup[i][j+1][k]
                elif j == i:
                    # if i == 0 and j == 0 and k == 1:
                    #     print tup[i][j][k]
                    #     print tup[i][j][k-1]
                    #     print talign[k][j]
                    tup[i][j][k] = talign[k][j] and tup[i][j][k-1]
                else:
                    tup[i][j][k] = talign[k][j] and tup[i][j+1][k] and tup[i][j][k-1]

    alignlist = []
    for i in range(maxelen):
        zi = i + MAX_LEN
        if zi > maxelen:
            zi = maxelen
        for j in range(maxflen):
            zj = j + MAX_LEN
            if zj > maxflen:
                zj = maxflen
            for k in range(i, zi):
                for l in range(j, zj):
                    left = False
                    if j == 0:
                        left = True
                    else:
                        left = tleft[i][k][j-1]

                    down = False
                    if k == maxelen-1:
                        down = True
                    else:
                        down = tdown[j][l][k+1]

                    right = False
                    if l == maxflen-1:
                        right = True
                    else:
                        right = tright[k][i][l+1]

                    up = False
                    if i == 0:
                        up = True
                    else:
                        up = tup[l][j][i-1]

                    if up and down and left and right:
                        alignlist.append((i, j, k, l))
    alist = []
    for bound in alignlist:
        aset = set()
        for align in alignment:
            if inBound(align, bound):
                aset.add(align)
        if not len(aset) == 0 and not aset in alist:
            alist.append(aset)
    # print alignlist
    # print alist
    # print len(alist)

    # if len(alist) == 27:
    #     print tleft[38][43][36]
    #     print tdown[37][39][44]
    #     print tright[43][38][40]
    #     print tup[39][37][36]
    # print talign[1][0]
    # print tup[0][0][1]
    for z in alist:

        set1 = set()
        set2 = set()
        for a in z:
            set1.add(a[0])
            set2.add(a[1])
        string1 = ""
        string2 = ""
        for a in set1:
            string1 = string1 + etext[a] + " "
        for a in set2:
            string2 = string2 + ftext[a] + " "
       # print string1, " ||| ", string2

def inBound(align, bound):
    i = bound[0]
    j = bound[1]
    k = bound[2]
    l = bound[3]
    return not(align[0] < i or align[0] > k or align[1] < j or align[1] > l)
                            
