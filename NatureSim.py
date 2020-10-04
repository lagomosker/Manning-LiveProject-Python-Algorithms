
import tkinter, time, random

def let_it_rain():
    drops=[]
    window = tkinter.Tk()
    window.geometry("1000x1000")
    window.title("Rain on a window")
    window.configure(background="white")
    canvas=tkinter.Canvas(window, width=1000, height=1000)
    canvas.pack()
    #Build the grid
    for line_num in range(1,20):
        canvas.create_line(line_num*49,0,line_num*49,1000,fill="grey",width=1)
        canvas.create_line(0,line_num*49,1000,line_num*49,fill="grey",width=1)
    #Build 
    for drop_cols in range(1,20):
        drop_row=[]
        for drop_rows in range(1,20):
            drop_handle=canvas.create_oval(drop_cols*49-1, drop_rows*49-1, drop_cols*49+1, drop_rows*49+1, fill="red", width=1)
            drop_row.append([drop_handle,2]) #initial diameter 2 drop
        drops.append(drop_row)
    window.mainloop()

let_it_rain()