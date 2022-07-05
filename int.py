import argparse, re, sys

from splay import Tree

parser = argparse.ArgumentParser(description="Interpreter for Splaytime", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-w", "--show-warnings", action="store_true", help="Show warnings")
parser.add_argument("-v", "--verbose", action="store_true", help="For debugging; outputs every instruction that is done.")
parser.add_argument("-d", "--display-tree", action="store_true", help="For debugging; outputs the splay tree at the end.")
parser.add_argument("-i", "--input", help="Uses a file as an input source instead of stdin")
parser.add_argument("-o", "--output", help="Outputs to a file instead of stdout")
parser.add_argument("file")
args = parser.parse_args()

I = open(args.file, "r")
inst = re.sub(r"\s+", "", "".join(I.readlines()), flags=re.UNICODE)

if args.input != None:
	I = open(args.input, "r")

if args.output != None:
	O = open(args.output, "w+")

if len(inst) == 0 and args.show_warnings:
	sys.stderr.write("Instruction file is empty.\n")

t = Tree().insert(0)

pc = 0
while pc < len(inst):
	char = inst[pc]

	if char == '{': # insert
		s, key, value, comma, neg = pc, 0, 0, 0, 1
		pc += 1
		if pc < len(inst): # edge case: entire instruction string is just '{'
			char = inst[pc]
			while (char.isdigit() or char in '|[-'):
				if char == '[': # read from node
					if (pc != s+1 and not comma) or (pc != comma+1 and comma):
						sys.stderr.write("Invalid indexing at character %i\n"%pc)
						sys.exit(1)

					n, addr = 1, 0
					pc += 1; char = inst[pc]
					if char == '-' and pc+1 < len(inst) and inst[pc+1].isdigit():
						n = -1; pc += 1; char = inst[pc]
					while char.isdigit():
						addr = addr * 10 + int(char)

						pc += 1
						if pc >= len(inst): break
						char = inst[pc]

					addr *= n
					data = t.search(addr).data
					if data == None:
						sys.stderr.write("No node with address %i\n"%addr)
						sys.exit(1)

					if not comma:
						key = data
					else:
						value = data
						break
				elif char.isdigit():
					if not comma:
						key = key*10 + int(char)
					else:
						value = value*10 + int(char)
				elif char == '|':
					if comma:
						sys.stderr.write("Second '|' found at character %i, one (1) expected\n"%pc)
						sys.exit(1)
					comma = pc
				elif char == '-':
					if pc+1 < len(inst) and inst[pc+1].isdigit(): neg *= -1
					else: break

				pc += 1
				if pc >= len(inst): break
				char = inst[pc]

		value += 1 if char == '+' else (-1 if char == '-' else 0)
		value *= neg
		t.insert((key, value))
		if args.verbose: print(f"Inserted ({key}, {value})")
		pc -= 0 if char in '-+' else 1; char = inst[pc] # stops on the character after the numeral, next cycle would skip it
	elif char == '.': # print ascii
		if args.output == None:
			sys.stdout.write(chr(t.root.data))
			if args.verbose: print(f"\nWrote {chr(t.root.data)}")
		else:
			O.write(chr(t.root.data))
			if args.verbose: print(f"Wrote {chr(t.root.data)}")
	elif char == ',': # input ascii value
		t.root.data = (ord(c) if len(c := I.read(1)) else 0) if args.input else ord(sys.stdin.read(1))
		if args.verbose: print(f"Input: {t.root.data}")
	elif char == "@": # jump if zero
		if t.root.data == 0:
			s, addr = pc, 0
			pc += 1
			if pc < len(inst): # edge case: entire instruction string is just '@'
				char = inst[pc]
				while (char.isdigit() or char == '['):
					if char == '[': # read from node
						if pc != s+1:
							sys.stderr.write("Invalid indexing at character %i\n"%pc)
							sys.exit(1)

						saddr = 0
						pc += 1; char = inst[pc]
						while char.isdigit():
							saddr = saddr * 10 + int(char)

							pc += 1
							if pc >= len(inst): break
							char = inst[pc]

						addr = t.search(saddr).data
						break

					addr = addr * 10 + int(char)

					pc += 1
					if pc >= len(inst): break
					char = inst[pc]

			pc -= 1 # stops on the character after the numeral, next cycle would skip it

			if addr >= len(inst):
				break
			pc = addr-1
			if args.verbose: print(f"Jumped to {addr}")
		elif args.verbose: print("NEQ0")
	elif char == "$": # jump node
		s, addr = pc, 0
		pc += 1; char = inst[pc]
		if pc < len(inst): # edge case: entire instruction string is just '$'
			while (char.isdigit() or char == '['):
				if char == '[': # read from node
					if pc != s+1:
						sys.stderr.write("Invalid indexing at character %i\n"%pc)
						sys.exit(1)

					saddr = 0
					pc += 1; char = inst[pc]
					while char.isdigit():
						saddr = saddr * 10 + int(char)

						pc += 1
						if pc >= len(inst): break
						char = inst[pc]

					addr = t.search(saddr).data
					break

				addr = addr * 10 + int(char)

				pc += 1
				if pc >= len(inst): break
				char = inst[pc]

			pc -= 1 # stops on the character after the numeral, next cycle would skip it

		if t.search(addr) == None and args.show_warnings:
			sys.stderr.write("No node with address %i\n"%addr)
		if args.verbose: print(f"Shifted to {addr}")

	pc += 1

print()
if args.display_tree: t.print()