import sys, time, operator

class State():
	def __init__(self, lhs, rhs, states = [], value = 0):
		self.lhs = lhs
		self.rhs = rhs
		self.states = states
		self.value = value

	def is_initial(self):
		return self.lhs['C'] == 0 and self.lhs['M'] == 0 and self.lhs['B'] == 0

	def is_valid(self):
		return self.lhs['C'] >= 0 and self.rhs['C'] >= 0 and \
			   self.lhs['M'] >= 0 and self.rhs['M'] >= 0 and \
			   (self.lhs['M'] >= self.lhs['C'] or self.lhs['M'] == 0) and \
			   (self.rhs['M'] >= self.rhs['C'] or self.rhs['M'] == 0)

	def is_goal(self, goal):
		return self.rhs['C'] == goal.fetch_rhs()['C'] and \
			   self.rhs['B'] == goal.fetch_rhs()['B'] and \
			   self.rhs['M'] == goal.fetch_rhs()['M']

	def on_left(self):
		return self.lhs['B'] == 1 and self.rhs['B'] == 0

	def on_right(self):
		return self.lhs['B'] == 0 and self.rhs['B'] == 1

	def store_states(self, states):
		self.states = states

	def load_states(self):
		return self.states

	def fetch_lhs(self):
		return self.lhs

	def fetch_rhs(self):
		return self.rhs

def func_move_one(lhs, rhs, which, count, flag):
	if flag:
		lhs[which] += count
		lhs['B'] = 1
		rhs[which] -= count
		rhs['B'] = 0
		return State(lhs, rhs)
	else:
		lhs[which] -= count
		lhs['B'] = 0
		rhs[which] += count
		rhs['B'] = 1
		return State(lhs, rhs)

def func_move_two(lhs, rhs, flag):
	if flag:
		lhs['C'] += 1
		lhs['B'] = 1
		lhs['M'] += 1
		rhs['C'] -= 1
		rhs['B'] = 0
		rhs['M'] -= 1
		return State(lhs, rhs)
	else:
		lhs['C'] -= 1
		lhs['B'] = 0
		lhs['M'] -= 1
		rhs['C'] += 1
		rhs['B'] = 1
		rhs['M'] += 1
		return State(lhs, rhs)

def func_build_successor(state):
	states, flag = [], state.on_right()

	lhs, rhs = state.fetch_lhs().copy(), state.fetch_rhs().copy()
	new_state = func_move_one(lhs, rhs, 'C', 2, flag)
	if new_state.is_valid():
		states.append(new_state)

	lhs, rhs = state.fetch_lhs().copy(), state.fetch_rhs().copy()
	new_state = func_move_one(lhs, rhs, 'C', 1, flag)
	if new_state.is_valid():
		states.append(new_state)

	lhs, rhs = state.fetch_lhs().copy(), state.fetch_rhs().copy()
	new_state = func_move_two(lhs, rhs, flag)
	if new_state.is_valid():
		states.append(new_state)

	lhs, rhs = state.fetch_lhs().copy(), state.fetch_rhs().copy()
	new_state = func_move_one(lhs, rhs, 'M', 1, flag)
	if new_state.is_valid():
		states.append(new_state)

	lhs, rhs = state.fetch_lhs().copy(), state.fetch_rhs().copy()
	new_state = func_move_one(lhs, rhs, 'M', 2, flag)
	if new_state.is_valid():
		states.append(new_state)

	return states

def func_state_exist(target, array):
	for item in array:
		if cmp(target.lhs, item.lhs) == 0 and cmp(target.rhs, item.rhs) == 0:
			return True

	return False

def func_dfs_search(state, goal):
	state_stack, state_explore = [], []
	state_stack.append(state)

	while state_stack:
		tmp_state = state_stack.pop()
		if tmp_state.is_goal(goal):
			return tmp_state
		successor = func_build_successor(tmp_state)
		tmp_state.store_states(successor)
		if not func_state_exist(tmp_state, state_explore):
			state_explore.append(tmp_state)
			for item in successor:
				if (not func_state_exist(item, state_explore)) and (not item.is_initial()):
					state_stack.append(item)

	return None

def func_bfs_search(state, goal):
	state_queue, state_explore = [], []
	state_queue.append(state)

	while state_queue:
		tmp_state = state_queue.pop(0)
		if tmp_state.is_goal(goal):
			return tmp_state
		successor = func_build_successor(tmp_state)
		tmp_state.store_states(successor)
		if not func_state_exist(tmp_state, state_explore):
			state_explore.append(tmp_state)
			for item in successor:
				if (not func_state_exist(item, state_explore)) and (not item.is_initial()):
					state_queue.append(item)

	return None

