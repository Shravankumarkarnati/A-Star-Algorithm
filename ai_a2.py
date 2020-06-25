#!/usr/bin/env python
# coding: utf-8

from natsort import natsorted as ns
import math
import random
import sys
import warnings
warnings.filterwarnings("ignore")

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import seaborn.apionly as sns
import matplotlib.animation
from IPython.display import HTML    

plt.style.use('seaborn-pastel')


def locations():
    locations = open("locations.txt","r")
    locations = (locations.readlines())
    loc = dict()
    for i in locations:
        if(i.split()[0]!='END'):
            loc[str(i.split()[0])]=(int(i.split()[1]),int(i.split()[2]))
    return loc


def connections():
    connections = open("connections.txt","r")
    connections = connections.readlines()
    con = dict()
    for i in connections:
        if(i.split()[0]!='END'):
            lists = []
            for j in range (int(i.split()[1])):
                lists.append(str(i.split()[j+2]))
            con[str(i.split()[0])] = lists
    return con


def eud(p1,p2):
    ecdist = math.sqrt(sum([(x1 - x2) ** 2 for x1, x2 in zip(cord[p1], cord[p2])]))
    return round(ecdist,2)

def pathdist_SL(pathNow):
    total = 0
    for i in range(len(pathNow)-1):
        press = pathNow[i:i+2]
        pressDist = round(eud(press[0],press[1]),2)
        print(press[0]+" to "+ press[1] +" length " + str(pressDist) +", ")
        total+=pressDist
    print("\n Total path length " + str(round(total,2)))
    print('\n')


def pathdist_LH(pathNow):
    total = 0
    prime = True
    for i in range(len(pathNow)-1):
        press = pathNow[i:i+2]
        if prime :
            pressDist = 2
        else:
            pressDist = 1
        prime = False
        print(press[0]+" to "+ press[1] +" length " + str(pressDist) +", ")
        total+=pressDist
    print("\n Total path length " + str(total))
    print('\n')

    
    
def rem_nodes(nodes):
    mul = []
    for k in nodes:
        if k not in adj_list:
            print("No Node in the graph as: " +k)
            mul.append(k)
    for m in mul:
        nodes.remove(m)
    for i in nodes:
        for j in adj_list[i]:
            adj_list[j].remove(i)
        adj_list[i]=[]    
        

def path_SL(start,end,flag):
    global dist,path_list,stp,anim_SL,trav_path_SL
    stp={}
    dist={}
    path_list =[]
    trav_path_SL = []
    anim_SL = {0:[[]]}
    path_list.append(start)
    for i in adj_list:
        dist[i]=[math.inf,math.inf,False,None]
    dist[start]=[eud(start,end),0,False,start]
    n = start
    while(n!=end):
        n =sld_trav(n,end,flag)
        path_list.append(n)
        trav_path_SL.append([dist[n][3],n])
    if flag:
        print("\n\n Destination Reached: "+end)
    f=dist[end][3]
    path=[end]
    while(f!=start):
        path.append(f)
        f=dist[f][3]
    path.append(start)
    path.reverse()
    return path,anim_SL,trav_path_SL


def sld_trav(cur_node,end,fl):
    l=len(anim_SL)
    anim_SL[l]=[[]]
    list_Now = adj_list[cur_node]
    if fl:
        print("\n")
        print("\n City Selected : "+ cur_node)
        print("\n Possible cities to where to travel : " + str(list_Now))
        print("\n Cities at the end of possible paths :",end="  ")
    if cur_node in stp:
        del stp[cur_node]
    for i in adj_list[cur_node]:
        if dist[i][2] == False:
            d_start=dist[cur_node][1]+eud(cur_node,i)
            d_est=d_start+eud(i,end)
            if(dist[i][0]>d_est):
                dist[i][0]=d_est
                dist[i][1]=d_start
                dist[i][3] = cur_node
                stp[i] = d_est
                anim_SL[l].append([cur_node,i])

    if fl:
        for i in stp:
            print(i+"("+str(round(stp[i],2))+")",end=" ")
    dist[cur_node][2] = True
    min_values = {}
    for j in dist:
        if dist[j][2] == False:
            min_values[j]=dist[j][0]
    
    temp = min(min_values.values()) 
    res = [key for key in min_values if min_values[key] == temp] 
    return res[0]


