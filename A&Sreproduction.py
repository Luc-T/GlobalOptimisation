import random
import matplotlib.pyplot as plt
from matplotlib import cm, projections
from matplotlib.ticker import LinearLocator
from operator import attrgetter
import numpy as np
from rastrigins import Ras

##########
# for reproduction using parents
##########

POPSIZE = 50
HALFPOP = (POPSIZE//2)-1

fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(16, 9))

# Make data.
X = np.arange(-5, 5, 0.2)
Y = np.arange(-5, 5, 0.2)
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


def orderPop( popArray ):
    s = sorted(popArray, key=attrgetter('fitness'))
    return s

def reproduce(p1, p2):
    b = bool(random.getrandbits(1))
    if b:
        child = Ras(p1.get_x1(), p2.get_x2())
    else:
        child = Ras(p2.get_x1(), p1.get_x2())
    
    return child

#pick a parent based on fitness
def pickOne( pA ):
    index = 0
    r = random.random()
    while (r > 0):
        r = r - pA[index].get_prob()
        index +=1

    index -= 1
    return pA[index]

def newPop( popArray):
    #order pop, higher index = fitter
    popArray = orderPop(popArray)
    Fitsum = 0
    Probsum = 0
    for i in popArray:
        Fitsum += i.get_fitness()
    #create normalised probability score
    
    for i in popArray:
        mod = (i.get_fitness() / Fitsum)
        i.set_prob(1 / mod)
        Probsum += i.get_prob()
    
    for i in popArray:
        i.set_prob((i.get_prob() / Probsum))
    
     
    #create a new pop
    newPop = []
    
    for i in range(POPSIZE):
        parent1 = pickOne(popArray)
        #loop until parent2 has different x1 & x2 to parent1
        parent2 = pickOne(popArray)
        child = reproduce(parent1, parent2)
        if (parent1.get_x1() == parent2.get_x1()) & (parent1.get_x2() == parent2.get_x2()):
            child.aMutate()
        else:
            child.mutate()
            #print("")

                 
        newPop.append(child)

    calcFitness(newPop)

    return newPop


#array of population
popArray = []

#initialise & show population
for i in range(POPSIZE):
    x1 = random.uniform(-4.0, 4.0)
    x2 = random.uniform(-4.0, 4.0)
    data = Ras(x1, x2)
    popArray.append(data)

#draw on graph
calcFitness(popArray)

for i in popArray:
    ax.scatter(i.x1, i.x2, i.fitness, color='red', alpha=1)
    
plt.show()
print("original pop")
popArray = orderPop(popArray)
for i in popArray:
        print(i.x1, i.x2, i.fitness)


for i in range (10):
    title = 'Population: '
    title = (title + str(i))
    print("Offspring population version: ", (i+1))
    popArray = newPop(popArray)
    popArray = orderPop(popArray)
    for i in popArray:
        print(i.x1, i.x2, i.fitness,   )
    
    #show new genneration on graph
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(16, 9))
    ax.set_title(title)
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

    plt.show()
    
