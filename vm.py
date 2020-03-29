from random import randint
from copy import deepcopy

# Instruction numbers
NUMINSTR = 4
PUSH, ADD, PRINT, JUMP = range(NUMINSTR)

CELL_SIZE = 256
CELL_MAX = CELL_SIZE-1
CELL_MIN = 0

# indexes of the state components
STEPS, IP, CODE = range(3)

def execute(output, state):

	# Runtime stack for data manipulation
	stack = []

	while True:

		# Uncomment this to see the program state and stack each step
		#print("STATE:", state)
		#print("STACK:", stack)

		steps = state[STEPS]
		ip = state[IP]
		code = state[CODE]

		# We are out of steps, stop the process
		if steps <= 0:
			break

		# No instructions are left, stop the process
		if ip >= len(code):
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
		elif instruction == PRINT:
			# Pop the topmost element from the stack and print it
			#print("OUTPUT:", stack.pop(-1))
			if len(stack) >= 1:
				output(stack.pop(-1))
		elif instruction == JUMP:
			if len(stack) >= 1:
				state[IP] = stack.pop(-1)

		# Move the instruction pointer one step forward to point to the next instruction
		state[IP] += 1

		# Reduce the number of remaining steps by one
		state[STEPS] -= 1

		# Print a newline after each iteration
		#print("")

STARTGAS = 256

def code_to_state(code):
	return [STARTGAS, 0, code]

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
	code = deepcopy(state[CODE])
	for i in range(len(code)//10):
		random_index = randint(0, len(code)-1)
		code[random_index] = random_instruction()
	# Replenish, reset
	return code_to_state(code)

if __name__ == "__main__":
	# full runtime state of a process
	# number of remaining steps, instruction pointer, instruction list
	state_example = [100, 0, [[PUSH, 1], [PUSH, 2], [ADD], [PRINT], [JUMP]]]

	execute(state_example)
