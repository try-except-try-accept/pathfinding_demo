from turtle import Turtle, Screen, done, screensize
from math import inf as INF
from random import randint
from time import sleep
import ctypes



#RANDOM_GRAPH = [[randint(-W, W), randint(-H, H)] for i in range(5)]
#RANDOM_GRAPH = [[-229, -291], [237, -292], [-244, 164], [-179, -134], [209, 9]]
#print(f"RANDOM_GRAPH = {RANDOM_GRAPH}")


# set up canvas:
Turtle().write("initialising...")
user32 = ctypes.WinDLL('user32')
SW_MAXIMISE = 3
hWnd = user32.GetForegroundWindow()
user32.ShowWindow(hWnd, SW_MAXIMISE)
dimensions = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
W, H = dimensions[0] // 2.1, dimensions[1] // 2.85
screensize(W, H)
Screen().clear()

RANDOM_GRAPH = True
NODE_SIZE = 20
MENU_BUFFER = W # not implemented
COL_HEADING_BUFFER = 15

MSG_SIZE = 200

OUTPUT_DISPLAY_BUFFER = -W + 200

MSG_OFFSET = W / 10


## TO DO


def show_info(msg, is_error=False):
        if is_error:
                msg_tt.color("red")
        else:
                msg_tt.color("green")
        msg_tt.clear()
        msg_tt.penup()
        msg_tt.goto(W-500, -H-MSG_OFFSET)
        msg_tt.pendown()
        msg_tt.write(msg)        




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

class MenuElement:

        WIDTH = 40
        HEIGHT = 15

        def __init__(self, x, y, label):
                self.left = x
                self.right = x + self.WIDTH
                self.top = y
                self.bottom = y - self.HEIGHT

                self.action = None
                self.t = Turtle()
                self.t.hideturtle()

        def is_clicked(self, x, y):
                if self.left <= x <= self.right:
                        if self.top >= y >= self.bottom:
                                return True

                return False



class Button(MenuElement):

        def __init__(self, x, y, label, action):
                super().__init__(x, y, label)
                self.action = action



class DropDown(MenuElement):



        def __init__(self, x, y, label, options):
                super().__init__(x, y, label)

                self.options = options
                self.action = self.expand
                self.current = "▼" + label


        def expand(self):
                self.expanded = True

        def collapse(self):
                pass


        def draw(self):

                t = self.t

                if self.expanded:

                        options = [self.label] + self.options

                else:

                        options = [self.current]


                x, y = self.x, self.y

                for option in options:
                        t.goto(x, y)
                        t.write(option)
                        t.penup()
                        t.goto(x, y)
                        t.pendown()
                        t.goto(x+self.WIDTH, y)
                        t.goto(x + self.WIDTH, y + self.HEIGHT)
                        t.goto(x, y + self.HEIGHT)
                        t.goto(x, y)

                        t.penup()

                        y += self.HEIGHT









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
                self.deleted = False


        def __repr__(self):
                return self.label

        def deselect(self, mode=None):
                if mode == self.role:
                        print(self, f"Is no longer the {mode}")
                        self.role = None

        def link_to(self, neighbour):
                self.connections.append(neighbour)

        def draw(self, selected=None):

                if self.deleted:
                        self.t.clear()
                        return

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
                self.t = Turtle()
                self.t.hideturtle()
                self.t.ondrag(self.adjust)
                self.t.onrelease(self.update)
                self.adjustment = 0
                self.deleted = False

        def adjust(self, x, y):
                
                
                if y > self.top:
                        self.weight += 1
                else:
                        if self.weight > 1:
                                self.weight -= 1

                print(self.weight)

                print("Adjusting")
                print(self.weight)
                self.update()
                
                

        def update(self, x, y):
                #self.weight = self.adjustment
                self.adjustment = 0
                self.drawn = False
                self.t.clear()
                self.t.write(str(self.weight), font=("Courier New", self.SIZE, "normal"))
                

        def draw(self, selected=None):

                self.t.showturtle()

                if self.deleted:
                        self.t.clear()
                        self.t.hideturtle()
                        return
                

                if not self.drawn:

                        self.t.speed(0)
                        self.t.penup()
                        self.t.goto(self.left, self.top)
                        self.t.pendown()
                        self.t.write(str(self.weight), font=("Courier New", self.SIZE, "normal"))

                self.drawn = True







