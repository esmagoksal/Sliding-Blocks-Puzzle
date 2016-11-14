
import math
import copy
import time
import Queue
import bisect

class Board:

	def __init__(self, mode, size, initial_state, final_state):

		self.mode = mode
		self.size = size
		self.sizex = size[0]
		self.sizey = size[1]
		self.num_of_pieces = size[2]

		self.visited = 0

		self.initial_state = initial_state
		self.final_state = final_state

		self.onlyCounts = []
		self.countList = []

		temp = {}
		for p in range(1,self.num_of_pieces+1):
			count = 0
			prex = 0
			prey = 0
			countx = 0
			county = 0
			for i, row in enumerate(self.initial_state):

				for j, piece in enumerate(row):
					if self.initial_state[i][j] == p and count == 0:
						count = count+1
						prex = i
						prey = j
						countx = countx+1
						county = county+1
						temp = {p: (countx,county)}
					elif self.initial_state[i][j] == p and count > 0:
						if prex == i and prey != j:
							count = count+1
							prex = i
							prey = j
							county = county+1
							temp = {p: (countx,county)}
						elif prex != i and prey == j:
							count = count+1
							prex = i
							prey = j
							countx = countx+1
							temp = {p: (countx,county)}	
							
			self.countList.append(temp)
			self.onlyCounts.append(count)


	def manhattan(self):
		manhattan =0
		
		for piece in range(1,self.num_of_pieces+1):
			found = False
			for i, row in enumerate(self.initial_state):
				if piece in row:
					for k, grow in enumerate(self.final_state):
						if piece in grow:
							if found == False:
								found = True
								manhattan += math.fabs(i - k) + math.fabs(row.index(piece) - grow.index(piece))


		return manhattan



	def allpossibleactions(self):

		actions = []
		temp = {}
		countlist = self.countList

		for piece in range(1,self.num_of_pieces+1):
			measure = countlist[piece-1]
			found = False
			for i, row in enumerate(self.initial_state):
				if piece in row:
					j = row.index(piece)
					if found == False:
						found = True
						if i>0 :
							check = True
							for k in range(j, j+measure[piece][1]):
								if self.initial_state[i-1][k] != 0:
									check = False
							if check == True:		
								temp = {piece: (i-1,j)}
								if temp not in actions:
									actions.append(temp)
								
						if i < self.sizex -1 :
							check = True
							for k in range(j, j+measure[piece][1]):
								if self.initial_state[i+1][k] != 0:
									check = False
							if check == True:	
								temp = {piece: (i+1,j)}
								if temp not in actions:
									actions.append(temp)
								
						if j>0 :
							check = True
							for k in range(i, i+measure[piece][0]):
								if self.initial_state[k][j-1] != 0:
									check = False
							if check == True:
								temp = {piece: (i,j-1)}
								if temp not in actions:
									actions.append(temp)

						if j < self.sizey -1 :
							check = True
							for k in range(i, i+measure[piece][0]):
								if self.initial_state[k][j+1] != 0:
									check = False
							if check == True:	
								temp = {piece: (i,j+1)}
								if temp not in actions:
									actions.append(temp)

						if i+measure[piece][0] -1 < self.sizex -1:
							check = True
							for k in range(j, j+measure[piece][1]):
								if self.initial_state[i+measure[piece][0]][k] != 0:
									check = False
							if check == True:	
								temp = {piece: (i+1,j)}
								if temp not in actions:
									actions.append(temp)	

						if j+measure[piece][1] -1  < self.sizey -1:
							check = True
							for k in range(i, i+measure[piece][0]):
								if self.initial_state[k][j+measure[piece][1]] != 0:
									check = False
							if check == True:	
								temp = {piece: (i,j+1)}
								if temp not in actions:
									actions.append(temp)					


		return actions		

	def apply_action(self, action):
        
	    piece_key = action.keys()
	    piece = piece_key[0]
	    countlist = self.countList
	    measure = countlist[piece-1]


	    for i, row in enumerate(self.initial_state):
	    	if piece in row:
	    		j = row.index(piece)
	    		break

	    x, y = action[piece]
	    #print (i,j)
	    #print action
	    # check that the tile to move and the empty tile are neighbors
	    if (math.fabs(x - i) == 1) ^ (math.fabs(y - j) == 1):
	    	if (x - i) == -1:
	    		for a in range(i, i+measure[piece][0]):
	    			for b in range(j, j+measure[piece][1]):
	    				self.initial_state[a-1][b] = piece
	    		for k in range(y, y+measure[piece][1]):
    				self.initial_state[x+measure[piece][0]][k]= 0		

	    	elif (x - i) == 1:
	    		for a in range(i, i+measure[piece][0]):
	    			for b in range(j, j+measure[piece][1]):
	    				self.initial_state[a+1][b] = piece
	    		for k in range(y, y+measure[piece][1]):
    				self.initial_state[i][k]= 0			

	    	elif (y - j) == -1:
	    		for a in range(i, i+measure[piece][0]):
	    			for b in range(j, j+measure[piece][1]):
	    				self.initial_state[a][b-1] = piece
	    		for k in range(x, x+measure[piece][0]):
    				self.initial_state[k][y+measure[piece][1]]= 0		

	    	elif (y - j) == 1:
	    		for a in range(i, i+measure[piece][0]):
	    			for b in range(j, j+measure[piece][1]):
	    				self.initial_state[a][b+1] = piece
	    		for k in range(x, x+measure[piece][0]):
    				self.initial_state[k][j]= 0										

	    else:
	    	print "who" , action
	        raise ValueError("Invalid move")


	def solve_puzzle(self):

		start_time = time.clock()
		frontier = Queue.PriorityQueue()
		frontier.put(Graph(self,None, 0, None, self.manhattan()))
		#frontier = [Graph(self, None, 0, None, self.manhattan())]
		explored = []
		visited = 0
		solution = None

		#while True:
		while frontier and not solution:
		    self.visited += 1		    
		    #node = frontier.pop(0)
		    node = frontier.get()
		    
		    if node.board.manhattan() == 0:
		        moves = []
		        hodo = []
		        while node.parent:
		            hodo.append(node.action)
		            moves.append(node.board.initial_state)
		            solution = node
		            node = node.parent
		        moves.reverse()
		        hodo.reverse()

		        print "Solution found!"
		        print "move path", len(hodo)
		        print "Time:", time.clock() - start_time
		        break
		    else:

		        for new_node in node.expand():
		            
		            if new_node not in explored: # and new_node not in frontier:
		                #bisect.insort(frontier, new_node)
		                frontier.put(new_node)
		        
		        explored.append(node)  

		return moves




