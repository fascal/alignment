MAX_LEN = 7
def extractPhrase(alignment):
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

    talign = [][]

    for i in range(maxelen):
        for j in range(maxflen):
            talign = True
    for align in alignment:
        talign[align[0]][align[1]] = False


    tleft = [][][]

    tleft[0][0][0] = talign[0][0]

    for i in [1:maxelen]:
        for j in [i:i + MAX_LEN]:
            tleft[i][j][0] = tleft[i][j-1][0] and talign[j][0]

    for k in [1:maxflen]:
        tleft[0][0][k] = tleft[0][0][k-1] and talign[0][k]

    for i in [1:maxelen]:
    	for j in [i:i + MAX_LEN]:
    		for k in [1:maxflen]:
    			tleft[i][j][k] = tleft[i][j-1][k] and tleft[i][j][k-1] and talign[j][k]


   	tup = [][][]

   	tup[0][0][0] = talign[0][0]

   	for i in [1:maxflen]:
   		for j in [i:i + MAX_LEN]:
   			tup[i][j][0] = tup[i][j-1][0]

   	for k in [1:maxelen]:
   		tup[0][0][k] = tup[0][0][k-1]

   	for i in [1:maxflen]:
   		for j in [i:i = MAX_LEN]:
   			for k in [1:maxflen]:
   				tup[i][j][k] = tup[i][j][k-1] and tup[i][j-1][k] and talign[k][j]

   	tdown = [][][]

   	tdown[0][0][maxelen-1] = talign[maxelen-1][0]

   	for k in range(maxelen-2, 0, -1):
   		tdown[0][0][k] = tdown[0][0][k+1]
   	for i in range(1, maxflen):
   		for j in range(i, i + MAX_LEN):
   			tdown[i][j][maxelen-1] = tdown[i][j-1][maxelen-1]
   	for i in range(1, maxelen):
   		for j in range(i, i + MAX_LEN):
   			for k in range(maxelen-1, 0, -1):
   				tdown[i][j][k] = tdown[i][j][k+1] and tdown[i][j-1][k] and talign[k][j]

   	

    # for i in range(maxelen):
    #     for j in range(maxflen):
    #         for k < range(MAX_LEN):
    #             for l < range(MAX_LEN):

