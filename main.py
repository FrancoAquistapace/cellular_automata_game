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
import sys

# Import scripts
from grid import Grid
from button import Button


# Define main simulation class
class Simulation():
    def __init__(self):
        self.width = 640
        self.height = 640

        # Initialize screen and display
        pygame.init()
        pygame.display.set_caption('Cellular Automata')
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.display = pygame.Surface((self.width, self.height))

        # Display manipulation settings
        self.display_size = list(self.screen.get_size())
        self.display_zoom = 4
        self.display_offset = [0, 0]
        self.display_scroll = [0, 0]
        self.scroll_speed = 10

        self.clock = pygame.time.Clock()

        # Initialize the grid
        self.grid_size = 100
        self.grid = Grid(self, self.grid_size)

        # Initialize buttons
        self.b = Button(10, 40)

        # Simulation manipulation
        self.running = False

    def run(self):
        # Main simulation loop
        while True:
            self.screen.fill((0, 0, 0))
            self.display.fill((0, 0, 0))

            # Update display offset
            self.display_offset[0] += self.display_scroll[0] * self.scroll_speed
            self.display_offset[1] += self.display_scroll[1] * self.scroll_speed

            # Get mouse position and button status
            mpos = pygame.mouse.get_pos()
            on_play = self.b.update(mpos)

            # Update grid and render alive cells
            if self.running:
                self.grid.update()
            self.grid.render(self.display)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if on_play:
                            self.running = not self.running
                    # Zoom in
                    if event.button == 4:
                        self.display_size[0] += self.display_zoom
                        self.display_size[1] += self.display_zoom
                    # Zoom out
                    if event.button == 5:
                        self.display_size[0] = max(self.display_size[0] - self.display_zoom, 
                                                    self.screen.get_size()[0])
                        self.display_size[1] = max(self.display_size[1] - self.display_zoom, 
                                                    self.screen.get_size()[1])

                if event.type == pygame.KEYDOWN:
                    # Activate scrolling
                    if event.key == pygame.K_LEFT:
                        self.display_scroll[0] = 1
                    if event.key == pygame.K_RIGHT:
                        self.display_scroll[0] = -1
                    if event.key == pygame.K_UP:
                        self.display_scroll[1] = 1
                    if event.key == pygame.K_DOWN:
                        self.display_scroll[1] = -1

                if event.type == pygame.KEYUP:
                    # Deactivate scrolling
                    if event.key == pygame.K_LEFT:
                        self.display_scroll[0] = 0
                    if event.key == pygame.K_RIGHT:
                        self.display_scroll[0] = 0
                    if event.key == pygame.K_UP:
                        self.display_scroll[1] = 0
                    if event.key == pygame.K_DOWN:
                        self.display_scroll[1] = 0
            
            # Blit display and update screen
            self.screen.blit(pygame.transform.scale(self.display, 
                                                    self.display_size), 
                                                    self.display_offset)

            # Render buttons on top of everything
            self.b.render(self.screen)

            pygame.display.update()
            self.clock.tick(60)

Simulation().run()