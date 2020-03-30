from random import randint, choice
from copy import deepcopy

W = H = 256

# Instruction numbers
NUMINSTR = 10
PUSH, ADD, PRINT, JUMP, SUB, I_IP, I_LEFT, I_RIGHT, I_MOVE, I_RANDOM = range(NUMINSTR)

CELL_SIZE = 256
CELL_MAX = CELL_SIZE-1
CELL_MIN = 0

# indexes of the state components
NUMFIELDS = 6
F_GAS, F_IP, F_X, F_Y, F_R, F_CODE = range(NUMFIELDS)

MOVES = [[0,1], [-1,0], [0,-1], [1,0]]

STARTGAS = 1024

def execute(output, state):

	# Runtime stack for data manipulation
	stack = []

	start_steps = state[F_GAS]

	while True:

		# Assuming no refills
		steps_done = start_steps - state[F_GAS]

		# pseudo-gravity
		"""
		if steps_done % 20 == 0:
			if state[F_Y] < H-1:
				state[F_Y] = (state[F_Y]+1)%H
		"""

		# Uncomment this to see the program state and stack each step
		#print("STATE:", state)
		#print("STACK:", stack)

		steps = state[F_GAS]
		ip = state[F_IP]
		code = state[F_CODE]

		# We are out of steps, stop the process
		if steps <= 0:
			break

		# No instructions are left, stop the process
		if ip >= len(code) or ip < 0:
			break

		if len(code[ip]) == 2:
			# Some instructions have an argument, unpack that as well
			instruction, argument = code[ip]
		else:
			instruction = code[ip][0]
			argument = None


		if instruction == PUSH:
			# Push the argument to the top of the stack
			stack.append(argument)
		elif instruction == ADD:
			# Pop the two topmost elements from the stack, add them and push the result back on the stack
			if len(stack) >= 2:
				stack.append(stack.pop(-1) + stack.pop(-1))
		elif instruction == SUB:
			# Pop the two topmost elements from the stack, subtract them and push the result back on the stack
			if len(stack) >= 2:
				stack.append(stack.pop(-1) - stack.pop(-1))
		elif instruction == PRINT:
			# Pop the topmost element from the stack and print it
			#print("OUTPUT:", stack.pop(-1))
			if len(stack) >= 1:
				output(state[F_X], state[F_Y], stack.pop(-1))
		elif instruction == JUMP:
			if len(stack) >= 1:
				state[F_IP] = stack.pop(-1)
		elif instruction == I_IP:
			stack.append(ip)
		elif instruction == I_LEFT:
			state[F_R] = (state[F_R]-1)%4
		elif instruction == I_RIGHT:
			state[F_R] = (state[F_R]+1)%4
		elif instruction == I_MOVE:
			move = MOVES[state[F_R]]
			state[F_X] = (state[F_X] + move[0])%W
			newy = (state[F_Y] + move[1])
			if newy < H:
				state[F_Y] = newy%H
		elif instruction == I_RANDOM:
			stack.append(randint(0,255))
		# Move the instruction pointer one step forward to point to the next instruction
		state[F_IP] += 1

		# Reduce the number of remaining steps by one
		state[F_GAS] -= 1

		# Print a newline after each iteration
		#print("")

def code_to_state(code):
	return [STARTGAS, 0, randint(0,W-1), randint(0,H-1), 0, code]

def random_instruction():
	instr = randint(0, NUMINSTR-1)
	if instr == PUSH:
		block = [PUSH, randint(0,CELL_MAX)]
	else:
		block = [instr]
	return block

def generate_random():
	code = []
	for i in range(100):
		code.append(random_instruction())

	return code_to_state(code)

def mutate(state):
	code = deepcopy(state[F_CODE])
	for i in range(len(code)//10):
		random_index = randint(0, len(code)-1)
		code[random_index] = random_instruction()
	# Replenish, reset
	return code_to_state(code)

def splice(state1, state2):
	code1 = deepcopy(state1[F_CODE])
	code2 = deepcopy(state2[F_CODE])
	index = randint(0, min(len(code1), len(code2))-1)
	first, second = (code1, code2) if randint(0,1) == 0 else (code2, code1)
	code = first[:index] + second[index:]
	return code_to_state(code)

if __name__ == "__main__":
	# full runtime state of a process
	# number of remaining steps, instruction pointer, instruction list
	state_example = [100, 0, 0, 0, 0, [[PUSH, 1], [PUSH, 2], [ADD], [PRINT], [JUMP]]]

	execute(state_example)
