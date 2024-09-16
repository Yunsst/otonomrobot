from Bitirme_pathfinding.HybridAstarPlanner import hybrid_astar as planner
from Bitirme_pathfinding.HybridAstarPlanner import yaw as yw
from Bitirme_pathfinding.HybridAstarPlanner import circle
import numpy as np
import math

def pathplanner(c_x,c_y,c_yaw,x_g,y_g,yaw_g):
    x,y,yaw,direction = planner.call_Path(c_x,c_y,c_yaw,x_g,y_g,yaw_g)
    intervals = yw.find_yaw_intervals(yaw)
    infos=[]
    for i in intervals:
        r=0
        x_n = x[i[0]:i[1]]
        y_n = y[i[0]:i[1]]

        first_arg = x[i[1]] - x[i[0]]
        last_arg = y[i[1]] - y[i[0]]
        r=np.sqrt((first_arg*first_arg)+(last_arg*last_arg))

        if i[2]!=0:
            coords= np.array([x_n,y_n]).T 
            r = circle.least_squares_circle(coords)
        first_arg = math.degrees(yaw[i[0]])
        last_arg = math.degrees(yaw[i[1]])
        infos.append([first_arg,last_arg,r,i[2],x[i[0]],y[i[0]]])
    return infos
