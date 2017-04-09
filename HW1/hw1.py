import sys

class State():
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.parent = None

    def func_fetch_boat(self):
        return 'L' if self.lhs['B'] == 1 and self.rhs['B'] == 0 else 'R'
        
    def func_check_initial(self):
        return self.lhs['M'] == 0 and self.lhs['C'] == 0 and self.lhs['B'] == 0
        
    def func_check_goal(self):
        return self.rhs['M'] == 0 and self.rhs['C'] == 0

    def func_check_valid(self):
        mflag = self.lhs['M'] >= 0 and self.rhs['M'] >= 0
        cflag = self.lhs['C'] >= 0 and self.rhs['C'] >= 0
        lflag = self.lhs['M'] == 0 or self.lhs['M'] >= self.lhs['C']
        rflag = self.rhs['M'] == 0 or self.rhs['M'] >= self.rhs['C']
        return mflag and cflag and lflag and rflag

    def func_print_state(self):
        print 'Left:', self. lhs, 'Right:', self. rhs

def func_init_move(state, which = None):
    lhs, rhs = state.lhs.copy(), state.rhs.copy()
    
    if which == None:
        lhs['M'] += 1
        lhs['C'] += 1
        lhs['B'] = 1
        lhs['M'] -= 1
        rhs['C'] -= 1
        rhs['B'] = 0
    else:
        lhs[which] += 2
        lhs['B'] = 1
        rhs[which] -= 2
        rhs['B'] = 0
        
    return State(lhs, rhs)

def func_move_state(init_state):
    print '**** ', init_state.lhs, '      ', init_state.rhs, ' ****'
    state_list = []
    
    if init_state.func_check_initial():
        state_list.append(func_init_move(init_state, 'M'))       
        state_list.append(func_init_move(init_state))        
        state_list.append(func_init_move(init_state, 'C'))
    else:
        print 'undefined'
        
    return state_list
        
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

if __name__ == '__main__':
    params = sys.argv
    print params
    start_file = params[1]
    goal_file = params[2]
    mode = params[3]
    output = params[4]
    lhs, rhs = func_read_file(start_file)
    init_state = State(lhs, rhs)
    states = func_move_state(init_state)
    print [state.func_fetch_boat() for state in states]
    # func_write_file(output, ['(3,3,left,0,0)', '(2,3,left,1,0)', '(0,3,right,3,0)', '(1,3,left,2,0)', '(1,1,right,2,2)', '(2,2,left,1,1)', '(2,0,right,1,3)', '(3,0,left,0,3)', '(1,0,right,2,3)', '(1,1,left,2,2)', '(0,0,right,3,3)', '(1,3,right,2,0)'])
