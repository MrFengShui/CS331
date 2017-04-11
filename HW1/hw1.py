import sys

class State():
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def set_node_list(self, node):
        self.node = node

    def get_node_list(self):
        return self.node

    def check_boat_location(self):
        return 'L' if self.lhs['B'] == 1 and self.rhs['B'] == 0 else 'R'

    def is_initial_state(self):
        return self.lhs['M'] == 0 and self.lhs['C'] == 0 and self.lhs['B'] == 0

    def is_goal(self, goal):
        lflag = self.lhs['M'] == goal.lhs['M'] and self.lhs['C'] == goal.lhs['C'] and self.lhs['B'] == goal.lhs['B']
        rflag = self.rhs['M'] == goal.rhs['M'] and self.rhs['C'] == goal.rhs['C']
        return lflag and rflag and self.rhs['B'] == goal.rhs['B']

    def is_valid(self):
        mflag = self.lhs['M'] >= 0 and self.rhs['M'] >= 0
        cflag = self.lhs['C'] >= 0 and self.rhs['C'] >= 0
        lflag = self.lhs['M'] == 0 or self.lhs['M'] >= self.lhs['C']
        rflag = self.rhs['M'] == 0 or self.rhs['M'] >= self.rhs['C']
        return mflag and cflag and lflag and rflag

    def print_state(self):
        print 'Left:', self. lhs, 'Right:', self. rhs

def func_init_move(state, which = None):
    lhs, rhs = state.lhs.copy(), state.rhs.copy()

    if which == None:
        lhs['M'] += 1
        lhs['C'] += 1
        lhs['B'] = 1
        rhs['M'] -= 1
        rhs['C'] -= 1
        rhs['B'] = 0
    else:
        lhs[which] += 2
        lhs['B'] = 1
        rhs[which] -= 2
        rhs['B'] = 0

    return State(lhs, rhs)

def func_left_right(state, which):
    lhs, rhs = state.lhs.copy(), state.rhs.copy()
    lhs[which] -= 1
    lhs['B'] = 0
    rhs[which] += 1
    rhs['B'] = 1
    return State(lhs, rhs)

def func_right_left(state, which):
    lhs, rhs = state.lhs.copy(), state.rhs.copy()
    lhs[which] += 1
    lhs['B'] = 1
    rhs[which] -= 1
    rhs['B'] = 0
    return State(lhs, rhs)

def func_move_state(state):
    state_list = []

    if state.is_initial_state():
        new_state = func_init_move(state, 'M')
        new_state.set_node_list([])

        if new_state.is_valid():
            state_list.append(new_state)

        new_state = func_init_move(state)
        new_state.set_node_list([])

        if new_state.is_valid():
            state_list.append(new_state)

        new_state = func_init_move(state, 'C')
        new_state.set_node_list([])

        if new_state.is_valid():
            state_list.append(new_state)
    else:
        if state.check_boat_location() == 'L':
            new_state = func_left_right(state, 'C')
            new_state.set_node_list([])

            if new_state.is_valid():
                state_list.append(new_state)

            new_state = func_left_right(state, 'M')
            new_state.set_node_list([])

            if new_state.is_valid():
                state_list.append(new_state)

        if state.check_boat_location() == 'R':
            new_state = func_right_left(state, 'C')
            new_state.set_node_list([])

            if new_state.is_valid():
                state_list.append(new_state)

            new_state = func_right_left(state, 'M')
            new_state.set_node_list([])

            if new_state.is_valid():
                state_list.append(new_state)

    state.set_node_list(state_list)
    return state

def func_create_path(state, goal, i = 0):
    print ' ' * i,
    state.print_state()
    state_list = state.get_node_list()
    i += 1
    for state_item in state_list:
        new_state = func_move_state(state_item)
        func_create_path(new_state, goal, i)

def func_read_file(name):
    fp = open(name, 'r');
    lines = fp.readlines();
    fp.close();
    lhs = lines[0].rstrip().split(',')
    rhs = lines[1].rstrip().split(',')
    return {'M': int(lhs[0]), 'C': int(lhs[1]), 'B': int(lhs[2])}, {'M': int(rhs[0]), 'C': int(rhs[1]), 'B': int(rhs[2])}

def func_write_file(name, result):
    fp = open(name, 'w+')
    fp.write('\n'.join(result))
    fp.close()

def func_print_states(state, i = 0):
    print '    ' * i,
    state.print_state()
    nodes = state.get_node_list()
    i += 1
    for node in nodes:
        func_print_states(node, i)

if __name__ == '__main__':
    params = sys.argv
    start_file = params[1]
    goal_file = params[2]
    mode = params[3]
    output = params[4]
    lhs, rhs = func_read_file(start_file)
    init_state = State(lhs, rhs)
    lhs, rhs = func_read_file(goal_file)
    goal_state = State(lhs, rhs)
    init_state = func_move_state(init_state)
    func_print_states(init_state)
    print
    func_create_path(init_state, goal_state)
    # func_print_states(init_state)
    # func_write_file(output, ['(3,3,left,0,0)', '(2,3,left,1,0)', '(0,3,right,3,0)', '(1,3,left,2,0)', '(1,1,right,2,2)', '(2,2,left,1,1)', '(2,0,right,1,3)', '(3,0,left,0,3)', '(1,0,right,2,3)', '(1,1,left,2,2)', '(0,0,right,3,3)', '(1,3,right,2,0)'])
