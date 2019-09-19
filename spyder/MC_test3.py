import numpy as np
import matplotlib.pyplot as plt
rand = np.random.rand

particles = 1000000

# Tracking variables
left = 0
right = 0


# Course region array where each number is a plane
cRegion =  [0.0, 0.09, 1.17, 1.26, 1.35, 2.43, 2.52, 2.61, 3.69, 3.78]
# Array for the number of fine regions
fRegion =  [  3,   22,   3,   3,   22,   3, 3, 22, 3]
# Array to input the material that is used
material = [  1,   0,   1, 1, 0, 1,  1,   0,   1]

# More tracking variables
numCell = len(material)
numSources = 0
bornInCell = [0] * numCell

# Create list of absorbed neutrons in cells of variable length
fCell = []
for i in range(numCell):
    fCell.append([0] * fRegion[i])

# Cross section data for Uranium. absorb, scatter, total
U_cross_section = [0.8, 0.4, 1.2]
# Cross section data for Water. absorb, scatter, total
W_cross_section = [0.1, 0.9, 1.0]

# Template to place the materials cross section in an array
cellxs = [[0, 0, 0] for x in range(numCell)]

# Function to define material cross section and count sources
for i in range(numCell):
    if material[i] == 0:
        cellxs[i] = U_cross_section
        numSources += 1
    elif material[i] == 1:
        cellxs[i] = W_cross_section

# Function to sort find which fine region the neutron was absorbed in                
def findFRegion(curCell, pos):
    Found = False
    x = 0
    width = cRegion[curCell+1]-cRegion[curCell]
    while not Found:
        if pos > cRegion[curCell] + width * x / fRegion[curCell] \
            and pos <= cRegion[curCell] + width * (x+1) / fRegion[curCell]:
            Found = True
            fCell[curCell][x] += 1
        else:
            x += 1


for test in range(particles):
    # Tells if neutron is absorbed or escapes
    alive = True
    
    # Give the neutron a starting position in a source
    initSource = rand()
    sourceCount = 0
    for i in range(numCell):
        # If cell is uranium
        if material[i] == 0:
            # and if cell is between certain 1/ number of sources
            if initSource <= (float)(sourceCount+1)/numSources \
                and initSource >= (float)(sourceCount)/numSources:
                # Position is between coarse region surrounding source
                position = (cRegion[i+1] - cRegion[i])*rand()+cRegion[i]
                bornInCell[i] += 1
                inCell = i
            sourceCount += 1
    
    
    
    # Gives neutron direction
    mu = 2 * rand() - 1
    
    # While neutron is not absorbed
    while alive:
        
        # Calculates distan 9,   3ce traveled by neutron before an interaction
        dist = -np.log(rand()) / cellxs[inCell][2]
        # Calculate position in x direction
        position += mu * dist
        # If particle leaves left boundary
        if position <= cRegion[inCell]:
            # and if the current cell has one to the left of it
            if inCell > 0:
                # in cell moves to the cell to the left
                position = cRegion[inCell]
                inCell -= 1
            else:
                # if particle leaves left boundary it 'dies'
                alive = False  
                left += 1
        # If particle leaves right boundary
        elif position >= cRegion[inCell+1]:
            # and if the current cell has one to the right of it
            if inCell < numCell - 1:
                # in cell moves to the cell to the right
                position = cRegion[inCell+1]
                inCell += 1
            else:
                # If particles leaves right boundary it 'dies'
                alive = False
                right += 1
        # If particle stays in uranium and is absorbed
        elif cellxs[inCell][2] * rand() < cellxs[inCell][0]:
            # Find and tally the fine region it is absorbed in
            findFRegion(inCell, position)
            alive = False
        # If particle scatters
        else:
            # Gives neutron direction
            mu = 2 * rand() - 1
        
# Adds total neutrons for debugging 
total = left + right
for i in range(numCell):
    total += sum(fCell[i])

for i in range(numCell):
    print("Born in cell", i, end = ':')
    print("      ", bornInCell[i])

print("Total born:          ", sum(bornInCell))
print('\n')
print("Left boundary:       ", left)
print("Right boundary:      ", right)

for i in range(numCell):
    print("Absorbed cell", i, end = ':')
    print("     ", sum(fCell[i]))
    print("                            ", fCell[i])
    
print("Total:               ", total)

x = [(cRegion[i+1] - cRegion[i]) / fRegion[i] for i, c in enumerate(cRegion[:-1]) for _ in range(fRegion[i])]
x = np.concatenate(([0], np.cumsum(x)))
x = 0.5 * (x[1:] + x[:-1])
flux = np.array([vv for v in fCell for vv in v])

plt.plot(x, flux)
plt.show()