def path_LH(start,end,flag):
    global dist_lh,path_list,stp_lh,anim_LH,trav_path_LH
    stp_lh={}
    dist_lh={}
    path_list =[]
    anim_LH={0:[[]]}
    trav_path_LH = []
    path_list.append(start)
    for i in adj_list:
        dist_lh[i]=[math.inf,math.inf,False,None]
    dist_lh[start]=[0,0,False,start]
    n = start
    while(n!=end):
        n =lh_trav(n,end,flag)
        path_list.append(n)
        trav_path_LH.append([dist_lh[n][3],n])
    if flag:
        print("\n\n Destination Reached: "+end)
    f=dist_lh[end][3]
    path=[end]
    while(f!=start):
        path.append(f)
        f=dist_lh[f][3]
    path.append(start)
    path.reverse()
    return path,anim_LH,trav_path_LH

        
def lh_trav(cur_node,end,fl):
    l=len(anim_LH)
    anim_LH[l]=[[]]
    list_Now = adj_list[cur_node]
    if fl:
        print("\n")
        print("\n City Selected : "+ cur_node)
        print("\n Possible cities to where to travel : " + str(list_Now))
        print("\n Cities at the end of possible paths :",end="  ")
    if cur_node in stp_lh:
        del stp_lh[cur_node]
    for i in adj_list[cur_node]:
        if dist_lh[i][2] == False:
            flag=2
            if i==end:
                flag=0
            else:
                for j in adj_list[i]:
                    if j == end:
                        flag=1
            d_start=dist_lh[cur_node][1]+1
            d_est=d_start+flag
            if(dist_lh[i][0]>d_est):
                dist_lh[i][0]=d_est
                dist_lh[i][1]=d_start
                dist_lh[i][3] = cur_node
                stp_lh[i] = d_est
                anim_LH[l].append([cur_node,i])
    if fl:
        for i in stp_lh:
            print(i+"("+str(stp_lh[i])+")",end=" ")
    dist_lh[cur_node][2] = True
    min_values = {}
    for j in dist_lh:
        if dist_lh[j][2] == False:
            min_values[j]=dist_lh[j][0]
    temp = min(min_values.values()) 
    res = [key for key in min_values if min_values[key] == temp]
    return res[0]
    
   
def pathdist_SL(pathNow):
    total = 0
    print("\n")
    for i in range(len(pathNow)-1):
        press = pathNow[i:i+2]
        pressDist = round(eud(press[0],press[1]),2)
        print(press[0]+" to "+ press[1] +" length " + str(pressDist) +", ")
        total+=pressDist
    print("\n Total path length " + str(round(total,2)))

    
def pathdist_LH(pathNow):
    total = 0
    print("\n")
    prime = True
    for i in range(len(pathNow)-1):
        press = pathNow[i:i+2]
        if prime :
            pressDist = 2
        else:
            pressDist = 1
        prime = False
        print(press[0]+" to "+ press[1] +" length " + str(pressDist) +", ")
        total+=pressDist
    print("\n Total path length " + str(total))
    
def removeDuplicates(lst): 
      return [t for t in (set(tuple(i) for i in lst))] 

# Code for edges for the graph
def find_edges():
    edges = []
    adj=connections()
    for i in adj:
        for j in adj[i]:
            edges.append((i,j))
    new_edges = []
    for i in edges:
        m = [i[0],i[1]]
        m = ns(m)
        i = (m[0],m[1])
        new_edges.append(i)
    new_edges = removeDuplicates(new_edges)
    return new_edges

        
