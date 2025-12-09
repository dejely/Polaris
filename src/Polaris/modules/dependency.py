class Entry:
    def __init__(self, key, value):
        self._key = key
        self._value = value

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    def __eq__(self, other):
        if not isinstance(other, Entry):
            return False
        return self.key == other.key and self.value == other.value

    def __str__(self):
        return f"<{self._key} : {self._value}>"

    def __repr__(self):
        return f"<{self._key} : {self._value}>"

class DLLNode:
	def __init__(self,item=None,prev_node=None,next_node=None):

		self.item = item 
		self.prev = prev_node
		self.next = next_node

	def __repr__(self):
		# string representation of DLLNode object
		return '<DLLNode: %s>' % str(self.item)

	# Getter and Setter Methods
	# Use self.item, self.prev, and self.next

	def get_item(self):
		return self.item

	def set_item(self,item):
		self.item = item

	def get_prev(self):
		return self.prev

	def set_prev(self,prev_node):
		self.prev = prev_node

	def get_next(self):
		return self.next

	def set_next(self,next_node):
		self.next = next_node