class Connection:

        def __init__(self, origin, destination):
                self.origin = origin
                self.destination = destination
                
                weight = randint(2, 20)
                midpoint = calculate_midpoint(origin, destination)
                print("Will draw label at", midpoint)
                self.label = WeightLabel(weight, *midpoint)
                self.deleted = False

                self.t = Turtle()
                self.t.hideturtle()
                self.t.speed(0)
                

        def delete(self):
                self.deleted = True
                self.label.deleted = True # bad redundancy.


        def draw(self, selected=None):
                if self.deleted:
                        self.t.clear()
                        return


                self.t.speed(0)
                self.t.hideturtle()

                self.t.penup()
                self.t.goto(self.origin.x, self.origin.y)
                self.t.pendown()
                self.t.goto(self.destination.x, self.destination.y)



class Graph:

        def __init__(self):

                self.nodes = {}
                self.current_label = 65
                self.currently_selected = None
                self.labels = []
                self.connections = {}
                self.redraw = set()
                self.origin = None
                self.destination = None
                self.iter_q = []

                if RANDOM_GRAPH:

                        for i in range(5):

                                x, y = randint(OUTPUT_DISPLAY_BUFFER, W), randint(-H, H)
                                self.redraw.add(self.add_node(x, y))

                        for node in self.nodes.values():
                                for other_node in self.nodes.values():
                                        if node == other_node:
                                                continue

                                        if randint(0, 100) > 70 and other_node not in node.connections:
                                                new_conn = self.add_connection(node, other_node)
                                                self.redraw.add(new_conn)
                                                self.redraw.add(new_conn.label)


                        self.update(None)

        def __iter__(self):
                self.iter_q = list(self.nodes.values())
                return self

        def __next__(self):
                if self.iter_q:
                        return self.iter_q.pop(0)
                raise StopIteration
                

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

        def get_distance(self, node, neighbour):
                poss_hashes = [hash(str(node) + str(neighbour)),
                                           hash(str(neighbour) + str(node))]

                for possibility in poss_hashes:
                        connection = self.connections.get(possibility)
                        if connection is not None:
                                return connection.label.weight


                raise Exception(f"Node {node} and node {neighbour} are not connected.")



        def select_label(self, x, y):
                print("selecting label")
                for label in self.labels:
                        if label.left <= x <= label.right:
                                if label.bottom >= y <= label.top:
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


        def delete_node(self, delete=None):
                if delete is None:
                        delete = self.currently_selected

                if delete == self.origin:
                        self.origin = None
                elif delete == self.destination:
                        self.destination = None

                for node in self.nodes.values():

                        if delete in node.connections:
                                node.connections.remove(delete)
                                

                connections_to_delete = []
                
                for key, connection in self.connections.items():
                        if connection.origin is delete or connection.destination is delete:
                                connections_to_delete.append(key)
                                connection.delete()
                                self.redraw.add(connection)
                                


                for key in connections_to_delete:
                        self.connections.pop(key)
                        
                        
                        


                self.nodes.pop(str(delete))

                delete.deleted = True
                self.redraw.add(delete)

                self.update(delete)
                                
                        

        def update(self, element):

                print("updated graph because", type(element))

                if element is not None:
                        element.draw(self.currently_selected)
                if type(element) == Connection:
                        element.label.draw()

                to_redraw = set(self.redraw)

                for redraw_element in to_redraw:
                        redraw_element.draw()
                        if type(redraw_element) == Connection:
                                redraw_element.label.draw()

                        self.redraw.remove(redraw_element)


                if type(element) == Node:
                        self.redraw.add(element)

        def add_connection(self, orig=None, dest=None):

                if orig == None or dest == None:
                        return None

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

                orig.link_to(dest)
                dest.link_to(orig)

                return new_connection

        def delete(self):
                nodes = list(self.nodes.values())
                for node in nodes:
                        self.currently_selected = node
                        self.delete_node()



