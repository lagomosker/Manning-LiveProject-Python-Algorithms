#David Moskowitz submission
#Manning Liveproject unit: "How to think about solving a maze"
#Three classes: Maze, MazeCell, MazeExplorer
#To test: create a Maze(width, height, <string detailing the maze>) B(egin) G(goal) *(wall) with spaces or open path. 
#       : create a MazeExplorer(maze object, string representing facing "N","E","S" or "W")
#       : call explore_maze() on MazeExplorer object
#For example:
#maze=Maze(5,4,"******B*G**   ******")
#explorer=MazeExplorer(maze,"N")
#explorer.explore_maze()

#AFTER each explorer step, maze draws itself, with the explorer and facing represented by the arrow


class MazeCell:
    coordinates=[]
    desc=""
    def __init__(self, row, col, cell_desc):
        self.coordinates=[col,row]
        self.desc=cell_desc
        #print(self.coordinates, self.desc)

    def get_coordinates(self):
        return self.coordinates
    
    def get_desc(self):
        return self.desc

    def __repr__(self):
        return self.desc

   
#B(egin) G(oal) *(wall) 
class Maze:
    #0,0 is the upper left, i.e. northwest corner. All coordinates by column row 
    cells=[]
    #Apparently if I use numpy, I can count on shape for dimensions...I'll bulk up the code a bit instead.
    dimensions=[]
    #row colum pairs of moving up down etc. 
    orientation_steps=[[0,-1],[1,0],[0,1],[-1,0]] # col/row up,right,down,left i.e. NESW
     
    def __init__(self, num_cols, num_rows, stringrep):
        self.dimensions.append(num_cols)
        self.dimensions.append(num_rows)
        strIndex=0;#For clarity sake. Unpythonic? Maybe.
        for row in range(num_rows):
            for col in range(num_cols):
                self.cells.append(MazeCell(row, col, stringrep[strIndex]))
                strIndex+=1
    

    
    #Not very pythonic, but needed to separate it from the next function
    def get_cell(self,col, row):
        return self.cells[(row*self.dimensions[0]) + col]
    
    def get_forward_cell(self, location, facing):
        #print(location[0]+self.orientation_steps[facing][0])
        return self.get_cell(location[0]+self.orientation_steps[facing][0],location[1]+self.orientation_steps[facing][1])


    def __repr__(self):
        strrep=""
        for cell in self.cells:
            if (cell.get_coordinates()[0]==0): 
                strrep+="\n"
            strrep+=cell.get_desc()
        return strrep[1:] #Eliminate that first carriage return

    #Think Pac-Man: unexplored spaces are shown with . while explored spaces are empty
    def draw_with_explorer(self, explored_spaces, explorer,facing):
        strrep=""
        for cell in self.cells:
            if (cell.get_coordinates()[0]==0):
                strrep+="\n"
            else:
                first_line=False
           # print(explorer.get_coordinates())
            if (cell==explorer):#(cell.same_place(explorer.get_coordinates())):
                if (facing==0):
                    strrep+="↑"
                elif (facing==1):
                    strrep+="→"
                elif (facing==2):
                    strrep+="↓"
                else:
                    strrep+="←"
            elif (cell in explored_spaces) and cell.get_desc()!="G":
                strrep+="."
            else:
                strrep+=cell.get_desc()
        return strrep[1:]


class MazeExplorer:
    orientations=list("NESW")
    unexplored_cells=[]
    location=MazeCell(1,1,"X")
      
    def __init__(self, maze, compass_orientation):
        self.maze=maze
        self.orientation=self.orientations.index(compass_orientation)
        #Now let's find out where we're starting and prep our unexplored 
        for cell in maze.cells:
            if cell.get_desc()==" " or cell.get_desc()=="G":
                self.unexplored_cells.append(cell)
            if (cell.get_desc()=="B"):#Where we start
                self.location=cell
                coordinates=cell.get_coordinates()
            #For the instructions
            if cell.get_desc()=="B":
                print ("Begin:" +str(cell.get_coordinates()))
            if cell.get_desc()=="G":
                print ("Goal:" +str(cell.get_coordinates()))
  
    def turn_left(self,facing):
        if (facing==0):
            facing=3
        else:
            facing-=1
        return facing
    
    def turn_right(self,facing):
        if (facing==3):
            facing=0
        else:
            facing+=1
        return facing


    def explore_maze(self):
        while (self.unexplored_cells.count!=0):
            #print("\nExplorer at:" + str(self.location.get_coordinates()))
            coordinates=self.location.get_coordinates()
            facing=self.orientation
            if (self.maze.get_forward_cell(coordinates, facing).desc==" " or self.maze.get_forward_cell(coordinates, facing).desc=="G"):
                destination=self.maze.get_forward_cell(coordinates, facing)
            else: 
                facing=self.turn_right(facing)
                if (self.maze.get_forward_cell(coordinates, facing).desc==" " or self.maze.get_forward_cell(coordinates, facing).desc=="G"):
                    destination=self.maze.get_forward_cell(coordinates, facing)
                else:
                    facing=self.turn_left(facing)
                    facing=self.turn_left(facing)
                    if (self.maze.get_forward_cell(coordinates, facing).desc==" " or self.maze.get_forward_cell(coordinates, facing).desc=="G"):
                        destination=self.maze.get_forward_cell(coordinates, facing)
                    else:
                        facing=self.turn_left(facing)#going backwards
                        destination=self.maze.get_forward_cell(coordinates, facing)
            if self.location in self.unexplored_cells:
                self.unexplored_cells.remove(self.location)
            self.location=destination
            coordinates=self.location.get_coordinates()
            self.orientation=facing
            print(self.maze.draw_with_explorer(self.unexplored_cells,destination,facing)+"\n")
            if (self.location.get_desc()=="G"):
                print("Freedom!")
                return
        print ("No solution")


