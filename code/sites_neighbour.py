from util import *

def liste_voisins(in_data):
    v = in_data['siteSiteDistances'] 
    for i in range(len(v)):
        for j in range(len(v[i])):
            v[i][j] = (v[i][j],j)
        v.sort()
    return v

