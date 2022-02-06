from turtle import Turtle, Screen, screensize

W, H = screensize()


square_size = 6

size = 6

origin = False
destination = False
graph_change = False

## app_state ::= 0 (setup)  1 (plot)   2 (run)

app_state = 0


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

class Graph:

     def __init__(self):
          self.nodes = []


     def add_node(self, x, y):
          print(f"Clicked at {x} {y}")
          x = x - (x % square_size) - lost_width
          y = y - (y % square_size)
          print(f"Floored to {x} {y}")

          self.nodes.append(Node(x, y))


     def draw_nodes(self):
          t = Turtle()
          print("Made turtle")
          t.color("green")
          t.speed(0)
          print("speed turtle")
          for node in self.nodes:
               if not node.drawn:
                    node.draw(t)
               


def get_nearest_square(x_click, y_click):
     
     return x_click % square_size, y_click % square_size

     
               
          
     

     
          


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
          graph.add_node(x, y)
          print("adding node")
          graph_change = True
          graph.draw_nodes()
     

def draw_grid(square_size):
     t = Turtle()
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


if __name__ == "__main__":
     use_app = True
     while use_app:
          app_state = 0
          use_app = main()
               

     
