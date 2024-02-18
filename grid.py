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
        self.pbc = False
        
        # Build the grid
        self.cells = dict()
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.cells[str(i)+';'+str(j)] = {'pos': [i, j],
                                                 'state': random.randint(0,1)}

        self.alive_cells = [self.cells[cell]['pos'] for cell in self.cells if self.cells[cell]['state'] == 1]

    def get_cells(self):
        out_cells = dict()
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                out_cells[str(i) + ';' + str(j)] = {'pos': [i, j], 
                                        'state': 0 + self.cells[str(i)+';'+str(j)]['state']}
        return out_cells

    def clear(self):
        # Clear the grid
        self.cells = dict()
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.cells[str(i)+';'+str(j)] = {'pos': [i, j],
                                                 'state': 0}

        self.alive_cells = []

    def reset_random(self):
        # Rebuild the grid
        self.cells = dict()
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.cells[str(i)+';'+str(j)] = {'pos': [i, j],
                                                 'state': random.randint(0,1)}

        self.alive_cells = [self.cells[cell]['pos'] for cell in self.cells if self.cells[cell]['state'] == 1]

    def toggle_cell(self, mpos):
        pos = [(mpos[0] - self.sim.display_offset[0]) * self.sim.width / self.sim.display_size[0], 
               (mpos[1] - self.sim.display_offset[1]) *  self.sim.height / self.sim.display_size[1]]
        x = (int(pos[0]) * int(self.sim.grid_size * 1.1) / self.sim.width) - int(self.sim.grid_size*0.09)
        y = (int(pos[1]) * int(self.sim.grid_size * 1.1) / self.sim.height) - int(self.sim.grid_size*0.09)
        idx = str(int(x)) + ';' + str(int(y))
        if idx in self.cells:
            old_state = 0 + self.cells[idx]['state']
            if old_state == 0:
                self.alive_cells.append(self.cells[idx]['pos'])
            elif old_state == 1:
                self.alive_cells.remove(self.cells[idx]['pos'])
            self.cells[idx]['state'] = int(1 - old_state)

    def get_neighbors(self, idx):
        i, j = self.cells[idx]['pos']
        # General neighbor indexes
        next_i, prev_i = i + 1, i - 1
        next_j, prev_j = j + 1, j - 1
        # Check for boundaries and resolve PBC
        if i == 0 and self.pbc:
            prev_i = self.grid_size - 1
        if i == (self.grid_size - 1) and self.pbc:
            next_i = 0
        if j == 0 and self.pbc:
            prev_j = self.grid_size - 1
        if j == (self.grid_size - 1) and self.pbc:
            next_j = 0

        neighbor_pos = [str(next_i) + ';' + str(j),
                        str(prev_i) + ';' + str(j),
                        str(i) + ';' + str(next_j),
                        str(i) + ';' + str(prev_j),
                        str(next_i) + ';' + str(next_j),
                        str(prev_i) + ';' + str(next_j),
                        str(next_i) + ';' + str(prev_j),
                        str(prev_i) + ';' + str(prev_j)]

        # Check that the neighbor positions are actually in the grid
        for n_pos in neighbor_pos.copy():
            if not n_pos in self.cells:
                neighbor_pos.remove(n_pos)

        return neighbor_pos

    def get_alive_condition(self, idx):
        neighbor_pos = self.get_neighbors(idx)

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


# Class for grid patterns
class GridAsset():
    def __init__(self, sim):
        self.alive_cells = []
        self.sim = sim
    
    def set_alive_cells(self, pattern):
        self.alive_cells = pattern.copy()

    def rotate(self):
        # Do a pi/2 clock rotation
        new_alive_cells = []
        for pos in self.alive_cells.copy():
            new_alive_cells.append([-pos[1], pos[0]])
        self.set_alive_cells(new_alive_cells)

    def flip(self):
        # Do a flip over the y axis
        new_alive_cells = []
        for pos in self.alive_cells.copy():
            new_alive_cells.append([-pos[0], pos[1]])
        self.set_alive_cells(new_alive_cells)

    def print_to_grid(self, mpos, grid):
        # Get reference cell position from mouse pos
        ref_pos = [(mpos[0] - self.sim.display_offset[0]) * self.sim.width / self.sim.display_size[0], 
               (mpos[1] - self.sim.display_offset[1]) *  self.sim.height / self.sim.display_size[1]]
        ref_x = (int(ref_pos[0]) * int(self.sim.grid_size * 1.1) / self.sim.width) - int(self.sim.grid_size*0.09)
        ref_y = (int(ref_pos[1]) * int(self.sim.grid_size * 1.1) / self.sim.height) - int(self.sim.grid_size*0.09)
        # Print pattern to the grid
        for pos in self.alive_cells:
            idx = str(int(pos[0] + ref_x)) + ';' + str(int(pos[1] + ref_y))
            if idx in grid.cells:
                grid.cells[idx]['state'] = 1
                if not grid.cells[idx]['pos'] in grid.alive_cells:
                    grid.alive_cells.append(grid.cells[idx]['pos'])

    def render(self, surf, mpos):
        # Get reference from mouse pos
        ref_pos = [(mpos[0] - self.sim.display_offset[0]) * self.sim.width / self.sim.display_size[0], 
                (mpos[1] - self.sim.display_offset[1]) *  self.sim.height / self.sim.display_size[1]]
        ref_x = (int(ref_pos[0]) * int(self.sim.grid_size * 1.1) / self.sim.width) - int(self.sim.grid_size * 0.09)
        ref_y = (int(ref_pos[1]) * int(self.sim.grid_size * 1.1) / self.sim.height) - int(self.sim.grid_size*0.09)
        toggle_pos = [int(ref_x) * self.sim.width // int(self.sim.grid_size * 1.1), 
                      int(ref_y) * self.sim.height // int(self.sim.grid_size * 1.1)]
        
        # Render grey squares at the position of each 
        # cell in the pattern
        for cell in self.alive_cells:
            pos = [(int(self.sim.grid_size*0.09) + cell[0]) * self.sim.width // int(self.sim.grid_size * 1.1), 
                   (int(self.sim.grid_size*0.09) + cell[1]) * self.sim.height // int(self.sim.grid_size * 1.1)]
            cell_surf = pygame.Surface((self.sim.width // int(self.sim.grid_size * 1.1), 
                                        self.sim.height // int(self.sim.grid_size * 1.1)))
            cell_surf.fill((200,200,200))
            surf.blit(cell_surf, (toggle_pos[0] + pos[0], toggle_pos[1] + pos[1]))