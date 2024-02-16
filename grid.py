'''
Copyright 2024 Franco Aquistapace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

# Import modules
import pygame
import random


# Define Grid class
class Grid():
    def __init__(self, sim, grid_size):
        '''
        Params:
            sim : Simulation
                Instance of the Simulation class on which
                the grid will be implemented.
            grid_size : int
                Number of cells along each dimension of the 
                grid. This means that the total amount of 
                cells in the grid will be grid_size * grid_size.
        Output:
            Initializes an instance of the Grid class.
        '''
        self.sim = sim
        self.grid_size = grid_size
        
        # Build the grid
        self.cells = dict()
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.cells[str(i)+';'+str(j)] = {'pos': [i, j],
                                                 'state': random.randint(0,1)}

        self.alive_cells = [self.cells[cell]['pos'] for cell in self.cells if self.cells[cell]['state'] == 1]

    def reset_random(self):
        # Rebuild the grid
        self.cells = dict()
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.cells[str(i)+';'+str(j)] = {'pos': [i, j],
                                                 'state': random.randint(0,1)}

        self.alive_cells = [self.cells[cell]['pos'] for cell in self.cells if self.cells[cell]['state'] == 1]

    def get_alive_condition(self, idx):
        i, j = self.cells[idx]['pos']
        neighbor_pos = [str(i + 1) + ';' + str(j),
                        str(i - 1) + ';' + str(j),
                        str(i) + ';' + str(j + 1),
                        str(i) + ';' + str(j - 1),
                        str(i + 1) + ';' + str(j + 1),
                        str(i - 1) + ';' + str(j + 1),
                        str(i + 1) + ';' + str(j - 1),
                        str(i - 1) + ';' + str(j - 1)]

        # Check that the neighbor positions are actually in the grid
        for n_pos in neighbor_pos.copy():
            if not n_pos in self.cells:
                neighbor_pos.remove(n_pos)

        alive_neighbors = sum([self.cells[pos]['state'] for pos in neighbor_pos])
        
        # Compute alive condition:
        # Death by underpopulation
        if self.cells[idx]['state'] == 1 and alive_neighbors < 2:
            return -1
        # Death by overpopulation
        if self.cells[idx]['state'] == 1 and alive_neighbors > 3:
            return -1
        # Birth by reproduction
        if self.cells[idx]['state'] == 0 and alive_neighbors == 3:
            return 1

        return 0

    def update(self):
        # Init empty list for new alive cells
        new_alive = []
        alive_cells = []
        dead_cells = []
        for cell in self.cells:
            alive_condition = self.get_alive_condition(cell)
            if alive_condition == 1:
                new_alive.append(self.cells[cell]['pos'])
                alive_cells.append(cell)
            elif alive_condition == -1:
                self.alive_cells.remove(self.cells[cell]['pos'])
                dead_cells.append(cell)

        self.alive_cells.extend(new_alive)
        # Update cells
        for cell in alive_cells:
            self.cells[cell]['state'] = 1
        for cell in dead_cells:
            self.cells[cell]['state'] = 0

    def render(self, surf):
        # Render a white square at the position of each 
        # cell that is alive
        for cell in self.alive_cells:
            pos = [(int(self.sim.grid_size*0.09) + cell[0]) * self.sim.width // int(self.sim.grid_size * 1.1), 
                   (int(self.sim.grid_size*0.09) + cell[1]) * self.sim.height // int(self.sim.grid_size * 1.1)]
            cell_surf = pygame.Surface((self.sim.width // int(self.sim.grid_size * 1.1), 
                                        self.sim.height // int(self.sim.grid_size * 1.1)))
            cell_surf.fill((255,255,255))
            surf.blit(cell_surf, pos)