#!/usr/bin/env python
# coding: utf-8

# In[1]: Importing Libraries
from IPython import get_ipython
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from math import cos, sin, pi
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:Finding Distance using distance formula
def distance(p1,p2):
    dx = p1[0]-p2[0]
    dy = p1[1]-p2[1]
    distance = np.sqrt(dx*dx+dy*dy)
    return distance
# In[3]: Finding Circle intersections and handling them
def circle_intersection(circle1, circle2): 
    x1,y1,r1 = circle1
    x2,y2,r2 = circle2
    dx,dy = x2-x1,y2-y1
    d = np.sqrt(dx*dx+dy*dy)
    #d = distance([x1,y1],[x2,y2])
    
    # non-overlapping circles
    if d >= r1+r2:
        return (( (d+r1-r2)/(2*d)*(x2-x1)+x1, (d+r1-r2)/(2*d)*(y2-y1)+y1 ),) 

    # one circle inside another
    elif r1 > (d+r2) or r2 > (d+r1):
        if dx == 0: angle = pi/2
        else: angle = np.arctan(dy/dx)
        p11 = [ x1+r1*cos(angle), y1+r1*sin(angle) ]
        p12 = [ x1-r1*cos(angle), y1-r1*sin(angle) ]
        p21 = [ x2+r2*cos(angle), y2+r2*sin(angle) ]
        p22 = [ x2-r2*cos(angle), y2-r2*sin(angle) ]
        
        point_set = [[p11,p21],[p11,p22],[p12,p21],[p12,p22]]
        
        dist_set = [distance(item[0],item[1]) for item in point_set]
        points = point_set[np.argmin(dist_set)]
        points = np.array(points)
        points = sum(points)/len(points)

        return (points,)
    
    # overlapping circles
    else:
        a = (r1*r1-r2*r2+d*d)/(2*d)
        h = np.sqrt(r1*r1-a*a)
        xm = x1 + a*dx/d
        ym = y1 + a*dy/d
        xs1 = xm + h*dy/d
        xs2 = xm - h*dy/d
        ys1 = ym - h*dx/d
        ys2 = ym + h*dx/d

        return (xs1,ys1),(xs2,ys2)
# In[4] Plot Function
def plot(cs):
   
    cmap = cm.plasma
    
    fig, ax = plt.subplots() 
    ax.set(xlim=[-10, 10], ylim=[-10, 10], aspect=1)
    
    for i,c in enumerate(cs):
        ax.add_artist(plt.Circle(c[:2], c[2], color=cmap(i/len(cs)), alpha=0.5))
        ax.plot(c[0], c[1], 'or')

    return fig, ax

# In[5]: Choosing point Function
def choose_point(points, circle, order):
    distance = ()
    for point in points:
        dx = point[0]-circle[0]
        dy = point[1]-circle[1]
        dist = np.sqrt(dx*dx+dy*dy) - circle[2] 
        distance = distance + (dist,)
    
    arg = np.argmin([abs(i) for i in distance])
    choosen_point = points[arg]
    # ref_point = point on c3 perimeter closest to choosen_point
    ref_point = [circle[0]+(choosen_point[0]-circle[0])*circle[2]/(circle[2]+distance[arg]), 
                 circle[1]+(choosen_point[1]-circle[1])*circle[2]/(circle[2]+distance[arg])]
    result = [((order-1)*choosen_point[0]+ref_point[0])/order, ((order-1)*choosen_point[1]+ref_point[1])/order]
        
    return result


# In[6]: Trilateration Function
def trilateration(c1, c2, c3):
    
    points = circle_intersection(c1, c2)
    result = choose_point(points, c3, 3)
    
    fig, ax = plot([c1, c2, c3])
    ax.plot(result[0], result[1], "*")
    return result


# In[7]: Trial Values

# c1 = (3.8635, 5.872, 0)
# c2 = (7.727, 2.936, 0)
# c3 = (3.8635, 0, 0)
# # c4 = (0, 2.936, 0)

# trilateration(c1, c2, c3)


# In[8]: Trilateration function 2
def trilateration2(c1, c2, c3):
    circles = [c1,c2,c3]
    results = []
    for i in range(3):
        first = circles[0]
        circles.pop(0)
        circles.append(first)
    
        points = circle_intersection(circles[0], circles[1])
        result = choose_point(points, circles[2], 3)
        results.append(result)
     
    results = np.array(results)
    location = sum(results)/len(results)
    
    fig, ax = plot([c1, c2, c3])
    ax.plot(location[0],location[1], "*")
    return location


# In[9]:


# c1 = (3.8635, 5.872, 0)
# c2 = (7.727, 2.936, 0)
# c3 = (3.8635, 0, 0)

c1 = (0.3833,0.9627,0)
c2 = (0.3416,0.9627,0)
c3 = (0.3833,1.0802,0)

trilateration2(c1, c2, c3)


# In[ ]:




