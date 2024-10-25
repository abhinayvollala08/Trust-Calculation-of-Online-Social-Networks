import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import timeit

global filename, abc_time, firefly_time, mabc_time, keys
graph = {}
cost = 0
graph_size = 0
mabc_worker_bee = {}
trust1 = 0
trust2 = 0
trust3 = 0

main = tkinter.Tk()
main.title("A New Model for Calculating the Maximum Trust in Online Social Networks using ABC, Firefly & MABC")
main.geometry("1300x1200")

def uploadDataset():
    text.delete('1.0', END)
    global filename, dataset, graph
    graph.clear()
    filename = filedialog.askopenfilename(initialdir="Dataset")
    status.config(text = filename+" loaded")

    with open(filename, "r") as file:
        for line in file:
            line = line.strip('\n')
            line = line.strip()
            arr = line.split(",")
            user = arr[0].strip()
            friend = arr[1].strip()
            if user in graph.keys():
                graph[user].append(friend)
            else:
                temp = []
                temp.append(friend)
                graph[user] = temp
    file.close()
    for key, value in graph.items():
        text.insert(END,"User : "+key+" Friends List : "+str(value)+"\n")
    text.update_idletasks()

'''
ABC is also a nature inspired algorithm where employee bee search for food in neighbours and then inform to ONLOOKER bee, this bee will watch waggle dance of
employee bees to compute fitness values and if fitness is more then they will move in that more fitness path, if fitness less then it will choose new random path,
ABC will suffer heavy computation time due to random path selection
'''
def runABCAlgorithm(src, des):
    try:
        global cost, graph_size
        key = list(graph)
        if src in graph.keys():
            friends = graph[src]#get friend list from given source and if source not found in graph then take a random source node who can reach destination
        else:
            found = True
            while found:
                random_path = random.randint(0, len(graph))#get random id
                paths = list(graph)
                src = paths[random_path] #get random source from the graph path
                if src in graph.keys(): #compute fitness if source found in graph anf if not found then continue finding new paths
                    friends = graph[src]
                    found = False     #if source found then break loop   
        if des in friends: #if destination found then break loop and get friends size as graph length
            graph_size += len(friends)
            return True
        else: #if destination not found then continue loop and increas cost value as this source having more friends and can be trusted
            graph_size += len(friends)
            for i in range(len(friends)):
                cost = cost + 1
                return runABCAlgorithm(friends[i], des)                
    except Exception:
        return False
    
def runABC():
    text.delete('1.0', END)
    global abc_time, cost, graph_size, trust1
    trust1 = 0
    cost = 0
    graph_size = 0
    src = tf1.get()
    des = tf2.get()
    start = timeit.default_timer()
    flag = runABCAlgorithm(src,des)
    end = timeit.default_timer()
    abc_time = end - start
    time = '{:f}'.format(abc_time)
    cost = cost/graph_size
    print("abc "+str(cost))
    if cost > 0.0054:
        trust1 = 1
        text.insert(END,"ABC Output : Source : "+src+" & Destination : "+des+" Cost Value : "+str(cost)+"\n")
        text.insert(END,"ABC Computation Time : "+str(time)+"\n\n")
    else:
        text.insert(END,"ABC Output : Source : "+src+" & Destination : "+des+" Cost Value : "+str(cost)+"\n")
        text.insert(END,"ABC Computation Time : "+str(time)+"\n\n")

'''
firefly is a nature inspired algorithm which attract other firefly using their lights, lights intensity will get weaker if distance/fitness value more and
can receive strong light intensity if distance is less and based on this distance all firefly will move to optimize path.
In trust calculation optimized function will keep moving to next index with greater chances of finding path between source and destination and once path found
then optimization will stop. Firefly is superior to ABC as it move towards next position without taking any random path. ABC execution time is more due to
random path movement to get optimized solution
'''
def firefly(src, des, keys, index):
    try:
        global cost, graph_size
        if src in graph.keys(): #if friends found in source path then continue path to get destination
            friends = graph[src]
        else: #if not found then firefly (users) continue scanning next path till found source
            found = True
            while found: 
                src = keys[index]
                index += 1
                if src in graph.keys(): #if source found then search for destination and compute cost
                    friends = graph[src]
                    found = False               
        if des in friends: #if destination found then terminate loop
            graph_size += len(friends)
            return True
        else: #if not found then continue scanning path till destination found and increase cost value
            graph_size += len(friends)
            for i in range(len(friends)): 
                cost += 1
                return firefly(friends[i], des, keys, index)                
    except Exception:
        return False    