def func_dls_search(state, goal, depth, state_explore = []):
	state_explore.append(state)
	if state.is_goal(goal) and depth == 0:
		return state
	else:
		flag, successor = False, func_build_successor(state)
		state.store_states(successor)
		for item in successor:
			if not func_state_exist(item, state_explore):
				found = func_dls_search(item, goal, depth - 1, state_explore)
				if found != None:
					return found

		return None


def func_iddfs_search(state, goal, depth = 0):
	while True:
		found = func_dls_search(state, goal, depth)
		if found != False:
			return found
		depth += 1

def func_calc_h(state, goal):
	diff_c = goal.fetch_lhs()['C'] - state.fetch_lhs()['C']
	diff_m = goal.fetch_rhs()['M'] - state.fetch_rhs()['M']
	return diff_c + diff_m

def func_calc_c(state, goal, length = 0):
	for item in state.load_states():
		if not item.is_goal(goal):
			func_calc_c(item, goal, length + 1)
	return length

def func_astar_search(state, goal):
	state_queue, state_explore, state.value = [], [], func_calc_h(state, goal)
	state_queue.append(state)

	while len(state_queue) > 0:
		tmp_state = state_queue.pop(0)
		if tmp_state.is_goal(goal):
			return tmp_state
		successor = func_build_successor(tmp_state)
		tmp_state.store_states(successor)
		if not func_state_exist(tmp_state, state_explore):
			state_explore.append(tmp_state)
			for item in successor:
				if (not func_state_exist(item, state_queue)) and (not func_state_exist(item, state_explore)):
					item.value = func_calc_c(item, state) + func_calc_h(item, state)
					state_queue.append(item)
					state_queue.sort(key = operator.attrgetter('value'))

	return None

def func_print_state(state):
	print 'LHS:', state.fetch_lhs(), '<--->', 'RHS:', state.fetch_rhs()
	for item in state.load_states():
		print 'LHS:', item.fetch_lhs(), '<--->', 'RHS:', item.fetch_rhs()
	print

def func_print_string(tree, result, goal, item = ''):
	lhs, rhs = tree.fetch_lhs(), tree.fetch_rhs()
	str_lhs = '(' + ','.join([str(value) for value in lhs.values()]) + ')'
	str_rhs = '(' + ','.join([str(value) for value in rhs.values()]) + ')'
	item += str_lhs + ' ' + str_rhs + '-->'

	if cmp(lhs, goal.fetch_lhs()) == 0 and cmp(rhs, goal.fetch_rhs()) == 0:
		temp = item[:-3].split('-->')
		result.append(temp)

	for state in tree.load_states():
		func_print_string(state, result, goal, item)

def func_print_tree(tree, level = 0):
	lhs = '(' + ','.join([str(value) for value in tree.fetch_lhs().values()]) + ')'
	rhs = '(' + ','.join([str(value) for value in tree.fetch_rhs().values()]) + ')'
	print '+' * level + lhs, '<--->', rhs
	level += 1
	for state in tree.load_states():
		func_print_tree(state, level)

def func_read_file(name):
	fp = open(name, 'r');
	lines = fp.readlines();
	fp.close();
	lhs = lines[0].rstrip().split(',')
	rhs = lines[1].rstrip().split(',')
	return {'M': int(lhs[0]), 'C': int(lhs[1]), 'B': int(lhs[2])}, {'M': int(rhs[0]), 'C': int(rhs[1]), 'B': int(rhs[2])}

def func_write_file(name, results):
	fp = open(name, 'w+')
	fp.write('(C,B,M) (C,B,M)\n')
	i = 1
	for result in results:
		head = '* Solution-[' + str(i) + '] *\n'
		fp.write(head + '\n'.join(result) + '\n')
		i += 1
	fp.close()

if __name__ == '__main__':
	sys.setrecursionlimit(999999999)
	params = sys.argv
	start_file, goal_file = params[1], params[2]
	mode, output = params[3], params[4]
	start_lhs, start_rhs = func_read_file(start_file)
	goal_lhs, goal_rhs = func_read_file(goal_file)
	goal_state, init_state = State(goal_lhs, goal_rhs), State(start_lhs, start_rhs)

	if mode == 'bfs':
		func_bfs_search(init_state, goal_state)

	if mode == 'dfs':
		func_dfs_search(init_state, goal_state)

	if mode == 'iddfs':
		func_iddfs_search(init_state, goal_state)

	if mode == 'astar':
		func_astar_search(init_state, goal_state)

	results = []
	func_print_string(init_state, results, goal_state)
	func_write_file(output, results)
