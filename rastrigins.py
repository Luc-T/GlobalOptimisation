from multiprocessing.sharedctypes import Value
from matplotlib.pyplot import step
import numpy as np
import random


class Ras:
    
    def __init__(self, x1, x2):
        self.x1 = x1
        self.x2 = x2
        self.fitness = 1000

#getters and setters used 
    def get_x1(self):
        return self.x1

    def set_x1(self, value):
        
        self.x1 = value

    def get_x2(self):
        return self.x2

    def set_x2(self, value):
        
        self.x2 = value
    
    def get_fitness(self):
        return self.fitness

    def set_fitness(self, y):
        
        self.fitness = y
    
    
    def calc(self):
        y = 20 + (self.x1**2) + (self.x2**2) - 10*(np.cos((2*np.pi*self.x1)) + np.cos((2*np.pi*self.x2)))
        self.set_fitness(y)

    def set_prob(self, p):
        
        self.prob = p

    #functionality

    def get_prob(self):
        return self.prob

    def getStep(self):
        #find a direction (plus or minus)
        choice = bool(random.getrandbits(1))
        #how far is the increment?
        s = random.random()
        if choice:
            #positive
            return s
        elif ~choice:
            #negative
            return (-s)

    #change dna
    def modifyX1(self):
        mod = self.getStep()
        newx1 = self.get_x1() + mod
        self.set_x1(newx1)
    
    def modifyX2(self):
        mod = self.getStep()
        newx2 = self.get_x2() + mod
        self.set_x2(newx2)
    
    #get completely new dna
    def newValues(self):
        newx1 = random.uniform(-4.0, 4.0)
        newx2 = random.uniform(-4.0, 4.0)
        self.set_x1(newx1)
        self.set_x2(newx2)
        
    #mutation for sexual reproduction    
    def mutate(self):
        
        num = random.random()
        if (num > 0.82) & (num < 0.87):
            self.modifyX1()
        elif (num > 0.87) & (num < 0.92):
            self.modifyX2()
        elif (num > 0.92) & (num < 0.97):
            self.modifyX1()
            self.modifyX2()
        elif num > 0.97:
            self.newValues()
        
        return

    #mutation for asexual reproduction
    def aMutate(self):
        num = random.random()
        if num < 0.45:
            self.modifyX1()
        elif (num > 0.45) & (num < 0.9):
            self.modifyX2()
        elif (num > 0.9) & (num < 0.95):
            self.modifyX1()
            self.modifyX2()
        else:
            self.newValues()
        return