def runFirefly():
    global firefly_time, trust2
    global cost, graph_size, keys
    trust2 = 0
    cost = 0
    graph_size = 0
    src = tf1.get()
    des = tf2.get()
    start = timeit.default_timer()
    keys = list(graph)
    flag = firefly(src,des,keys,0)
    end = timeit.default_timer()
    firefly_time = end - start
    time = '{:f}'.format(firefly_time)
    cost = cost/graph_size
    print("fire "+str(cost))
    if cost > 0.010:
        text.insert(END,"Firefly Output : Source  : "+src+" & Destination : "+des+" Cost Value : "+str(cost)+"\n")
        text.insert(END,"Firefly Computation Time : "+str(time)+"\n\n")
        trust2 = 1
    else:
        text.insert(END,"Firefly Output : Source  : "+src+" & Destination : "+des+" Cost Value : "+str(cost)+"\n")
        text.insert(END,"Firefly Computation Time : "+str(time)+"\n\n")


'''
MABC make worker bee to memorize previous solution and for next search it will get optimized result from memory dont have result then it will invoke
firefly algorithm to get optimized result and then memorize that result for future use 
'''
def MABC(src, des, keys, index):
    global graph_size, cost
    if src+","+des in mabc_worker_bee.keys(): #check source and destination cost in the memory and if exists then send result  
        cost = mabc_worker_bee[src+","+des]
        return True
    else: #if not exists then invoke firefly to find path and then add result path and cost values to memory
        flag = firefly(src, des, keys, index)
        data = []
        cost = cost / graph_size
        data.append(cost)
        mabc_worker_bee[src+","+des] = data #add result to memory for giveb source and destination
        return flag

def runMABC():
    global mabc_time
    global cost, graph_size, keys, trust3
    trust3 = 0
    src = tf1.get()
    des = tf2.get()
    start = timeit.default_timer()
    flag = MABC(src,des,keys,0)
    end = timeit.default_timer()
    mabc_time = end - start
    time = '{:f}'.format(mabc_time)
    print("mabc "+str(cost)+"\n")
    if cost > 0.010:
        text.insert(END,"MABC Output : Source  : "+src+" & Destination : "+des+" Cost Value : "+str(cost)+"\n")
        text.insert(END,"MABC Computation Time : "+str(time)+"\n\n")
        trust3 = 1
    else:
        text.insert(END,"MABC Output : Source  : "+src+" & Destination : "+des+" Cost Value : "+str(cost)+"\n")
        text.insert(END,"MABC Computation Time : "+str(time)+"\n\n")
    if trust1 == 1 and trust2 == 1 and trust3 == 1:
        text.insert(END,"Both source & destination are TRUSTED USERS\n")
    else:
        text.insert(END,"Both source & destination are UNTRUSTED USERS\n")

def comparisonGraph():
    height = [abc_time, firefly_time, mabc_time]
    bars = ('ABC', 'Firefly', 'MABC')
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height)
    plt.xticks(y_pos, bars)
    plt.xlabel("Algorithm Names")
    plt.ylabel("Computation Time")
    plt.title("All Algorithms Computation Time Graph")
    plt.show()

def close():
    main.destroy()

font = ('times', 12, 'bold')
title = Label(main, text='A New Model for Calculating the Maximum Trust in Online Social Networks using ABC, Firefly & MABC',anchor=W, justify=CENTER)
title.config(bg='yellow4', fg='white')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)
    
font1 = ('times', 13, 'bold')

upload = Button(main, text="Upload Facebook Dataset", command=uploadDataset)
upload.place(x=10,y=100)
upload.config(font=font1)  
    
status = Label(main, text='')
status.config(font=font1)
status.place(x=230,y=100)
    
l1 = Label(main, text='Source User')
l1.config(font=font1)
l1.place(x=10,y=150)

tf1 = Entry(main,width=10)
tf1.config(font=font1)
tf1.place(x=230,y=150)

l2 = Label(main, text='Destination User')
l2.config(font=font1)
l2.place(x=10,y=200)

tf2 = Entry(main,width=10)
tf2.config(font=font1)
tf2.place(x=230,y=200)

b1 = Button(main, text = "Run ABC Algorithm", command=runABC)
b1.config(font=font1)
b1.place(x=10,y=250)
    
b2 = Button(main, text = "Run Firefly Algorithm", command=runFirefly)
b2.config(font=font1)
b2.place(x=230,y=250)

b3 = Button(main, text = "Run MABC Algorithm", command=runMABC)
b3.config(font=font1)
b3.place(x=470,y=250)

b4 = Button(main, text = "Comparison Graph", command=comparisonGraph)
b4.config(font=font1)
b4.place(x=690,y=250)

b5 = Button(main, text = "Exit", command=close)
b5.config(font=font1)
b5.place(x=880,y=250)

text=Text(main,height=15,width=120)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=10,y=300)
text.config(font=font1)
    
main.config(bg='magenta3')
main.mainloop()
    














    
