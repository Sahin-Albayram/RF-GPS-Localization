import random
import numpy as np
class Beacon:
    def __init__(self,x,y,z,gnss_err,alt_err):
        self.x = x
        self.y = y
        self.z = z
        self.gnss_err = gnss_err
        self.alt_err= alt_err
        self.get_error()
    


    def coord(self):
        err1 = np.random.normal(0,1)*5
        err2 = np.random.normal(0,1)*5
        err3 = np.random.normal(0,1)*5
        #err1,err2,err3 = 0,0,0
        return self.nx+err1, self.ny+err2 ,self.nz+err3
    
    def get_error(self):

        err = random.randrange(-self.alt_err,self.alt_err)
        err1 = random.randrange(-self.gnss_err,self.gnss_err)
        err2 = random.randrange(-self.gnss_err,self.gnss_err)


        self.nz = self.z+err
        self.nx = self.x+err1
        self.ny = self.y+err2