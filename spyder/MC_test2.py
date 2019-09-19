import numpy as np
rand = np.random.rand

particles = 1000000
left = 0
right = 0
absorbedU1 = 0
absorbedU2 = 0
absorbedW1 = 0
absorbedW2 = 0
absorbedW3 = 0
bornInUranium1 = 0
bornInUranium2 = 0

# Course region array where each number is a plane
cRegion = np.array([0.0, 2.0, 4.0, 6.0, 8.0, 10.0])
# Array for the number of fine regions
fRegion = np.array([3, 22, 3, 22, 3])
# Array to input the material taht is used
material = np.array([0, 1, 0, 1, 0])

# Cross section data for Uranium.
U_cross_section = np.array([0.8, 0.4, 1.2])
# Cross section data for Water
W_cross_section = np.array([0.1, 0.9, 1.0])

# Variables for geometry
XPlane0 = 0
XPlane2 = 2
XPlane4 = 4
XPlane6 = 6
XPlane8 = 8
XPlane10 = 10


for test in range(particles):
    # Tells if neutron is absorbed or escapes
    alive = True
    # Tells if the neutron is in Water1
    inWater1 = False
    # Tells if the neutron is in Uranium1
    inUranium1 = False
    # Tells is neutron is in Water2
    inWater2 = False
    # Tells if neutron is in Uranium2
    inUranium2 = False
    # Tells if neutron is in Water3
    inWater3 = False
    
    
    # Decide which uranium the neutron is born in.
    if rand() < 0.5:
        # Give the neutron a position in Uranium1
        position = (XPlane4 - XPlane2)*rand()+XPlane2
        bornInUranium1 += 1
        inUranium1 = True
    else:
        # Give the neutron a position in Uranium2
        position = (XPlane8 - XPlane6)*rand()+XPlane6 
        bornInUranium2 += 1
        inUranium2 = True
    
    # Gives neutron direction
    mu = 2 * rand() - 1
    
    # While neutron is not absorbed
    while alive:

        while inUranium1:
            # Calculates distance traveled by neutron before an interaction
            dist = -np.log(rand()) / U_cross_section[2]
            # Calculate position in x direction
            position += mu * dist
            # If particle leaves left boundary
            if position <= XPlane2:
                position = XPlane2
                inUranium1 = False
                inWater1 = True
            # If particel leaves right boundary
            elif position >= XPlane4:
                position = XPlane4
                inUranium1 = False
                inWater2 = True
            # If particle stays in uranium and is absorbed
            elif U_cross_section[2]*rand() < U_cross_section[0]:
                absorbedU1 += 1
                alive = False
                inUranium1 = False
            # If particle scatters
            else:
                # Gives neutron direction
                mu = 2 * rand() - 1
                
        while inUranium2:
            # Calculates distance traveled by neutron before an interaction
            dist = -np.log(rand()) / U_cross_section[2]
            # Calculate position in x direction
            position += mu * dist
            # If particle leaves left boundary
            if position <= XPlane6:
                position = XPlane6
                inUranium2 = False
                inWater2 = True
            # If particel leaves right boundary
            elif position >= XPlane8:
                position = XPlane8
                inUranium2 = False
                inWater3 = True
            # If particle stays in uranium and is absorbed
            elif U_cross_section[2]*rand() < U_cross_section[0]:
                absorbedU2 += 1
                alive = False
                inUranium2 = False
            # If particle scatters
            else:
                # Gives neutron direction
                mu = 2 * rand() - 1
                
        while inWater1:
            # Calculates distance traveled by neutron before an interaction
            dist = -np.log(rand()) / W_cross_section[2]
            # Calculate position in x direction
            position += mu * dist
            # If neutron leaves left boundary
            if position <= XPlane0:
                left += 1
                inWater1 = False
                alive = False
            # If particel leaves right boundary
            elif position >= XPlane2:
                position = XPlane2
                inWater1 = False
                inUranium1 = True
            # If neutron is absorbed
            elif W_cross_section[2]*rand() < W_cross_section[0]:
                absorbedW1 += 1
                inWater1 = False
                alive = False
            # If neutron scatters
            else:
                # Gives neutron direction
                mu = 2 * rand() - 1
                
        while inWater2:
            # Calculates distance traveled by neutron before an interaction
            dist = -np.log(rand()) / W_cross_section[2]
            # Calculate position in x direction
            position += mu * dist
            
            # If neutron leaves left boundary
            if position <= XPlane4:
                position = XPlane4
                inWater2 = False
                inUranium1 = True
            # If particel leaves right boundary
            elif position >= XPlane6:
                position = XPlane6
                inWater2 = False
                inUranium2 = True
            # If neutron is absorbed
            elif W_cross_section[2]*rand() < W_cross_section[0]:
                absorbedW2 += 1
                inWater2 = False
                alive = False
            # If neutron scatters
            else:
                # Gives neutron direction
                mu = 2 * rand() - 1
                
        while inWater3:
            # Calculates distance traveled by neutron before an interaction
            dist = -np.log(rand()) / W_cross_section[2]
            # Calculate position in x direction
            position += mu * dist
            
            # If neutron leaves left boundary
            if position <= XPlane8:
                position = XPlane8
                inWater3 = False
                inUranium2 = True
            # If particel leaves right boundary
            elif position >= XPlane10:
                right += 1
                inWater3 = False
                alive = False
            # If neutron is absorbed
            elif W_cross_section[2]*rand() < W_cross_section[0]:
                absorbedW3 += 1
                inWater3 = False
                alive = False
            # If neutron scatters
            else:
                # Gives neutron direction
                mu = 2 * rand() - 1

# Adds total neutrons for debugging
total = left + right + absorbedU1 + absorbedU2
total += absorbedW1 + absorbedW2 + absorbedW3

print("Left boundary:          ", left)
print("Right boundary:         ", right)
print("Absorbed uranium1:      ", absorbedU1)
print("Absorbed uranium2:      ", absorbedU2)
print("Absorbed water1:        ", absorbedW1)
print("Absorbed water2:        ", absorbedW2)
print("Absorbed water3:        ", absorbedW3)
print("Total:                  ", total)
print("Born in 1:              ", bornInUranium1)
print("Born in 2:              ", bornInUranium2)