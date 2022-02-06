from turtle import Turtle, Screen, screensize

W, H = screensize()


square_size = 6

size = 6

origin = False
destination = False


graph_change = False

## app_state ::= 0 (setup)  1 (plot)   2 (run)

app_state = 0



def get_nearest_square(x, y):
     print("Clicked at ", x, y)
     x = x - (x % square_size) - lost_width
     y = y - (y % square_size)

     print("Now at", x, y)

     return x, y


class Connection:

     def __init__(self):

          self.origin = None
          self.destination = None
          self.steps = []
          self.drawn = False

     def append(self, x, y):
          print("appended", x, y)
          self.steps.append((x, y))

     def draw(self, t):

          for x, y in self.steps:
               if (x,y) == self.destination: continue
               t.penup()
               t.goto(x, y)
               t.begin_fill()
               for _ in range(4):
                    t.forward(square_size)
                    t.right(90)
               t.end_fill()
          self.drawn = True

          


class Node:

     def __init__(self, x, y):
          self.x, self.y = x, y
          self.connections = []
          self.drawn = False

     def draw(self, t):
          t.penup()
          t.goto(self.x, self.y)
          t.begin_fill()
          for _ in range(4):
               t.forward(square_size)
               t.right(90)
          t.end_fill()
          self.drawn = True

          

     def add_connection(self, x, y):

          if not self.connections or self.connections[-1].destination is None:
               self.connections.append(Connection())

          print("Node class")
          most_recent_conn = self.connections[-1]

          print("Most recent conn", most_recent_conn)

          most_recent_conn.append(x, y)
          
          print("Why append not work")

     def end_connection(self, x, y):
          self.connections[-1].destination = (x, y)

          
          

          

class Graph:

     def __init__(self):
          self.nodes = {}
          self.most_recent_node = None


     def set_node(self, x, y):
          x, y = get_nearest_square(x, y)
          node_connector.goto(x, y)
          
          if (x,y) not in self.nodes:
               this_node = Node(x, y)
               self.nodes[(x,y)] = (this_node)
          else:
               this_node = self.nodes[(x, y)]
               
          self.current_node = this_node

          print("Current node is", x, y)

          

     def draw_nodes(self):
          node_t = Turtle()
          node_t.hideturtle()
          conn_t = Turtle()
          conn_t.hideturtle()
          print("Made turtle")
          node_t.color("green")
          node_t.speed(0)
          conn_t.color("yellow")
          conn_t.speed(0)
          print("speed turtle")
          for node in self.nodes.values():
               if not node.drawn:
                    node.draw(node_t)

               for connection in node.connections:

                    if not connection.drawn:

                         connection.draw(conn_t)

                    

               


     def connect_nodes(self, to_x, to_y):

          to_x, to_y = get_nearest_square(to_x, to_y)

          if (to_x, to_y) in self.nodes:
               print("End of connection")
               self.current_node.end_connection(to_x, to_y)

          else:
               print("Extending connection")
               self.current_node.add_connection(to_x, to_y)



          

                    

                    

          

          
               


     
               
          
     

     
          


def get_num(prompt):

     num = input(prompt)

     while not num.isdigit() or not (6 <= int(num) <= 25):
          print("Invalid. Enter between 6 and 25.")
          num = input(prompt)

     return int(num)






def sel_origin():
     if app_state == 1:
          origin = True
          destination = False


def sel_destination():
     if app_state == 1:
          destination = True
          origin = False

def sel_node():
     if app_state == 1:
          destination, origin = False, False
     
def handle_click(x, y):
     
     global graph_change
     if app_state == 1:
          node_connector.goto(x, y)
          graph.set_node(x, y)
          print("adding node")
          graph_change = True
          graph.draw_nodes()
     

def draw_grid(square_size):
     t = Turtle()
     t.hideturtle()
     t.speed(0)
     left, right = -W, W
     top, bottom = -H, H
     t.penup()
     t.goto(left, top)
     
     for x in range(left, right+1, square_size):
          print(x)
          t.goto(x, top)
          t.pendown()
          t.goto(x, bottom)
          t.penup()

     for y in range(top, bottom, square_size):
          t.goto(left, y)
          
          t.pendown()
          
          t.goto(right, y)
          t.penup()


     



               

def main():
     global app_state, square_size, size, lost_width, graph_change


     #size = get_num("Enter grid size: ")
     size = 10


     
     square_size = int(H / size)

     lost_width = W % square_size
     
     
     
     app_state = 1

     restart = False
     plot_path = False
     draw_grid(square_size)
     
          


##          try:
##               run_path_find()
##          except KeyboardInterrupt:
##               restart = True
               

     return restart

screen = Screen()
screen.onkey(sel_origin, "o")
screen.onkey(sel_destination, "d")
screen.onkey(sel_node, "n")
screen.onclick(handle_click)

graph = Graph()

node_connector = Turtle()

node_connector.ondrag(graph.connect_nodes)

node_connector.penup()


if __name__ == "__main__":
     use_app = True
     while use_app:
          app_state = 0
          use_app = main()
               

     
