from modules.dependency	import Entry, DLLNode

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BOLD = '\033[1m'
RESET = '\033[0m'

class DLLPriorityQueue:
	# DLL-based Priority Queue
	def __init__(self):

		self.size = 0
		self.head_guard = DLLNode(None)
		self.tail_guard = DLLNode(None)
		self.head_guard.set_next(self.tail_guard)
		self.tail_guard.set_prev(self.head_guard)

	def __repr__(self):

		display = []
		node = self.head_guard.get_next()
		while node != self.tail_guard:
			entry = node.get_item()
			priority = -entry.key
			line = f"<LGU: {GREEN + BOLD + entry.value + RESET} | Priority: {YELLOW + BOLD}{priority}{RESET}>"
			display.append(line)
			node = node.get_next()
			


		display = ', '.join(display)
		display = '{' + display + '}'
		return display

	def is_empty(self):
		return self.size == 0

class UnsortedPQ(DLLPriorityQueue):
	# Unsorted DLL-based Priority Queue
	def find_min_node(self):
		if self.is_empty():
			raise Exception('Empty PQ: cannot find min')

		#start at head
		current = self.head_guard.get_next()
		min_node = current


		while current != self.tail_guard: #traverse until we reach the end of the list
			if current.get_item().key < min_node.get_item().key: #just compare keys
				min_node = current
			current = current.get_next() #point to the next current

		return min_node

	def insert(self,key,value):

		#Create with key value param
		entry = Entry(key, value)

		ins_node = DLLNode(entry) #instantiate

		first = self.head_guard.get_next() #store the head

		#Link properly
		ins_node.set_prev(self.head_guard)
		ins_node.set_next(first)
		
		#link
		self.head_guard.set_next(ins_node)
		first.set_prev(ins_node)
		
		self.size += 1

	def remove_min(self):
		if self.is_empty():
			raise Exception('Empty PQ: cannot remove min')
		
		min_node = self.find_min_node() #store  the min node first\

		#point the neigbors to each other
		prev = min_node.get_prev()
		next = min_node.get_next()
		prev.set_next(next)
		next.set_prev(prev)
		#point to None
		min_node.set_next(None)
		min_node.set_prev(None)

		self.size -= 1
		return min_node.get_item().value
		

	def min(self):
		if self.is_empty():
			raise Exception('Empty PQ: no min')
		return self.find_min_node().get_item().value

class SortedPQ(DLLPriorityQueue):
	# Sorted DLL-based Priority Queue
	def insert(self,key,value):
		entry = Entry(key, value)

		ins_node = DLLNode(entry)
		current = self.head_guard.get_next()

		while current != self.tail_guard:
			if current.get_item().key <= ins_node.get_item().key:
				current = current.get_next()
			else: #if condition is fulfilled we executei then break so it does not loop further
				#linking
				ins_node.set_next(current)
				ins_node.set_prev(current.get_prev())

				current.get_prev().set_next(ins_node)
				current.set_prev(ins_node)
				break

		

		if current == self.tail_guard: #case for when we loop to the most back of the list
			#store orig last node
			last = self.tail_guard.get_prev()
			#linking
			ins_node.set_prev(last)
			ins_node.set_next(self.tail_guard)
			last.set_next(ins_node)
			self.tail_guard.set_prev(ins_node)
				

		self.size += 1

	def extract_max(self):
		pass




	def remove_min(self):
		if self.is_empty():
			raise Exception('Empty PQ: cannot remove min')
		#store head/min
		
		min_node = self.head_guard.get_next()

		#[head_guard] <-> [min] <-> [new min]

		#store the new min and point prev to head guard
		new_min = min_node.get_next()
		new_min.set_prev(self.head_guard)
		#overwrite point headguard to point to new min
		self.head_guard.set_next(new_min)
		#head_guard prev is None

		#point to none
		min_node.set_prev(None)
		min_node.set_next(None)

		self.size -= 1

		return min_node.get_item().value

	def min(self):
		if self.is_empty():
			raise Exception('Empty PQ: no min')
		return self.head_guard.get_next().get_item().value
		