class Table:
        COL_WIDTH = 75
        ROW_HEIGHT = 25

        def __init__(self, x, y, data):

         
               

                self.row_keys = list(data.keys())

                self.rows = len(data.keys())

                print("Found", self.rows, "rows")

                self.col_keys = list(data[self.row_keys[0]].keys())

                self.cols = len(self.col_keys)

                print("Found", self.cols, "cols")

                self.origin = x, y

                
                self.cells = []

                
                self.t = Turtle()
                self.t.speed(0)
                self.t.hideturtle()


                

                for label in self.col_keys:
                        self.t.penup()
                        self.t.goto(x+COL_HEADING_BUFFER, y)
                        self.t.pendown()
                        self.t.write(label, font=('Arial', 8, 'bold'))
                        x += self.COL_WIDTH
                        

                        

                
                for y in range(self.rows):
                        row = []
                        for y in range(self.cols):
                                t = Turtle()
                                t.hideturtle()
                                t.speed(0)
                                row.append(t)
                        self.cells.append(row)                               
                        

                

                


        def draw(self):

                x, y = self.origin
                self.t.penup()
                self.t.goto(x, y)
                self.t.pendown()
                offset = 0

                for i in range(self.rows+1):
                        self.t.forward(self.COL_WIDTH * self.cols)                       
                        self.t.penup()
                        y -= self.ROW_HEIGHT
                        
                        self.t.goto(x, y)                        
                        self.t.pendown()                

                x, y = self.origin
                self.t.penup()
                self.t.goto(x, y)
                self.t.pendown()

                offset = 0

                self.t.right(90)
                
                for j in range(self.cols):
                        self.t.forward(self.ROW_HEIGHT * self.rows)                       
                        self.t.penup()
                        x += self.COL_WIDTH
                        self.t.goto(x, y)                        
                        self.t.pendown()

                self.t.left(90)

        def update(self, row_key, col_key, new_data):

                row_index = list(self.row_keys).index(row_key)
                col_index = self.col_keys.index(col_key)                

                x_change = self.origin[0] + (col_index * self.COL_WIDTH) + 25
                y_change = self.origin[1] - (row_index * self.ROW_HEIGHT) - 25

                turt = self.cells[row_index][col_index]

                turt.penup()
                turt.goto(x_change, y_change)

                turt.pendown()

                turt.clear()



                turt.write(str(new_data))

                
        def delete(self):

                self.t.clear()
                for row in self.cells:
                        for t in row:
                                t.clear()
                
                

