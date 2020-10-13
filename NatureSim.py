import tkinter, time, random

"""
A simulation of rain. All drops are lists [handle, radius] that grow randomly and reset to zero as all those below them when they reach max_size
Ideally, those below should be placed in separate data structures, resetting in order to better simulate drops falling. But then, we could move the ovals too.
"""
drop_radius_increase=2
drop_density=10 #Number of rows and columns
window_dim=1000
max_size=40
drops_per_loop=100 #How many--roughly--drops we increase per loop (may have repeat random numbers)
window = tkinter.Tk()
window.geometry("1000x1000")
window.title("Rain on a window")
window.configure(background="white")

#Determines if 
def below_drop(resetting_drop, drop_tested):
    return resetting_drop[0]==drop_tested[0] and resetting_drop[1]<drop_tested[1] #seeing if same column, lower row

def let_it_rain():
    drops=[]
    #convenience variable
    drop_space=int((window_dim/drop_density))
    canvas=tkinter.Canvas(window, width=window_dim, height=window_dim)
    canvas.pack()
    #Build the grid
    for line_num in range(1,drop_density+1):
        canvas.create_line(line_num*drop_space,0,line_num*drop_space,window_dim,fill="gray80",width=1)
        canvas.create_line(0,line_num*drop_space,window_dim,line_num*drop_space,fill="gray80",width=1)
    #Add the drops
    for drop_cols in range(1,drop_density+1):
        for drop_rows in range(1,drop_density+1):
            drop_handle=canvas.create_oval(drop_cols*drop_space, drop_rows*drop_space, drop_cols*drop_space, drop_rows*drop_space, outline="gray30")
            drops.append([drop_handle,2])
    while (True):
        drops_to_clear=[]#Once a number is added here, all drops below are reduced to zero radius and not checked
        for count in range (drops_per_loop): #increase random drops per loop, replacing new ones with old
            index=random.randint(0,drop_density*drop_density-1)
            drop=drops[index]
            col=index%drop_density +1
            row=int(index/drop_density)
            size=drop[1]
            drop_handle=drop[0]
            size+=drop_radius_increase
            if (size>=max_size): #delete all below
                drops_to_clear.append([col,index])
                size=0
            canvas.delete(drop_handle)
            drop_handle=canvas.create_oval((col*drop_space)-size, row*drop_space-size,int(col*drop_space)+size, row*drop_space+size, outline="gray30", width=1)
            drops[index]=[drop_handle,size]
        #Now we clear all those below those reset due to size change
        for index,drop in enumerate(drops):
            drop=drops[index]
            col=index%drop_density +1
            for big_drop in drops_to_clear:
                if below_drop(big_drop,[col,index]):
                    drop_handle=drop[0]
                    canvas.delete(drop_handle)
                    drop_handle=canvas.create_oval(col*drop_space, (index/drop_density)*drop_space,col*drop_space, (index/drop_density)*drop_space)
                    drops[index]=[drop_handle,0]
        window.update() 
        time.sleep(.1)
   
   
let_it_rain()
