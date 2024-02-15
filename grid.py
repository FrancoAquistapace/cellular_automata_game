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
        for i in range(grid_size):
            for j in range(grid_size):
                self.cells[str(i)+';'+str(j)] = 0

        self.alive_cells = [(4, 5), (5, 5), (5, 4)]

    def update(self):
        return None

    def render(self, surf):
        # Render a white square at the position of each 
        # cell that is alive
        for cell in self.alive_cells:
            pos = [cell[0] * self.sim.width // 10, cell[1] * self.sim.height // 10]
            cell_surf = pygame.Surface((self.sim.width // 10, self.sim.height // 10))
            cell_surf.fill((255,255,255))
            surf.blit(cell_surf, pos)