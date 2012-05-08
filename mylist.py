import itertools

class Node(object):

    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next

    def __eq__(self, other):
        """Return True if data values equal."""
        if type(other) is type(self):
            return other.data == self.data
        return False

    def __ne__(self, other):
        return not self == other

    def equal(self, other):
        """Deep equal comparison."""
        if type(other) is type(self):
            return other.__dict__ == self.__dict__
        return False

    def __str__(self):
        return str(self.data)

class List(object):

    def __init__(self, head=None):
        # TODO: Allow list constructor to accept multiple elements at initialization
        self.head = head
        if head:
            self.len = 1
        else:
            self.len = 0

    def empty(self):
        return not self.head

    def length(self):
        return self.len

    def cons(self, node):
        node.next = self.head
        self.head = node
        self.len += 1

    def pop(self):
        first = self.first()
        self.head = self.head.next
        self.len += -1
        first.next = None
        return first

    def first(self):
        if self.head:
            return self.head
        else:
            raise Exception('The list is empty.')

    def rest(self):
        if self.head:
            return List(self.head.next).copy()
        else:
            raise Exception('The list is empty.')

    def last(self):
        # TODO: Cache and update last element for efficiency
        return self.index(self.length() - 1) if self.length() else None

    def reverse(self):
        lst = List()
        while not self.empty():
            lst.cons(self.pop())
        self.head = lst.head
        self.len = lst.length()

    def rev(self):
        """Reverse in place."""
        prev = None
        curr = self.head
        while curr:
            save_next = curr.next
            curr.next = prev
            prev = curr
            curr = save_next
        self.head = prev

    def rrev(self, prev=None):
        """Recursive reverse in place."""
        if not self.head:
            self.head = prev
        else:
            save_next = self.head.next
            self.head.next = prev
            prev = self.head
            self.head = save_next
            self.rrev(prev)

    # TODO: def sort(self):

    def index(self, pos):
        """Return node as index position pos."""
        for i, n in enumerate(self):
            if i == pos: return n
        raise Exception('Index out of bounds.')

    def find(self, node):
        for i, n in enumerate(self):
            if n == node: return i
        return -1

    def insert(self, n, pos):
        """Insert the node n beginning at index position pos."""
        if pos == 0:
            self.cons(n)
        else:
            prev = self.index(pos-1)
            next = prev.next
            prev.next = n
            n.next = next
            self.len += 1

    # TODO: def remove(self, pos):

    def append(self, n):
        """Append the node n to the end of the list."""
        last = self.last()
        if last:
            last.next = n
            self.len += 1
        else:
            self.cons(n)

    # TODO: def concat(self, other):

    def copy(self):
        # TODO: Fix copy for list of lists
        lst = List()
        for n in self:
            lst.cons(Node(n.data))
        lst.rev()
        return lst

    def dump(self):
        s = ''
        s += '[\n'
        for n in self:
            s+= str((n.data, str(n.next)))
            s+= '\n'
        s += ']'
        return s

    def __iter__(self):
        curr = self.head
        while curr:
            yield curr
            curr = curr.next

    def __eq__(self, other):
        return all(itertools.imap(Node.equal, self, other)) if self.length() == other.length() else False

    def __ne__(self, other):
        return not self == other

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
        assert lst0 == List()
        assert lst0.empty()

        copy = lst0.copy()
        assert copy.empty()
        assert lst0 == copy

        lst1 = List(a)
        assert str(lst1) == '[a]'
        assert lst1 == List(Node('a'))
        assert lst1.empty() == False

        copy = lst1.copy()
        assert lst1 == copy

        b = Node('b')
        assert b.data == 'b'

        c = Node('c')
        lst1.cons(b)
        lst1.cons(c)
        assert str(lst1) == '[c, b, a]'

        copy = lst1.copy()
        copy.cons(Node('d'))
        assert str(copy) == '[d, c, b, a]'
        assert str(lst1) == '[c, b, a]'
        assert copy != lst1
        copy.pop()
        assert copy == lst1

        assert c.next.equal(b)
        assert b.next.equal(a)

        b1 = Node('b')
        assert b1.equal(b) == False
        assert b1 == b # True, equal data values
        assert c != b

        assert lst1.find(c) == 0
        assert lst1.find(b) == 1
        assert lst1.find(b1) == 1
        assert lst1.find(a) == 2
        assert lst1.find(Node('j')) == -1

        assert lst1.index(0) == c
        assert lst1.index(1) == b
        assert lst1.index(2) == a
        assert lst1.index(lst1.find(a)) == a
        assert lst1.find(lst1.index(2)) == 2

        e = ''
        try:
            lst1.index(3)
        except Exception:
            e = 'Error: Index out of bounds.'
        assert e == 'Error: Index out of bounds.'

        lst1.reverse()
        assert str(lst1) == '[a, b, c]'
        lst1.rev()
        assert str(lst1) == '[c, b, a]'
        lst1.rrev()
        assert str(lst1) == '[a, b, c]'

        elst = List()

        elst.reverse()
        assert str(elst) == '[]'
        elst.rev()
        assert str(elst) == '[]'
        elst.rrev()
        assert str(elst) == '[]'
        assert elst.length() == 0

        alst = List(Node('a'))

        alst.reverse()
        assert str(alst) == '[a]'
        alst.rev()
        assert str(alst) == '[a]'
        alst.rrev()
        assert str(alst) == '[a]'
        assert alst.length() == 1

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
        copy = lst3.copy()

        lst3.append(Node('f'))
        assert lst3.last() == Node('f')
        assert str(lst3) == '[a, b, c, d, e, f]'
        assert lst3.length() == 6

        assert copy.length() == 5
        assert copy != lst3
        copy.append(Node('f'))
        assert copy == lst3

        lst4 = List()
        assert lst4.last() is None
        lst4.append(Node('a'))
        assert str(lst4) == '[a]'

        # Nested lists
        lst5 = List()
        lst5.cons(List(Node('a')))
        lst5.cons(List(Node('b')))
        lst5.cons(List(Node('c')))
        assert str(lst5) == '[[c], [b], [a]]'
        #copy = lst5.copy()

        lst5.reverse()
        assert str(lst5) == '[[a], [b], [c]]'
        assert lst5.length() == 3

        #assert copy != lst5
        #copy.rev()
        #assert copy == lst5

        lst6 = List()

        e = ''
        try:
            lst6.first()
        except Exception:
            e = 'Error: The list is empty.'
        assert e == 'Error: The list is empty.'

        e = ''
        try:
            lst6.rest()
        except Exception:
            e = 'Error: The list is empty.'
        assert e == 'Error: The list is empty.'

        lst6.cons(Node('a'))
        assert str(lst6.first()) == 'a'
        assert str(lst6.rest()) == '[]'

        lst6.cons(Node('b'))
        lst6.cons(Node('c'))
        lst6.reverse()
        assert str(lst6.first()) == 'a'
        assert str(lst6.rest()) == '[b, c]'

        rest = lst6.rest()
        assert rest != lst6
        lst6.pop()
        assert rest == lst6

        lst7 = lst1.copy()
        assert str(lst7) == '[a, b, c]'
        rest = lst7.rest()
        rest.pop()
        assert str(rest) == '[c]'
        assert rest.length() == 1
        assert lst7 == lst1 # '[a, b, c]'
        assert lst7.length() == 3

        return 'tests pass'

print Test().test()
