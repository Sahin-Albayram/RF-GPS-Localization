from beacon import Beacon
import random
from node import Node
import numpy as np


class Simulation:
    def __init__(self,cfg):
        self.cfg = cfg # every cfg is taking config from config.yaml you can go check there
        self.alpha = cfg["sim"]["alpha"] # alpha 
        self.pl0 = cfg["sim"]["pl0"] # loss 0
        self.ptx = cfg["sim"]["ptx"] # transmitter power
        self.gnss_err = cfg["sim"]["gnss"] # gps error margin (in cm)
        self.alt_err = cfg["sim"]["altitude"] # barometer error margin (in cm)
        self.create_beacons()
        self.create_nodes()
        self.thetas = self.simulate()
        
    def simulate(self):
        self.b_to_b() # beacon to beacon signal check to determine alpha value of environment
        self.theta = None  # theta values of node 
        for _ in range(1000): # take 1000 time
            if self.theta == None:
                self.theta = self.b_to_node() 
            else:
                for i in range(len(self.theta)): # for each node
                    self.theta[i] += self.b_to_node()[i] 

        for i in range(len(self.theta)): # for each node
            self.theta[i] = self.theta[i]/1000

        for i in range(len(self.theta)):
            print(round(self.theta[i][0],2), end= " ")
        print(" ")
        for i in range(len(self.theta)):
            print(round(self.theta[i][1],2), end= " ")
        print(" ")
        for i in range(len(self.theta)):
            print(round(self.theta[i][2],2), end= " ")
        print(" ")



    def create_beacons(self): # Create beacons (drones)
        beacon_cfg = self.cfg["beacon"]
        self.beacons = []
        for i in range(beacon_cfg["num_beacon"]):
            beacon = Beacon(beacon_cfg["x"][i],beacon_cfg["y"][i],beacon_cfg["z"][i],self.gnss_err,self.alt_err)
            self.beacons.append(beacon)


    def create_nodes(self): # Create nodes
        node_cfg = self.cfg["node"]
        self.nodes = []
        for i in range(node_cfg["num_node"]):
            node = Node(node_cfg["x"][i],node_cfg["y"][i],node_cfg["z"][i])
            self.nodes.append(node)


    def send_signal(self,x1,y1,z1,x2,y2,z2): # simulating signal power 
        loss = self.pl0 + 10 * self.alpha * np.log10(self.find_distance(x1,y1,z1,x2,y2,z2)) + np.random.normal(0,1)
        prx = self.ptx - loss
        return prx

    def find_distance(self,x1,y1,z1,x2,y2,z2): # distance between two point
        return (np.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2))
    
    def b_to_node(self): # beacon to node signal checking and distance calculation
        nodes_theta = []
        for node in self.nodes:
            thetas = [0,0,0,0,0]
            for _ in range(10):
                x_mcd = []
                y_mcd = []
                z_mcd = []
                prx_values = []
                for beacon in self.beacons:
                    x1,y1,z1 = beacon.coord()
                    x2,y2,z2 = node.coord()
                    prx = self.send_signal(x1,y1,z1,x2,y2,z2)
                    prx_values.append(prx)
                    x_mcd.append(x1)
                    y_mcd.append(y1)
                    z_mcd.append(z1)
                N_MCD = len(x_mcd)
                x_mcd = np.array(x_mcd)
                y_mcd = np.array(y_mcd)
                z_mcd = np.array(z_mcd)


                prx_arr = np.array(prx_values)

                A = np.column_stack((2 * x_mcd, 2* y_mcd, 2* z_mcd ,10 ** ((- self.pl0 - prx_arr) / (5 * self.calculated_alpha))
                                    ,-1*np.ones(N_MCD)))
                b = np.array([xi**2 + yi**2 + zi**2 for xi, yi,zi in zip(x_mcd, y_mcd, z_mcd)])
                # print(A)
                theta, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
                thetas += theta
            nodes_theta.append(thetas/10)
            #print(thetas/10)
        return nodes_theta

    def b_to_b(self): # beacon to beacon signal checking for alpha calculation
        alpha_sum = 0
        count = 0
        for _ in range(10):
            for i in range(len(self.beacons)-1):
                for j in range(i+1,len(self.beacons)):
                    count +=1
                    b1 = self.beacons[i]
                    b2 = self.beacons[j]
                    x1,y1,z1 = b1.coord()
                    x2,y2,z2 = b2.coord()
                    prx = self.send_signal(x1,y1,z1,x2,y2,z2)

                    loss = self.ptx - prx


                    x1,y1,z1 = b1.coord()
                    x2,y2,z2 = b2.coord()
                    alpha = (loss - self.pl0)/(10 * np.log10(self.find_distance(x1,y1,z1,x2,y2,z2)))
                    alpha_sum += alpha
        self.calculated_alpha = alpha_sum/count

    


