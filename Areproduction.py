from os import remove
import random
import matplotlib.pyplot as plt
from matplotlib import cm, projections
from matplotlib.ticker import LinearLocator
from operator import attrgetter
import numpy as np
from rastrigins import Ras

###########
# for aesexual reproduction
###########

POPSIZE = 50
HALFPOP = (POPSIZE//2)-1

fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(16, 9))
ax.set_title('Original Population')

# Make data.
X = np.arange(-5.12, 5.12, 0.2)
Y = np.arange(-5.12, 5.12, 0.2)
X, Y = np.meshgrid(X, Y)
Z = 20 + (X**2) + (Y**2) - 10*(np.cos((2*np.pi*X)) + np.cos((2*np.pi*Y)))


# Plot the surface.
surf = ax.plot_surface(X, Y, Z, alpha=.2, cmap=cm.winter,
                       linewidth=0, antialiased=False)

# Customize the z axis.
ax.set_zlim(-100, 100)
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.02f}')

# Add a color bar which maps values to colours.
fig.colorbar(surf, shrink=0.5, aspect=5)

def calcFitness( popArray ):
    for i in range(POPSIZE):
        popArray[i].calc()

#find the total fitness of entire pop
def getMaxFitness( popArray ):
    max = 0.0
    for i in range(POPSIZE):
        max += popArray[i].fitness
        return max

def orderPop( popArray ):
    s = sorted(popArray, key=attrgetter('fitness'))
    return s

def removeScatters( popArray ):
    for i in popArray:
        ax.scatter(i.x1, i.x2, i.fitness, color='red', alpha=1).remove()

def addFittest( pa ):
    newPA = []
    for i in range(HALFPOP, -1, -1):
        #adds fittest half to mating pool.
        x1 = pa[i].get_x1()
        x2 = pa[i].get_x2()
        newMember = Ras(x1, x2)
        newPA.append(newMember)
    return newPA

def newMP( pa ):
    mp = addFittest(pa)
    for i in mp:
        i.aMutate()
    return mp

def newPop( popArray):
    #order pop, higher index = fitter
    popArray = orderPop(popArray)
    #matingPool = array of 5 fittest candidates *2
    matingPool = newMP(popArray)
    matingPool.extend(addFittest(popArray))
    calcFitness(matingPool)

    for i in matingPool:
        print(i.x1, i.x2, i.fitness)

    return matingPool


#array of population
popArray = []

#initialise & show population
for i in range(POPSIZE):
    x1 = random.uniform(-5.12, 5.12)
    x2 = random.uniform(-5.12, 5.12)
    data = Ras(x1, x2)
    popArray.append(data)

#draw on graph
calcFitness(popArray)
scArray = []
for i in popArray:
    scArray.append(ax.scatter(i.x1, i.x2, i.fitness, color='red', alpha=1))
    
plt.show()
print("original pop")
for i in popArray:
        print(i.x1, i.x2, i.fitness)


for i in range (10):
    title = 'Population: '
    title = (title + str(i))
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(16, 9))
    ax.set_title(title)

    print("population version: ", (i+1))
    popArray = newPop(popArray)

    for i in popArray:
        ax.scatter(i.x1, i.x2, i.fitness, color='red', alpha=1)
    
    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, alpha=.2, cmap=cm.winter,
                       linewidth=0, antialiased=False)

    # Customize the z axis.
    ax.set_zlim(-100, 100)
    ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter('{x:.02f}')

    # Add a color bar which maps values to colours.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show(block=False)

    move = input()

    if i == 9:
        break
    else:
        plt.close()

