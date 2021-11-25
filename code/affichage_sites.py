from util import *
import matplotlib.pyplot as plt

def liste_voisins(in_data):
    v = in_data['siteSiteDistances'] 
    for i in range(len(v)):
        for j in range(len(v[i])):
            v[i][j] = (v[i][j],j)
        v.sort()
    return v

def affichage(in_data):
    coord_s = in_data['sites']
    x_coord_s = []
    y_coord_s = []
    for x,y in coord_s:
        x_coord_s.append(x)
        y_coord_s.append(y)
    
    coord_c = in_data['clients']
    x_coord_c = []
    y_coord_c = []
    for d,(x,y) in coord_c:
        x_coord_c.append(x)
        y_coord_c.append(y)

    plt.scatter(x_coord_c,y_coord_c)
    plt.scatter(x_coord_s,y_coord_s)
    
    plt.show()