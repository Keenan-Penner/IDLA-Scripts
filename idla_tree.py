import random as rd
import matplotlib.pyplot as plt

## PRELIMINARY FUNCTIONS

def sum_list(L1,L2):
    S=[]
    for i in range(len(L1)):
        S.append(L1[i]+L2[i])
    return S

def diff_list(L1,L2):
    S=[]
    for i in range(len(L1)):
        S.append(L1[i]-L2[i])
    return S

def movement(L,p): 

    if p<0.25:##right##
        
        newposition=sum_list(L[0],[1,0])
        L.append([1,0])
    
    
    elif 0.25<=p<0.5:##left##
        
        newposition=sum_list(L[0],[-1,0])
        L.append([-1,0])
    
    elif 0.5<=p<0.75:##up##
        
        newposition=sum_list(L[0],[0,1])
        L.append([0,1])
    
    else:##down##
        
        newposition=sum_list(L[0],[0,-1])
        L.append([0,-1])

    return L, newposition

def prev(L,p):
    if p<0.25:
        previous=sum_list(L, [-1,0])
    elif 0.25<=p<0.5:
        previous=sum_list(L, [1,0])
    elif 0.5<=p<0.75:
        previous=sum_list(L, [0,-1])
    else:
        previous=sum_list(L, [0,1])
    return previous

def idla(n):
    L=[[0,0]]
    aretes=[]
    count=1
    while count<n:
        
        p=rd.random()
        move=movement([[0,0]],p)[1]
        
        while move in L:
            p=rd.random()
            move=movement([move],p)[1]    
            
        if move not in L:
            previous=prev(move,p)
            L.append(move)
            aretes.append([previous,move])
            count+=1
    return L,aretes


## PLOT 2D TREE

'''A=idla(30000)
for i in range(len(A)):
    plt.plot([A[i][0][0],A[i][1][0]],[A[i][0][1],A[i][1][1]],linewidth=0.5)
    plt.axis('square')
    plt.axis('off')
plt.show()
plt.savefig('IDLA_tree_30000.png', dpi=500)'''



## 2D TREE WITH COLORED BRANCH 

def branch(aretes,point):
    B=[]
    rev=reverse(aretes)
    for i in range(len(rev)):
        if rev[i][1]==point:
            B.append(rev[i])
            point=rev[i][0]
    return B
            
        

def reverse(aretes):
    L=[]
    for i in range( len(aretes) - 1, -1, -1) :
        L.append(aretes[i])
    return L

def branchplot(n):
    A=idla(n)
    point=A[0][-1]
    aretes=A[1]
    Branch=branch(aretes,point)
    for i in range(len(aretes)):
        plt.plot([aretes[i][0][0],aretes[i][1][0]],[aretes[i][0][1],aretes[i][1][1]],linewidth=0.5,color='blue')
    for i in range(len(Branch)):
        plt.plot([Branch[i][0][0],Branch[i][1][0]],[Branch[i][0][1],Branch[i][1][1]],linewidth=0.5,color='red')
    plt.axis('square')
    plt.show()
    plt.savefig('branchtest.png', dpi=500)


### 3D TREE 


def movement_bis(L,p): #from a given position, gives the new position 

    if p<1/6:
        
        newposition=sum_list(L[0],[1,0,0])
        L.append([1,0,0])
    
    
    elif 1/6<=p<1/3:
        
        newposition=sum_list(L[0],[-1,0,0])
        L.append([-1,0,0])
    
    elif 1/3<=p<1/2:
        
        newposition=sum_list(L[0],[0,1,0])
        L.append([0,1,0])
    
    elif 1/2<=p<2/3:
        
        newposition=sum_list(L[0],[0,-1,0])
        L.append([0,-1,0])
    
    elif 2/3<=p<5/6:
       
        newposition=sum_list(L[0],[0,0,1])
        L.append([0,0,1])
        
    else:
    
        newposition=sum_list(L[0],[0,0,-1])
        L.append([0,0,-1])

    return L, newposition

def previous(L,p):
    if p<1/6:
        previous=sum_list(L, [-1,0,0])
    elif 1/6<=p<1/3:
        previous=sum_list(L, [1,0,0])
    elif 1/3<=p<1/2:
        previous=sum_list(L, [0,-1,0])
    elif 1/2<=p<2/3:
        previous=sum_list(L, [0,1,0])
    elif 2/3<=p<5/6:
        previous=sum_list(L, [0,0,-1])
    else:
        previous=sum_list(L, [0,0,1]) 
    return previous

def idla3(n):
    L=[[0,0,0]]
    aretes=[]
    count=1
    while count<n:
        
        p=rd.random()
        move=movement_bis([[0,0,0]],p)[1]
        
        while move in L:
            p=rd.random()
            move=movement_bis([move],p)[1]    
            
        if move not in L:
            prev=previous(move,p)
            L.append(move)
            aretes.append([prev,move])
            count+=1
    return aretes

## PLOT 3D TREE



'''A=idla3(1000)

ax=plt.axes(projection="3d")
ax.set_box_aspect([1,1,1])


for i in range(len(A)):
    ax.plot([A[i][0][0],A[i][1][0]],[A[i][0][1],A[i][1][1]],[A[i][0][2],A[i][1][2]],linewidth=2)
plt.axis('off')
plt.show()
plt.savefig('IDLA_tree_3D_1.png', dpi=500)'''

