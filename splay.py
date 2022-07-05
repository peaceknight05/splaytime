import sys

class Node():
	def __init__(self, key, data=0):
		self.key = key
		self.data = data
		self.left = None
		self.right = None
		self.parent = None

class Tree():
	def __init__(self):
		self.root = None

	def printr(self, currPtr, indent, last):
		# sys.stdout.write the tree structure on the screen
		if currPtr != None:
			sys.stdout.write(indent)
			if last:
				sys.stdout.write("R----")
				indent += "     "
			else:
				sys.stdout.write("L----")
				indent += "|    "

			print(f"{currPtr.key}|{currPtr.data}")

			self.printr(currPtr.left, indent, False)
			self.printr(currPtr.right, indent, True)

	def searchr(self, node, key):
		if node == None or key == node.key:
			return node

		if key < node.key:
			return self.searchr(node.left, key)
		return self.searchr(node.right, key)

	def minimum(self, node):
		while node.left != None:
			node = node.left
		return node

	def maximum(self, node):
		while node.right != None:
			node = node.right
		return node

	def rotr(self, x):
		y = x.left
		x.left = y.right
		if y.right != None:
			y.right.parent = x

		y.parent = x.parent
		if x.parent == None:
			self.root = y
		elif x == x.parent.right:
			x.parent.right = y
		else:
			x.parent.left = y

		y.right = x
		x.parent = y

	def rotl(self, x):
		y = x.right
		x.right = y.left
		if y.left != None:
			y.left.parent = x

		y.parent = x.parent
		if x.parent == None:
			self.root = y
		elif x == x.parent.left:
			x.parent.left = y
		else:
			x.parent.right = y

		y.left = x
		x.parent = y

	def splay(self, x):
		while x.parent != None:
			if x.parent.parent == None:
				if x == x.parent.left:
					# zig rotation
					self.rotr(x.parent)
				else:
					# zag rotation
					self.rotl(x.parent)
			elif x == x.parent.left and x.parent == x.parent.parent.left:
				# zig-zig rotation
				self.rotr(x.parent.parent)
				self.rotr(x.parent)
			elif x == x.parent.right and x.parent == x.parent.parent.right:
				# zag-zag rotation
				self.rotl(x.parent.parent)
				self.rotl(x.parent)
			elif x == x.parent.right and x.parent == x.parent.parent.left:
				# zig-zag rotation
				self.rotl(x.parent)
				self.rotr(x.parent)
			else:
				# zag-zig rotation
				self.rotr(x.parent)
				self.rotl(x.parent)

	def search(self, k):
		x = self.searchr(self.root, k)
		if x != None and x != self.root:
			self.splay(x)

		return x

	def insert(self, *keys):
		if type(keys[0]) == list:
			for key in keys[0]:
				self.insert(key)

			return self

		for key in keys:
			if hasattr(key, "__iter__"):
				node = Node(key[0], key[1])
			else:
				node = Node(key)
			y = None
			x = self.root

			while x != None:
				y = x
				if node.key < x.key:
					x = x.left
				elif node.key > x.key:
					x = x.right
				else: # node with key already exists
					x.data = node.data
					self.splay(x)
					return self

			# y is parent of x
			node.parent = y
			if y == None:
				self.root = node
			elif node.key < y.key:
				y.left = node
			else:
				y.right = node
			# splay the node
			self.splay(node)

		return self

	def print(self):
		self.printr(self.root, "", True)