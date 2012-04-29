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
	for i, n in enumerate(self):
	    if i == pos: return n
	raise Exception('Index out of bounds.')

    def index_of(self, node):
	for i, n in enumerate(self):
	    if n == node: return i
	return -1

    def length(self):
	# Refactor: Cache and update on list mutation for speed up
	return sum([1 for node in self])

    def insert(self, n, pos):
	"Insert the node n beginning at index position pos."
	if pos == 0:
	    self.cons(n)
	else:
	    prev = self.index(pos-1)
	    next = prev.next
	    prev.next = n
	    n.next = next

    def dump(self):
	s = ''
	s += '[\n'
	for n in self:
	    s+= str((n.data, str(n.next)))
	    s+= '\n'
	s += ']'
	return s

    def last(self):
	last = None
	for n in self:
	    last = n
	return last

    def append(self, n):
	"Append the node n to the end of the list."
	last = self.last()
	if last:
	    last.next = n
	else:
	    self.cons(n)

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

	assert lst1.index(0) == c
	assert lst1.index(1) == b
	assert lst1.index(2) == a
	assert lst1.index(lst1.index_of(a)) == a
	assert lst1.index_of(lst1.index(2)) == 2	

	e = ''
	try:
	    lst1.index(3)
	except Exception:
	    e = 'Error!'
	assert e == 'Error!'

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

	lst3 = List(Node('d'))
	lst3.cons(Node('b'))
	lst3.insert(Node('a'), 0)
	assert lst3.dump() == "[\n('a', 'b')\n('b', 'd')\n('d', 'None')\n]"
	
	lst3.insert(Node('c'), 2)
	lst3.append(Node('e'))
	lst3.append(Node('f'))
	assert lst3.last() == Node('f')
	assert str(lst3) == '[a, b, c, d, e, f]'
	assert lst3.length() == 6

	lst4 = List()
	assert lst4.last() == None
	lst4.append(Node('a'))
	assert str(lst4) == '[a]'
	
	# Nested lists
	lst5 = List()
	lst5.cons(List(Node('a')))
	lst5.cons(List(Node('b')))
	lst5.cons(List(Node('c')))
	assert str(lst5) == '[[c], [b], [a]]'
	
	lst5.reverse()
	assert str(lst5) == '[[a], [b], [c]]'

	#List ops: __eq__

    	return 'tests pass'

print Test().test()
