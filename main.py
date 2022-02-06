from turtle import Turtle, Screen, done

NODE_SIZE = 20

def calculate_distance(node1, node2):
	return abs(node1.x - node2.x) + abs(node1.y - node2.y)

def calculate_midpoint(node1, node2):

	print("Midpoint between")
	print(node1)
	print("And")
	print(node2)

	if node1.x > node2.x:
		new_x =  node1.x - (abs(node1.x - node2.x)) // 2
	else:
		new_x = node1.x + (abs(node1.x - node2.x)) // 2

	if node1.y > node2.y:
	 	new_y = node1.y - abs(node1.y - node2.y) // 2
	else:
		new_y = node1.y + abs(node1.y - node2.y) // 2

	return new_x, new_y
class Node:
	def __init__(self, x, y, label):
		self.x, self.y = x, y
		self.label = label
		self.connections = []
		self.left = self.x - (NODE_SIZE)
		self.right = self.x + (NODE_SIZE)
		self.top = self.y + (NODE_SIZE * 2)
		self.bottom = self.y
		self.role = None
		self.t = Turtle()
		self.t.hideturtle()
		self.t.pensize(10)


	def __repr__(self):
		return (f"left:{self.left} right:{self.right} top:{self.top} bottom:{self.bottom}")

	def deselect(self, mode=None):
		if mode == self.role:
			print(self, f"Is no longer the {mode}")
			self.role = None


	def draw(self, selected=None):

		self.t.speed(0)
		if self.role == "origin":
			self.t.color("blue")
		elif self.role == "destination":
			self.t.color("green")
		else:
			self.t.color("black")

		self.t.hideturtle()
		self.t.penup()
		self.t.goto(self.x, self.y)
		self.t.pendown()
		if self == selected:
			self.t.fillcolor("red")
		else:
			self.t.fillcolor("black")

		self.t.begin_fill()
		self.t.circle(NODE_SIZE)


		self.t.end_fill()
		self.t.penup()
		self.t.goto(self.x-NODE_SIZE*0.15, self.y+(NODE_SIZE*0.66))
		self.t.color("white")
		self.t.write(self.label)




class WeightLabel:
	SIZE = 14

	def __init__(self, value, x, y):
		self.weight = value
		self.left = x + 10
		self.top = y
		self.right = x + self.SIZE
		self.bottom = y + self.SIZE
		self.drawn = False

	def adjust(self, change=-1):

		if self.weight > 1:
			self.weight += change

	def draw(self, selected=None):

		if not self.drawn:

			label_tt.speed(0)
			label_tt.penup()
			label_tt.goto(self.left, self.top)
			label_tt.pendown()
			label_tt.write(str(self.weight), font=("Courier New", self.SIZE, "normal"))

		self.drawn = True







class Connection:

	def __init__(self, origin, destination):
		self.origin = origin
		self.destination = destination
		self.weight = calculate_distance(origin, destination)
		midpoint = calculate_midpoint(origin, destination)
		print("Will draw label at", midpoint)
		self.label = WeightLabel(self.weight, *midpoint)


	def draw(self, selected=None):


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
		self.connections = {}
		self.redraw = set()

	def get_next_label(self):
		label = self.current_label
		self.current_label += 1
		return chr(label)

	def add_node(self, x, y):


		label = self.get_next_label()
		new_node = Node(x, y, label)

		self.nodes[label] = new_node
		self.currently_selected = new_node
		return new_node

		
		

	def select_label(self, x, y):
		for label in self.labels:
			if label.left <= x <= label.right:
				if label.bottom <= y <= label.top:
					return label

		return None

	def select_node(self, x, y, make_new=True, keep_selected=False):
		node_found = None

		for node in self.nodes.values():

			if node_found:
				continue

			if node.left <= x <= node.right:
				if node.bottom <= y <= node.top:
					node_found = node
					if not keep_selected:
						self.currently_selected = node_found
					continue

		if node_found:
			print("node found")
			return node_found

		else:
			print("node not found")

		if make_new:
			return self.add_node(x, y)
		else:
			return None

	def update_graph(self, element):

		print("updated graph because", type(element))

		if element is not None:
			element.draw(self.currently_selected)
		if type(element) == Connection:
			element.label.draw()

		to_redraw = set(self.redraw)

		for redraw_element in to_redraw:
			redraw_element.draw()
			self.redraw.remove(redraw_element)


		if type(element) == Node:
			self.redraw.add(element)





	def add_connection(self, orig=None, dest=None):

		connection_hash = hash(str(orig) + str(dest))

		print(connection_hash)

		if orig == dest:
			print("Can't link a node to itself")
			return None

		if connection_hash in self.connections:
			print("already connected")

			return None

		new_connection = Connection(orig, dest)

		self.labels.append(new_connection.label)
		self.connections[connection_hash]  = new_connection

		return new_connection

class App:

	def __init__(self):

		self.connecting = False
		self.setting_origin = False
		self.setting_dest = False
		self.graph = Graph()



	def click_handler(self, x, y):
		x, y = int(x), int(y)

		g = self.graph

		if self.setting_origin or self.setting_dest:
			new_role = "origin" if self.setting_origin else "destination"
			selected_node = g.select_node(x, y, make_new=False)
			if selected_node is not None:
				for other_node in g.nodes.values():
					if other_node.role == new_role:
						other_node.deselect(new_role)
						g.redraw.add(other_node)

				selected_node.role = new_role
				new_element = selected_node


		if self.connecting:
			print("Making a connection")
			origin = g.currently_selected
			destination = g.select_node(x, y, make_new=False, keep_selected=True)
			new_element = g.add_connection(orig=origin, dest=destination)
			print("The new element is", new_element)
			self.connecting = False

		else:

			label = g.select_label(x, y)
			if label is not None:
				print("Selected a label")
			else:
				new_element = g.select_node(int(x), int(y))
				g.currently_selected = new_element


		g.update_graph(new_element)

	def start_connect_handler(self):
		if not self.connecting:
			print("Connecting")
			self.connecting = True

	def stop_connect_handler(self):
		print("No longer connecting")
		self.connecting = False

	def start_origin_select_handler(self):
		if not self.setting_origin:
			print("Setting origin node")
			self.setting_origin = True

	def stop_origin_select_handler(self):
		print("No longer setting origin node")
		self.setting_origin = False

	def start_dest_select_handler(self):
		if not self.setting_dest:
			print("Setting destination node")
			self.setting_dest = True

	def stop_dest_select_handler(self):
		print("No longer setting destination node")
		self.setting_dest = False







	# click to create a node / select a node

	# shift click to connect nodes

	# click and drag weight label to adjust weight

node_tt = Turtle()
node_tt.pensize(10)
node_tt.hideturtle()
conn_tt = Turtle()
conn_tt.hideturtle()
label_tt = Turtle()
label_tt.hideturtle()

screen = Screen()
app = App()

screen.onclick(app.click_handler)

screen.onkeypress(app.start_connect_handler, "z")
screen.onkeyrelease(app.stop_connect_handler, "z")
screen.onkeypress(app.start_origin_select_handler, "o")
screen.onkeyrelease(app.stop_origin_select_handler, "o")
screen.onkeypress(app.start_dest_select_handler, "d")
screen.onkeyrelease(app.stop_dest_select_handler, "d")

screen.listen()
done()