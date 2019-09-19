import numpy as np
rand = np.random.rand

particles = 10000
U_width = 2
left = 0
right = 0
absorbed = 0

# Cross section data for Uranium.
U_a_cross_section = 0.8
U_s_cross_section = 0.4
# Add scatter and absorption cross sections for total.
U_t_cross_section = U_a_cross_section + U_s_cross_section
# For loop to simulate 'particles' number of neutrons
for test in range(particles):
    # Value to tell if the neutron scatters or gets absorbed
    alive = True
    # Create random position for neutron to be born in
    position = U_width * (rand() - 0.5)
    
    # While neutron is not absorbed
    while alive:
        # Gives neutron direction
        mu = 2 * rand() - 1
        # Calculates distance traveled by neutron before an interaction
        dist = -np.log(rand()) / U_t_cross_section
        position += mu * dist
        
        if position > (U_width/2):  # Particle leaves right boundary.
            right += 1
            alive = False
        elif position < (-U_width/2):  # Particle leaves left boundary.
            left += 1
            alive = False
        # If partice does not leave it has an interaction
        # Particle was absorbed
        elif (U_t_cross_section * rand()) < U_a_cross_section: 
            absorbed += 1
            alive = False
    
# Adds total neutrons for debugging
total = left + right + absorbed

print("Left boundary:  ", left)
print("Right boundary: ", right)
print("Absorbed:       ", absorbed)
print("Total:          ", total)