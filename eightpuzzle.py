from collections import deque, OrderedDict
from itertools import groupby
from functools import update_wrapper
from time import clock
from sys import getsizeof

#### UTILITIES ####

def decorator(d):
    """Make function d a decorator: d wraps a function fn.
    @author Peter Norvig in Udacity CS212"""
    def _d(fn):
        return update_wrapper(d(fn), fn) # for example when memo (d) wraps search (fn)
    update_wrapper(_d, d) # for example when decorator (_d) wraps memo (d)
    return _d

@decorator # memo = decorator(memo)
def memo(f):
    """Decorator that caches return value for each call to f(args).
    Then when called again with same args, we can just look it up.
    @author Peter Norvig in Udacity CS212"""
    cache = {}
    def _f(*args):
        try:
            return cache[args] # Cache Hit!
        except KeyError:
            result = f(*args)
            cache[args] = result
            return result
        except TypeError:
            # some element of args can't be a dict key (i.e. unhashable)
            return f(*args)
    _f.cache = cache
    return _f
assert memo.__name__ == 'memo' # not '_d' returned from decorator

@decorator
def trace(f):
    # @author Peter Norvig in Udacity CS212
    indent = '   '
    def _f(*args):
        signature = '%s(%s)' % (f.__name__, ', '.join(map(repr, args)))
        print '%s--> %s' % (trace.level*indent, signature)
        trace.level += 1
        try:
            result = f(*args)
            print '%s<-- %s == %s' % ((trace.level-1)*indent,
                                      signature, result)
        finally:
            trace.level -= 1
        return result
    trace.level = 0
    return _f

def timed_call(fn, *args):
    t0 = clock()
    result = fn(*args)
    t1 = clock()
    return t1-t0, result

#### SEARCH TREE ####

def breadth_first_search(goal, predecessors):
    tree = OrderedDict({goal : (None, None)}) # {board : (action, next_board)} pairs
    fringe = deque([goal]) # FIFO queue

    while fringe:
        board = fringe.popleft()
        for (action, previous_board) in predecessors(board):
            if previous_board not in tree:
                tree[previous_board] = (action, board)
                fringe.append(previous_board)

    return tree
BFS = breadth_first_search

FAIL = 'Fail'

def shortest_path(board, tree_name):
    path = [board] # path := [board, action, board, ...]
    if board in TREES[tree_name]:
        action, next = TREES[tree_name][board]
    else:
        return FAIL # Goal (root of tree) not reachable from given board

    while next:
        path += [action, next]
        action, next = TREES[tree_name][next]
    return path

#@trace
@memo # recursive_shortest_path = memo(recursive_shortest_path)
def recursive_shortest_path(board, tree_name):
    if board not in TREES[tree_name]: return FAIL

    action, next = TREES[tree_name][board]
    if next is None:
        return [board]
    else:
        return [board, action] + recursive_shortest_path(next, tree_name)
assert recursive_shortest_path.__name__ == 'recursive_shortest_path' # not 'memo' or '_f' returned from memo

def shortest_paths(tree_name, shortest_path_fn):
    # The recursive, shortest path function is fastest.  Use it!
    # sorted based on insertion into tree (OrderedDict)
    return [shortest_path_fn(board, tree_name) for board in TREES[tree_name].keys()]

def shortest_path_astar(start_board, successors_fn, heuristic_fn, is_goal):
    pass # TODO

def path_actions(path):
    return path[1::2]

def path_boards(path):
    return path[0::2]

def group_paths(sorted_paths):
    # For example, group_paths(paths)[n] returns all paths n number of moves away from goal.
    # group_paths(path)[0] returns [[goal]], which is 0 moves away from itself.
    return map(lambda (n, paths): list(paths), groupby(sorted_paths, key=len))

def group_boards(path_groups):
    """Return all boards n number of moves away from goal.  n is the index into the returned list."""
    return [map(lambda p: p[0], group) for group in path_groups]

def average_n_moves(paths):
    """Return average number of moves to solve puzzle."""
    return sum(map(len, map(path_actions, paths))) / float(len(paths))

#### PUZZLE ####

def Board(text):
    # For example, Board('01 23') or Board('123 456 780')
    rows = text.split()
    N = len(rows)
    rows = [BORDER*N] + rows + [BORDER*N]
    return ''.join(BORDER + row + BORDER for row in rows)

BORDER = '|'

def size(board): return int(len(board)**0.5)

def display(board):
    N = size(board)
    return '\n'.join(board[i:i+N] for i in range(0, N*N, N))

def predecessors(board):
    blank = board.index('0')
    N = size(board)
    valid_move = lambda ((action, pos)): board[pos] is not BORDER
    moves = filter(valid_move, [('right', blank+1), ('left', blank-1), ('down', blank+N), ('up', blank-N)])

    def new_board(pos):
        b = list(board)
        b[blank], b[pos] = b[pos], b[blank]
        return ''.join(b)

    return ((a, new_board(pos)) for (a, pos) in moves)

def display_game(path):
    if path is FAIL:
        return 'Goal not reachable from starting board.'

    s = 'Start:' + '\n' + display(path[0])
    if len(path) > 1:
        s += '\n\n' + '\n\n'.join('\n'.join(('Move: '+path[i]+'\n', display(path[i+1]))) for i in range(1, len(path) - 1, 2))
    s += '\n\n' + 'Goal!'
    return s

