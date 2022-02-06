from turtle import Turtle, Screen, done

NODE_SIZE = 20

def calculate_distance(node1, node2):
	return abs(node1.x - node2.x) + abs(node1.y - node2.y)

def calculate_midpoint(node1, node2):

	return node1.x + abs(node1.x - node2.x), node1.y + abs(node1.y - node2.y)

class Node:
	def __init__(self, x, y, label):
		self.x, self.y = x, y
		self.label = label
		self.connections = []
		self.selected = False
		self.left = self.x - (NODE_SIZE)
		self.right = self.x + (NODE_SIZE)
		self.top = self.y + (NODE_SIZE * 2)
		self.bottom = self.y


	def __repr__(self):
		return (f"left:{self.left} right:{self.right} top:{self.top} bottom:{self.bottom}")

	def deselect(self):
		self.selected = False

	def draw(self):

		node_tt.speed(0)
		node_tt.hideturtle()
		node_tt.penup()
		node_tt.goto(self.x, self.y)
		node_tt.pendown()
		if self.selected:
			node_tt.color("red")
		else:
			node_tt.color("black")

		node_tt.begin_fill()
		node_tt.circle(NODE_SIZE)
		node_tt.end_fill()




class WeightLabel:
	SIZE = 32

	def __init__(self, value, x, y):
		self.weight = value
		self.left = x
		self.top = y
		self.right = x + self.SIZE
		self.bottom = y + self.SIZE

	def adjust(self, change=-1):

		if self.weight > 1:
			self.weight += change

	def draw(self):
		t = Turtle()
		t.speed(0)
		t.penup()
		t.goto(self.x, self.y, font=("Courier New", self.SIZE, "normal"))







class Connection:

	def __init__(self, origin, destination):
		self.origin = origin
		self.destination = destination
		self.weight = calculate_distance(origin, destination)
		midpoint = calculate_midpoint(origin, destination)
		self.label = WeightLabel(self.weight, *midpoint)


	def draw(self):


		conn_tt.speed(0)
		conn_tt.hideturtle()

		conn_tt.penup()
		conn_tt.goto(self.origin.x, self.origin.y)
		conn_tt.pendown()
		conn_tt.goto(self.destination.x, self.destination.y)



class Graph:

	def __init__(self):

		self.nodes = {}
		self.current_label = 65
		self.currently_selected = None
		self.labels = []

	def get_next_label(self):
		label = self.current_label
		self.current_label += 1
		return chr(label)

	def add_node(self, x, y):


		label = self.get_next_label()
		new_node = Node(x, y, label)
		self.nodes[label] = new_node
		return new_node

		
		

	def select_label(self, x, y):
		for label in self.labels:
			if label.left <= x <= label.right:
				if label.bottom <= y <= label.top:
					return label

		return None

	def select_node(self, x, y):
		node_found = None

		for node in self.nodes.values():


			node.deselect()

			if node_found:
				continue


			if node.left <= x <= node.right:
				if node.bottom <= y <= node.top:
					node_found = node
					node_found.selected = True
					continue

		if node_found:
			return node_found


		return self.add_node(x, y)

	def update_graph(self):

		nodes = dict(self.nodes).values()

		for node in nodes:
			node.draw()

			for connection in node.connections:
				connection.draw()

	def add_connection(self, orig=None, dest=None):

		if orig is None:
			orig = self.currently_selected
		new_connection = Connection(orig, dest)

		self.labels.append(new_connection.label)
		orig.connections.append(new_connection)

		self.currently_selected = dest

class App:

	def __init__(self):

		self.connecting = False
		self.graph = Graph()


	def click_handler(self, x, y):


		g = self.graph

		if self.connecting:
			print("Making a connection")
			destination = g.select_node(x, y)
			g.add_connection(dest=destination)
			self.connecting = False

		else:

			label = g.select_label(x, y)
			if label is not None:
				print("Selected a label")
			else:
				node = g.select_node(x, y)

				g.currently_selected = node


		g.update_graph()

	def key_down_handler(self):
		if not self.connecting:
			print("Connecting")
			self.connecting = True

	def key_up_handler(self):
		print("No longer connecting")
		self.connecting = False





	# click to create a node / select a node

	# shift click to connect nodes

	# click and drag weight label to adjust weight

node_tt = Turtle()
conn_tt = Turtle()

screen = Screen()
app = App()

screen.onclick(app.click_handler)

screen.onkeypress(app.key_down_handler, "z")
screen.onkeyrelease(app.key_up_handler, "z")

screen.listen()
done()