class Graph:

	def __init__(self, board, action, cost, parent, estimate):

		self.board = board
		self.action = action
		self.cost = cost
		self.parent = parent

		if(self.board.mode == 0):
			self.estimate = board.manhattan()

		else:

			rowcost = 0
			for i in range(len(self.board.final_state)):
				if self.board.initial_state[i]	!= self.board.final_state[i]:
					rowcost += 1 

			if rowcost > board.manhattan():
				self.estimate = rowcost
			else:
				self.estimate = rowcost + board.manhattan()	*3
			#self.estimate = board.visited + board.manhattan()*3

			

	def expand(self):

		nodes = []
		for action in self.board.allpossibleactions():
		    board = copy.deepcopy(self.board)
		    board.apply_action(action)

		    nodes.append(Graph(board, action, self.cost + 1, self, self.estimate))


		return nodes

	def _eq_(self,rhs):

		if isinstance(rhs, Graph):
			return self.board.initial_state == rhs.board.initial_state
		else:
			return rhs == self	

	def __lt__(self, rhs):
		assert isinstance(rhs, Graph)
		return self.estimate < rhs.estimate	


def main() :

	f = open('input.inp', 'r')

	num_of_states = int(f.readline().strip())

	count=0
	while(count!=num_of_states):
			mode= int(f.readline())
			size = [int(x) for x in f.readline().strip().split(' ')]
			initial_state = []
			lo = f.readline()

			for i in range(0,size[0]):
				temp = [int(x) for x in f.readline().split(' ')]
				initial_state.append(temp)

			final_states = []
			for k in range(0,size[3]):
				lo = f.readline()
				fstate=[]
				for j in range(0,size[0]):
					temp = [int(x) for x in f.readline().split(' ')]
					fstate.append(temp)	
				final_states.append(fstate)		

			raw_input('Press Enter')

			maxlen = 10000
			moves_result = []

			for state in final_states:
				board = Board(mode, size, initial_state,state)
				moves = board.solve_puzzle()
				if len(moves) >0 and len(moves) < maxlen:
					moves_result = moves 
					maxlen = len(moves)
			
			print initial_state
			for step in moves_result:
				print step
			
			count = count+1	

if __name__ == "__main__" : main()			