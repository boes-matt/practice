class Node(object):

    def __init__(self, data=None, next=None):
	self.data = data
	self.next = next

    def __eq__(self, other):
	"Return True if data values equal."
	if type(other) is type(self):
	    return other.data == self.data
	return False

    def __ne__(self, other):
	return not self.__eq__(other)

    def equal(self, other):
	"Deep equal comparison."
	if type(other) is type(self):
	    return other.__dict__ == self.__dict__
	return False

    def __str__(self):
	return str(self.data)

class List(object):

    def __init__(self, head=None):
	self.head = head

    def empty(self):
	return not self.head

    def cons(self, node):
	node.next = self.head
	self.head = node

    def pop(self):
	first = self.head
	self.head = self.head.next
	return first

    def reverse(self):
	lst = List()
	while not self.empty():
	    lst.cons(self.pop())
	self.head = lst.head

    def index(self, pos):
	"Return node as index position pos."
	pass

    def index_of(self, node):
	i = 0
	for n in self:
	    if n == node: return i
	    i += 1
	return -1

    def length(self):
	return sum([1 for node in self])

    def insert(self, x, pos):
	"Insert either the node or list x beginning at index position pos."
	pass

    def append(self, x):
	"Append either the node or list x to the end of the list."
	pass

    def __iter__(self):
	curr = self.head
	while curr:
	    yield curr
	    curr = curr.next

    #def __eq__(self, other):	

    def __str__(self):
	if self.empty():
	    return '[]'
	else:
	    s = ['[']
	    for node in self:
		s.append(str(node))
		s.append(', ')
	    s = s[:-1]
	    s.append(']')
	    return ''.join(s)

class Test(object):
    def test(self):
    
	a = Node()
	a.data = 'a'
	assert str(a) == 'a'	

	lst0 = List()
	assert str(lst0) == '[]'
	assert lst0.empty()
	
	lst1 = List(a)
	assert str(lst1) == '[a]'
	assert lst1.empty() == False	

	b = Node('b')
	assert b.data == 'b'
	
	c = Node('c')
	lst1.cons(b)
	lst1.cons(c)
	assert str(lst1) == '[c, b, a]'	

	assert c.next.equal(b)
	assert b.next.equal(a)
	
	b1 = Node('b')
	assert b1.equal(b) == False
	assert b1 == b # True, equal data values
	assert c != b
	
	assert lst1.index_of(c) == 0
	assert lst1.index_of(b) == 1
	assert lst1.index_of(b1) == 1
	assert lst1.index_of(a) == 2
	assert lst1.index_of(Node('j')) == -1

	lst1.reverse()
	assert str(lst1) == '[a, b, c]'
	
	elst = List()
	elst.reverse()
	assert str(elst) == '[]'

	head = lst1.pop()
	assert str(head) == 'a'
	assert str(lst1) == '[b, c]'
	lst1.cons(head)
	assert str(lst1) == '[a, b, c]'
    	
	lst2 = List()
	lst2.cons(Node('a'))
	assert str(lst2) == '[a]'
	lst2.pop()
	assert lst2.empty()

	assert lst1.length() == 3
	assert lst2.length() == 0

	#List ops: index, index_of, insert, append, ==

    	return 'tests pass'

print Test().test()
