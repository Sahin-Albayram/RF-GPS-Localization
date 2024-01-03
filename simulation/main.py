
#! conda install yaml
import numpy as np
import yaml
from node import Node
from beacon import Beacon
from sim import Simulation



with open("simulation/config.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile,Loader=yaml.FullLoader)


# nodes = [[100,200,100],[1000,500,1000]]
# beacons = [[-200,1000,200],[300,0,300] ,[500,400,500],[800,900,800],[0,0,0]]
# pl0 = 40
# ptx = 30
# alpha = 2
# def find_distance(x1,y1,z1,x2,y2,z2):
#     return (np.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2))

# def send_signal(x1,y1,z1,x2,y2,z2):
#     loss = pl0 + 10 * alpha * np.log10(find_distance(x1,y1,z1,x2,y2,z2)) #+ np.random.normal(0,1)
#     prx = ptx - loss
#     return prx

# print(find_distance(0,0,0,10,10,10))
# print(send_signal(0,0,0,10,10,10))
# for node in nodes:
#     thetas = [0,0,0,0,0]
    
#     x_mcd = []
#     y_mcd = []
#     z_mcd = []
#     prx_values = []
#     for beacon in beacons:
#         x1,y1,z1 = beacon[0],beacon[1],beacon[2]
#         x2,y2,z2 = node[0],node[1],node[2]
#         prx = send_signal(x1,y1,z1,x2,y2,z2)
#         prx_values.append(prx)
#         x_mcd.append(x1)
#         y_mcd.append(y1)
#         z_mcd.append(z1)
#     N_MCD = len(x_mcd)
#     x_mcd = np.array(x_mcd)
#     y_mcd = np.array(y_mcd)
#     z_mcd = np.array(z_mcd)

#     prx_arr = np.array(prx_values)

#     A = np.column_stack((2 * x_mcd, 2* y_mcd, 2*z_mcd , 10 ** ((- pl0 - prx_arr) / (5 * alpha))
#                         ,-1*np.ones(N_MCD)))
#     b = np.array([xi**2 + yi**2 + zi**2 for xi, yi,zi in zip(x_mcd, y_mcd,z_mcd)])
#     # print(A)
#     theta, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
#     thetas += theta
#     thetas/10
#     print(theta)
# Print the estimated position and any residuals (error metrics)


sim = Simulation(cfg)