def main():   
    global cord,adj_list,flag
    cord = locations()
    adj_list = connections()
    for i in adj_list:
        adj_list[i] = ns(adj_list[i])

    print("Enter the Initial Location:")
    start_city = input()
    while(start_city not in adj_list):
        print("No such Node. \nEnter the Initial Location:")
        start_city = input()
        
    print("Enter the Final Location:")
    end_city = input()
    while(end_city not in adj_list):
        print("No such Node. \n Enter the Final Location:")
        end_city = input()
    
    print("Initial Location : " + start_city + " \nFinal Location : " + end_city)
    
    print("Enter the locations that should not be included seperated by commas.")
    remove_nodes = input().split(",")
    if (remove_nodes[0]!=''):
        rem_nodes(remove_nodes)
        
    print("Enter output type: \n 1. Step by Step Option. \n 2. Just the solution path.")
    print_type = (input())
    while(print_type != "1" and print_type != "2"):
        print("No such type. \n Enter output type: \n 1. Step by Step Option. \n 2. Just the solution path.")
        print_type = (input())
    if(print_type == "1"):
        flag = True
    else:
        flag = False

    
    print("Enter the heuristic method number: \n 1. Straight Line Distances\n 2. Fewest Cities.")
    method_num = (input())
    while(method_num != "1" and method_num!= "2"):
        print("No such method. \n Enter the heuristic method number: \n 1. Straight Line Distances\n 2. Fewest Cities.")
        method_num=(input())
    
    
    if(len(adj_list[start_city])==0 or len(adj_list[end_city])==0):
        print("There is no path to find.")
        exit()
        
    else:
        if(method_num=="1"):
            print("Using Straight Line Distance Heuristic:")
            pathNow,anim_list,trav_path = path_SL(start_city,end_city,flag)
            print("\n \n Final Solution path is : ", end = "  ")
            print(pathNow)
            pathdist_SL(pathNow)
                
        else:
            print("Using Fewest Cities Heuristic:")
            pathNow,anim_list,trav_path = path_LH(start_city,end_city,flag)
            print("\n \n Final Solution path is : ", end = "  ")
            print(pathNow)
            pathdist_LH(pathNow)
        
        global path_whole,path_anim,all_nodes,trav_anim,goal_lead
        path_whole = anim_list
        path_anim=pathNow
        all_nodes = adj_list.keys()
        trav_anim = trav_path
        goal_lead=[]
        

if __name__ == '__main__':
    main()
  
goal_lead = [] 
# Create Graph
G=nx.Graph()
edges = find_edges()
G.add_nodes_from(all_nodes)
G.add_edges_from(edges)
pos = cord

# Build plot
fig, ax = plt.subplots(figsize=(20,20))  # plt.figure(3,figsize=(12,12)) 

def update(num):
    goal_lead=[]
    ax.clear()
    if num == 0:
        for e in G.edges():
            G[e[0]][e[1]]['color'] = '#8b8c8b'#gray

    elif num == len(path_whole):
        for j in goal_lead:
            G[j[0]][j[1]]['color']='#49fa02'#green
        for m in range(num-1):
            G[trav_anim[m][0]][trav_anim[m][1]]['color']='#ff0303'#red
        
    elif num==len(path_whole)+1:
        for e in G.edges():
            G[e[0]][e[1]]['color'] = '#8b8c8b'#gray
        for i in range(len(path_anim)-1):
            G[(path_anim[i])][(path_anim[i+1])]['color'] = '#49fa02' #final_green
    elif num == len(path_whole)+2:
        ax.clear()
    else:
        milds_new = []
        for ir in range(num):
            milds = path_whole[num]
            for i in milds:
                if len(i)!=0:
                    milds_new.append(i)
            goal_lead.extend(milds_new)
        for j in goal_lead:
            G[j[0]][j[1]]['color']='#49fa02'#green
        for m in range(num-1):
            G[trav_anim[m][0]][trav_anim[m][1]]['color']='#ff0303'#red
            
    edge_color_list = [G[e[0]][e[1]]['color'] for e in G.edges() ]
    nx.draw(G, edge_color = edge_color_list,   with_labels = True,pos= cord,node_color='#0c4778',node_size = 400,width =  2.0,ax =ax,font_size=10,font_color = 'white')
    
    ax.set_title("Path : "+ str(path_anim), fontweight="bold",fontsize = 15)
    ax.set_xticks([])
    ax.set_yticks([])
        
ani = matplotlib.animation.FuncAnimation(fig, update, frames=len(path_whole)+2, interval=1000, repeat=True,cache_frame_data = False)
# HTML(ani.to_html5_video())
plt.show()