class App:

        def __init__(self):
                self.state = 0
                self.connecting = False
                self.setting_origin = False
                self.setting_dest = False
                self.adjusting_label = False
                self.graph = Graph()
                self.selected_algorithm = 1
                self.table = None

                self.menu_elements = [DropDown(MENU_BUFFER, H, "Choose algorithm:", ["A* Search", "Dijkstra's Algorithm"]),
                                                          Button(MENU_BUFFER, H-50, "Run Demo", self.run_demo)]

                self.menu_elem_in_focus = None
                self.write_instructions()

        def new_graph(self):
                self.graph.delete()
                self.graph = Graph()

        def write_instructions(self):

                t = Turtle()
                t.speed(0)
                offset = -50

                for sentence in """Click to create a node.
Hold Z and click to form a connection between nodes.
Hold O and click to decide the origin node.
Hold D and click to decide the destination node.
Hold A and drag to adjust a weight label.
Press DELETE to delete a node and its connections.
Press R to generate a new random graph.
Press I to delete all island nodes.
Press 1 to run Dijkstra's Algorithm
Press 2 to run the A* Algorithm
Press 3 to run a BFS
Press 4 to run a DFS""".split("\t"):
                        
                        t.penup()
                        t.goto(-W, H)
                        t.pendown()
                        t.write(sentence)

                        offset += 15




                

                        
        def perform_dijkstras(self, g, origin, destination, rows):
                # Dijkstra's Algorithm
                origin = g.origin


                # set up table
                table = {n:{"node":str(n), "cost":INF if n is not origin else 0, "prev":"", "calc":""} for n in g.nodes.values()}                        

                self.table = Table(-W, H-MSG_SIZE, table)

                self.table.draw()

                for n, row in table.items():
                        self.update_row(n,
                                   {"node":n,
                                   "cost":row["cost"],      
                                   "prev":row["prev"],
                                   "calc":row["calc"]})                

                unvisited = list(g.nodes.values())
                visited = []

                while len(unvisited):

                        smallest = INF
                        current_node = None

                        ## find the unvisited vertex with smallest known distance from the origin
                        for node, data in table.items():
                                if node not in unvisited:        continue
                                if data["cost"] < smallest:
                                        smallest = data["cost"]
                                        current_node = node
                        print("The current vertex is", current_node)

                        ## find each unvisited neighbour of the current vertex

                        for neighbour in current_node.connections:
                                g.currently_selected = neighbour
                                g.update(neighbour)
                                
                                print(f"{current_node} is connected to {neighbour}")
                                if neighbour not in unvisited:
                                        print("Already visited")
                                else:
                                        ## calculate total distance from origin node
                                        tot = g.get_distance(current_node, neighbour)

                                        calc = str(tot)
                                        # until we've got back to the start

                                        
                                        print(f"We need to make it back from {current_node} to {origin}")
                                        pitstop = table[current_node]["cost"]
                                        print(f"Came via {current_node} and that cost {pitstop}")
                                        tot += pitstop
                                        calc += " + " + str(pitstop)
                                        print(f"so the total is now {tot}")


                                        if tot < table[neighbour]["cost"]:
                                                table[neighbour]["prev"] = current_node                                                        
                                                table[neighbour]["cost"] = tot                                                                                                              
                                                table[neighbour]["calc"] = calc
                                                self.update_row(neighbour,
                                                           {"cost":tot,      
                                                            "prev":current_node,
                                                            "calc":calc})
                                                
                                                for node, data in table.items():
                                                        print(
                                                                f'{str(node)} \t\t {data["cost"]} \t\t {data["prev"]} \t\t {data["calc"]}')

                                                print()
                                        else:
                                                print(f"{tot} was not shorter. table not updated")
                        unvisited.remove(current_node)
                self.trace_best_path(table, g, origin)

        def perform_a_star(self, g, origin, destination, rows):
                # A* Algorithm - something is broken here

                distances = [calculate_distance(n, g.destination) for n in g.nodes.values()]


                max_distance = max(distances)

                print("Maximum distance is", max_distance)

                weights = [connection.label.weight for connection in g.connections.values()]

                max_weight = max(weights)

                print("Max weight is", max_weight)

                h_cost_div_factor = (max_weight / max_distance) / 2

                
                print("Multiply all weights by", h_cost_div_factor)
                

                                      

                 # set up table
                table = {n:{"node":str(n),
                            "g-cost":INF if n is not origin else 0,
                            "h-cost":round(calculate_distance(n, destination) * h_cost_div_factor, 2),
                            "f-cost":INF,
                            "prev":"", "calc":""} for n in g.nodes.values()}                        

                self.table = Table(-W, H-MSG_SIZE, table)

                self.table.draw()

                for n, row in table.items():
                        self.update_row(n,
                                   {"node":n,
                                   "g-cost":row["g-cost"],
                                   "h-cost":row["h-cost"],
                                   "f-cost":row["f-cost"],
                                   "prev":row["prev"],
                                   "calc":row["calc"]})

                # OPEN - the set of nodes to be evaluated
                # add the start node to open
                open_nodes = set([origin])
                # CLOSED - the set of nodes already evaluated
                closed_nodes = set()


                current_node = None

                while len(open_nodes):

                        ## find the open list node with smallest known f-cost                              

                        current_node = min(open_nodes, key=lambda n: table[n]["f-cost"])

                        if current_node == g.destination:
                                break
                        
                        print("The current vertex is", current_node)

                        ## remove current from OPEN
                        open_nodes.remove(current_node)

                        ## add current to CLOSED
                        closed_nodes.add(current_node)

                        ## find each un-closed neighbour of the current node
                        for neighbour in current_node.connections:                                        

                                if neighbour in closed_nodes:
                                        continue

                                ## calculate f-cost
                                g_cost = g.get_distance(current_node, neighbour)
                                calc = str(g_cost)        

                                
                                
                                pitstop = table[current_node]["g-cost"]
                                
                                print(f"Came via {current_node} and that cost {pitstop}")
                                g_cost += pitstop
                                                                        
                                calc += " + " + str(pitstop)                             
                                h_cost = table[neighbour]["h-cost"]                                        
                                calc += f" + {h_cost}"

                                f_cost = g_cost + h_cost

                                
                                print(f"so the f_cost is now {f_cost}")

                                if neighbour not in open_nodes or g_cost < table[neighbour]["g-cost"]:
                                        open_nodes.add(neighbour)
                                        table[neighbour]["prev"] = current_node                                                        
                                        table[neighbour]["f-cost"] = f_cost
                                        table[neighbour]["g-cost"] = g_cost
                                                                                            
                                        table[neighbour]["calc"] = calc
                                        
                                        self.update_row(neighbour,
                                                   {"g-cost":g_cost,
                                                    "h-cost":h_cost,
                                                    "f-cost":f_cost,
                                                    "prev":str(current_node),
                                                    "calc":calc})
                                        
                                        for node, data in table.items():
                                                print(
                                                        f'{str(node)} \t\t {data["f-cost"]} \t\t {data["h-cost"]} \t\t {data["g-cost"]} \t\t {data["prev"]} \t\t {data["calc"]}')

                                        print()
                                else:
                                        print(f"{f_cost} was not shorter. table not updated")


                                open_nodes.add(neighbour)
                        
                                


                        
                self.trace_best_path(table, g, origin)


        def update_row(self, neighbour, updates):

                for heading, value in updates.items():
                                
                        self.table.update(neighbour, heading, str(value))
                                

        def run_demo(self):


                
                        
                g = self.graph

                if g.origin is None or g.destination is None:
                        
                        show_info("Set origin node and destination node first.", is_error=True)
                        
                        
                        return False
                elif any(len(node.connections) == 0 for node in g.nodes.values()):
                        
                        show_info("Can't run the demo if island nodes are present.", is_error=True)
                        
                        
                        return False


                if self.table:
                        self.table.delete()

                self.state = 1

                rows = len(g.nodes.keys())
                origin = g.origin
                destination = g.destination

                if self.selected_algorithm == 0:
                        self.perform_dijkstras(g, origin, destination, rows)

                else:
                        self.perform_a_star(g, origin, destination, rows)

                        
                

                        
        def trace_best_path(self, table, g, origin):
                        

                destination = g.destination
                node = destination

                
                path = [str(destination)]

                while node is not origin:


                        node = table[node]["prev"]
                        path.append(str(node))


                show_info(f"The shortest path from {origin} to {destination} is..." + " → ".join(reversed(path)))

                self.state = 0
















        def click_handler(self, x, y):

                x, y = int(x), int(y)

                g = self.graph

                if self.state == 0:
                        if x > MENU_BUFFER:
                                for elem in self.menu_elements:
                                        if elem.is_pressed():
                                                elem.action()

                        if y > OUTPUT_DISPLAY_BUFFER:

                                if self.adjusting_label:
                                        label = g.select_label(x, y)
                                        if label is not None:
                                                print("Selected a label")

                                        new_element = label
                                        

                                elif self.setting_origin or self.setting_dest:
                                        new_role = "origin" if self.setting_origin else "destination"
                                        selected_node = g.select_node(x, y, make_new=False)

                                        if selected_node is not None:
                                                if new_role == "origin":
                                                        g.origin = selected_node
                                                        if g.destination == g.origin:
                                                                g.destination == None
                                                else:
                                                        g.destination = selected_node
                                                        if g.destination == g.origin:
                                                                g.origin == None

                                                for other_node in g.nodes.values():
                                                        if other_node.role == new_role:
                                                                other_node.deselect(new_role)
                                                                g.redraw.add(other_node)
                                                selected_node.role = new_role
                                                new_element = selected_node

                                elif self.connecting:
                                        print("Making a connection")
                                        origin = g.currently_selected
                                        destination = g.select_node(x, y, make_new=False, keep_selected=True)
                                        new_element = g.add_connection(orig=origin, dest=destination)
                                        print("The new element is", new_element)
                                        self.connecting = False

                                else:
                                        
                                        
                                        new_element = g.select_node(int(x), int(y))
                                        g.currently_selected = new_element




                        g.update(new_element)

        def delete_islands_handler(self):
                for node in self.graph:
                        if len(node.connections) == 0:
                                self.graph.delete_node(node)

        def delete_handler(self):
                selected = self.graph.currently_selected
                if selected is not None:
                        self.graph.delete_node()

                else:
                        show_info("Nothing selected, cannot delete", is_error=True)

                        

        def start_connect_handler(self):
                if not self.connecting:
                        show_info("Connecting nodes...")
                        self.connecting = True

        def stop_connect_handler(self):
                self.connecting = False
                show_info("")
                
                

        def start_origin_select_handler(self):
                if not self.setting_origin:
                        show_info("Setting origin node")
                        self.setting_origin = True

        def stop_origin_select_handler(self):
                self.setting_origin = False               
                
                show_info("")

        def start_dest_select_handler(self):
                if not self.setting_dest:
                        self.setting_dest = True
                        show_info("Setting destination node")
                        

        def stop_dest_select_handler(self):
                self.setting_dest = False                
                show_info("")



        def start_label_adjust_handler(self):
                if not self.adjusting_label:
                        show_info("Adjusting label")
                        self.adjusting_label = True

        def stop_label_adjust_handler(self):
                self.adjusting_label = False
                show_info("")
                


        def dijkstras_handler(self):
                show_info("Running Dijkstra's Algorithm")
                self.selected_algorithm = 0
                self.run_demo()

        def a_star_handler(self):
                show_info("Running A* Algorithm")
                self.selected_algorithm = 1
                self.run_demo()

        def bfs_handler(self):
                note = ""
                if g.origin is None or g.destination is None:
                        note = "Exploring entire graph as no origin/destination was set"                        
                show_info(f"Running the breadth-first search algorithm. {note}")
                self.selected_algorithm = 2
                self.run_demo()

        def dfs_handler(self):
                note = ""
                if g.origin is None or g.destination is None:
                        note = "Exploring entire graph as no origin/destination was set"                        
                show_info(f"Running the depth-first search algorithm. {note}")
                self.selected_algorithm = 3
                self.run_demo()

        





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

msg_tt = Turtle()
msg_tt.hideturtle()
msg_tt.speed(0)
msg_tt.penup()
msg_tt.goto(W-400, -H)
msg_tt.pendown()


screen = Screen()
app = App()

screen.onclick(app.click_handler)



screen.onkeypress(app.start_connect_handler, "z")
screen.onkeyrelease(app.stop_connect_handler, "z")
screen.onkeypress(app.start_origin_select_handler, "o")
screen.onkeyrelease(app.stop_origin_select_handler, "o")
screen.onkeypress(app.start_dest_select_handler, "d")
screen.onkeyrelease(app.stop_dest_select_handler, "d")
screen.onkeypress(app.start_label_adjust_handler, "a")
screen.onkeypress(app.delete_islands_handler, "i")
screen.onkeyrelease(app.stop_label_adjust_handler, "a")
screen.onkeypress(app.delete_handler, "Delete")
screen.onkeypress(app.dijkstras_handler, "1")
screen.onkeypress(app.a_star_handler, "2")
screen.onkeypress(app.bfs_handler, "3")
screen.onkeypress(app.dfs_handler, "4")
screen.onkeypress(app.new_graph, "r")

screen.listen()
done()
