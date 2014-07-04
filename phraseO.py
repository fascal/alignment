
def printAlignment(alignment):
#	phrasePairing(alignment)
	rectlist = []
	head = 0
	tail = 0
	searchedlist = []
	for align in alignment:
		nlist = findAdjWord(align, alignment)
		isItemDuplicate = False
		for item in nlist:
			if item in searchedlist:
				isItemDuplicate = True
				break
		if isItemDuplicate:
			continue
	#	print "nlist"
	#	print nlist
	#	print "searchedlist"
	#	print searchedlist
		searchedlist = searchedlist + list(nlist)
	#	print list(nlist)
		rectlist = rectlist + [Rect(nlist)]
		head = head + 1

	while head != tail:
		current = rectlist[tail]
		nr = findAdjRect(current, rectlist)
		if nr == None:
			tail = tail + 1
			continue
		nr = nr.combineRects([current])
# need to get a rect constructor that combines two rects
		if nr != None and nr not in rectlist:
			rectlist = rectlist + [nr]
			#print "current", current, "nr", nr
			#print rectlist
			head = head + 1
		tail = tail + 1
	for r in rectlist:
		print r.alignlist
		
	
def findAdjRect(rect, rectlist):
	x = rect.upperleft[1] + rect.width
	y = rect.upperleft[0] + rect.height
	for r in rectlist:
		if r == rect:
			continue
		else:
			if r.isPosInside((x, y)):
			#	print rect.upperleft, rect.width, rect.height
			#	print r.upperleft, r.alignlist
				return r
	return None

def phrasePairing(alignments):

	for align in alignments:
		# adjPos = findAdjWord(align, alignments)
		# print adjPos
		alignmentlist = findAdjWord(align, alignments)

		#print alignmentlist


def getPairInDirection(pos, directIndex):
	if directIndex == 0:
		return (pos[0] - 1, pos[1])
	elif directIndex == 1:
		return (pos[0], pos[1] + 1)
	elif directIndex == 2:
		return (pos[0] + 1, pos[1])
	elif directIndex == 3:
		return (pos[0], pos[1] - 1)
	else:
		return None

def findAdjWord(pos, alignments):
	#print "finding adj word, init: ", pos
	queue = [pos]
	head = 1
	tail = 0

	while head != tail:
		current = queue[tail]
		tail = tail + 1

		for i in range(4):
			pair = getPairInDirection(current, i)
			if pair not in queue and pair in alignments:
				queue = queue + [pair]
				head = head + 1
			
	return queue

def findAdjWord2(pos, alignments):
	poslist = (pos[0] - 1, pos[1] + 1), (pos[0], pos[1] + 1), (pos[0] + 1, pos[1] + 1)
	lenAlign = len(alignments)
	for p in poslist:
		isPairNormal = True
		for num in p:
			if num < 0 or num == lenAlign:
				isPairNormal = False
				break
		
		if isPairNormal:
			if not(p in alignments):
				continue
			up = p[0]
			down = p[0]

			listf = [p]

			while True:
				c = 0
				if (up != -1):
					up = up - 1
					if up > -1:
						if (up, p[1]) in alignments:
							listf = listf + [(up, p[1])]
							c = c + 1
						else:
							up = -1

				if (down != lenAlign):
					down = down + 1
					if down < lenAlign:
						if (down, p[1]) in alignments:
							listf = listf + [(down, p[1])]
							c = c + 1
						else:
							down = lenAlign

				if c != 2:
					break
				
			return listf
			
class Rect:
	def __init__(self, ul, w = None, h = None):
		if not(w == None and h == None):
			self.upperleft = ul
			self.width = w
			self.height = h
		else:
			if ul == None:
				return
			xmin = ul[0][0]
			xmax = ul[0][0]
			ymin = ul[0][1]
			ymax = ul[0][1]
			for pos in ul:
				if pos[0] < xmin:
					xmin = pos[0]
				if pos[0] > xmax:
					xmax = pos[0]
				if pos[1] < ymin:
					ymin = pos[1]
				if pos[1] > ymax:
					ymax = pos[1] 
			self.upperleft = (xmin, ymin)
			self.width = xmax - xmin + 1
			self.height = ymax - ymin + 1
			self.alignlist = ul
			
	def __repr__(self):
		return "upperleft: %s width: %d height %d\n" % (self.upperleft, self.width, self.height)

	def isPosInside(self, pos):
		x = pos[0]
		y = pos[1]
		if x < self.upperleft[0] or x >= self.upperleft[0] + self.height:
			return False
		if y < self.upperleft[1] or y >= self.upperleft[1] + self.width:
			return False
		return True

	def combineRects(self, rectlist):
		list = self.alignlist;
		for rect in rectlist:
			list = list + rect.alignlist
		return Rect(list)

if __name__ == "__main__":
	rect = Rect([(3,2), (3,3), (3,4)])
	print rect
	