TREES = dict() # Lookup table, in order to optimize recursive, shortest path function

def print_moves(tree_name, board):
    print 'Current board:'
    print display(board)
    print 'Shortest path: ' + str(len(path_actions(shortest_path(board, tree_name)))) + ' moves.' + '\n'

    print 'Next boards:'
    for (action, next) in predecessors(board):
        print display(next)
        print 'Action: ' + action
        print 'Shortest path: ' + str(len(path_actions(shortest_path(next, tree_name)))) + ' moves.' + '\n'

#### TESTS ####

def test():
    goal = Board('01 23')
    assert goal == '|||||01||23|||||'
    assert display(goal) == """
||||
|01|
|23|
||||
""".strip()
    assert size(goal) == 4
    assert sorted(list(predecessors(goal))) == sorted([('down', Board('21 03')), ('right', Board('10 23'))])

    TREES['tree'] = BFS(goal, predecessors)
    assert len(TREES['tree']) == 12 # 4!/2
    assert Board('12 30') not in TREES['tree']

    TREES['other_tree'] = BFS(Board('12 30'), predecessors)
    assert len(TREES['other_tree']) == 12
    assert set(TREES['tree'].keys()) & set(TREES['other_tree'].keys()) == set() # Sets disjoint
    assert display_game(shortest_path(Board('12 30'), 'tree')) == 'Goal not reachable from starting board.'

    assert shortest_path(Board('21 03'), 'tree') == [Board('21 03'), 'down', goal]
    assert shortest_path(Board('10 23'), 'tree') == [Board('10 23'), 'right', goal]

    path = shortest_path(Board('20 31'), 'tree')
    assert path == [Board('20 31'), 'up', Board('21 30'), 'right', Board('21 03'), 'down', goal]
    assert path_actions(path) == ['up', 'right', 'down']
    assert path_boards(path) == [Board('20 31'), Board('21 30'), Board('21 03'), goal]
    assert display_game(path) == """
Start:
||||
|20|
|31|
||||

Move: up

||||
|21|
|30|
||||

Move: right

||||
|21|
|03|
||||

Move: down

||||
|01|
|23|
||||

Goal!
""".strip()

    longest = shortest_path(Board('32 10'), 'tree')
    assert path_actions(longest) == ['down', 'right', 'up', 'left', 'down', 'right']
    paths = shortest_paths('tree', shortest_path) # sorted by length
    assert average_n_moves(paths) == 3.0
    assert longest == paths[-1]
    assert len(paths) == 12 # 4!/2

    assert group_paths(paths)[0] == [ [goal] ]
    assert group_paths(paths)[-1] == [longest]

    boards = group_boards(group_paths(paths))
    assert sum(map(len, boards)) == 12 # 4!/2
    assert len(boards) == 7 # 0-6 moves away from goal
    assert boards[0] == [goal]
    assert sorted(boards[1]) == sorted([Board('10 23'), Board('21 03')])
    assert boards[6] == [Board('32 10')]

    assert recursive_shortest_path(Board('32 10'), 'tree') == longest
    assert recursive_shortest_path(None, 'tree') == FAIL
    assert recursive_shortest_path(Board('12 30'), 'tree') == FAIL

    def test_recursion(tree_name):
        time, result = timed_call(shortest_paths, tree_name, shortest_path)
        recursive_time, recursive_result = timed_call(shortest_paths, tree_name, recursive_shortest_path)
        assert result == recursive_result
        print [recursive_time, time]
        assert recursive_time < time
        return recursive_result

    test_recursion('tree')
    TREES['eight_tree'] = BFS(Board('012 345 678'), predecessors)
    eight_paths = test_recursion('eight_tree')
    eight_groups = group_paths(eight_paths)
    eight_boards = group_boards(eight_groups)
    assert len(eight_boards) == 32 # 0-31 moves away from goal
    assert int(average_n_moves(eight_paths)) == 21

    million_bytes = 1000000
    n_boards = len(TREES['eight_tree'])
    assert n_boards == 181440 # 9!/2
    tree_size = getsizeof(TREES['eight_tree'])
    assert tree_size/million_bytes == 12 # 12 MB
    assert tree_size/n_boards == 69 # node size of 69 bytes
    # Guessed 55 bytes for each {board : (action, next_board)} pair in tree

    return 'test passes'

if __name__ == '__main__':
    #print test()
    TREES['eight_tree'] = BFS(Board('012 345 678'), predecessors)
    #TREES['other_eight_tree'] = BFS(Board('123 456 780'), predecessors)
    #eight_paths = shortest_paths('eight_tree', recursive_shortest_path)
    #eight_groups = group_paths(eight_paths)
    #eight_boards = group_boards(eight_groups)
    #print path_actions(shortest_path(Board('134 025 678'), 'eight_tree'))
    #b = Board('724 506 831')
    b = Board('532 706 481')
    print_moves('eight_tree', b)
    #print_moves('eight_tree', Board('134 025 678'))
    #print shortest_path(Board('134 025 678'), 'eight_tree')
    #print shortest_path(Board('134 025 678'), 'other_eight_tree')

    #other_start = shortest_path(Board('123 456 780'), 'eight_tree')
    #print '\nOther start, length: ' + str(len(other_start))
    #print other_start

    #other_goal = shortest_path(Board('012 345 678'), 'other_eight_tree')
    #print '\nOther goal, length: ' + str(len(other_goal))
    #print other_goal



