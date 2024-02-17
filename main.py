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
from button import PlayButton, RefocusButton, RandomResetButton, ClearButton, PBCButton, MenuButton


# Define main simulation class
class Simulation():
    def __init__(self):
        self.width = 640
        self.height = 640
        self.margin_color = (107, 103, 105)
        self.menu_color = (85, 82, 84)
        self.button_color_off = (200, 200, 200)
        self.button_color_on = (255, 255, 255)
        self.text_color_1 = (0, 0, 0)
        self.text_color_2 = (250, 250, 250)
        self.text_color_3 = (178, 176, 178)

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
        self.centered = True

        self.clock = pygame.time.Clock()

        # Initialize the grid
        self.grid_size = 100
        self.grid = Grid(self, self.grid_size)
        self.iteration = 0

        # Initialize font
        self.font = pygame.font.SysFont('Times New Roman', 26)

        # Initialize buttons
        self.play_button = PlayButton(self, self.button_color_on, self.button_color_off, 3, 50, 
                            color=self.margin_color, on_color=self.margin_color, size=40)
        self.refocus_button = RefocusButton(self, self.button_color_on, self.button_color_off, 3, 90, 
                            color=self.margin_color, on_color=self.margin_color, size=40)
        self.rr_button = RandomResetButton(self, self.button_color_on, self.button_color_off, 3, 130, 
                            color=self.margin_color, on_color=self.margin_color, size=40)
        self.clear_button = ClearButton(self, self.button_color_on, self.button_color_off, 3, 170, 
                            color=self.margin_color, on_color=self.margin_color, size=40)
        self.pbc_button = PBCButton(self, self.button_color_on, self.button_color_off, 3, 210, 
                            color=self.margin_color, on_color=self.margin_color, size=40)
        self.menu_button = MenuButton(self, self.button_color_on, self.text_color_3, 
                            self.width * 0.7, 7, 
                            color=self.margin_color, on_color=self.margin_color, size=30)

        # Initialize iteration label
        self.iteration_box = pygame.Surface((0.12 * self.width, 0.05 * self.height))
        self.iteration_box.fill((0,0,0))
        self.iteration_label = self.font.render('Iteration', True, self.text_color_1)

        # Initialize patterns visualization
        self.patterns_box = pygame.Surface((0.3 * self.width, 0.07 * self.height))
        self.patterns_box.fill(self.menu_color)
        self.menu_box = pygame.Surface((0.3 * self.width, self.height))
        self.menu_box.fill(self.menu_color)
        self.patterns_label = self.font.render('Patterns', True, self.text_color_3)
        self.show_menu = False
        self.menu_y = (0.06 - 1) * self.height
        self.menu_speed = 30

        # Simulation manipulation
        self.running = False
        self.grid_area = pygame.Rect(0.07 * self.width, 0.07 * self.height, self.width, self.height)

        # Cell toggle visualization
        self.toggle_rect = pygame.Surface((self.width // int(self.grid_size * 1.1), 
                                        self.height // int(self.grid_size * 1.1)))
        self.toggle_rect.fill((200,200,200))

        # Initialize margins
        self.margin_y = pygame.Surface((0.07 * self.width, self.height))
        self.margin_x = pygame.Surface((self.width, 0.07 * self.height))
        self.margin_y.fill(self.margin_color)
        self.margin_x.fill(self.margin_color)

    def run(self):
        # Main simulation loop
        while True:
            self.screen.fill((0, 0, 0))
            self.display.fill((0, 0, 0))
            self.display.set_colorkey((0, 0, 0))

            # Update display offset
            self.display_offset[0] += self.display_scroll[0] * self.scroll_speed
            self.display_offset[1] += self.display_scroll[1] * self.scroll_speed

            # Limit the offset so that the user cannot go outside the
            # grid
            self.display_offset[0] = min(self.display_offset[0], 0)
            self.display_offset[0] = max(self.display_offset[0], 
                                         self.screen.get_size()[0] - self.display_size[0])
            self.display_offset[1] = min(self.display_offset[1], 0)
            self.display_offset[1] = max(self.display_offset[1], 
                                         self.screen.get_size()[1] - self.display_size[1])

            # Get mouse position and button status
            mpos = pygame.mouse.get_pos()
            on_play = self.play_button.update(mpos)
            on_focus = self.refocus_button.update(mpos)
            on_reset = self.rr_button.update(mpos)
            on_clear = self.clear_button.update(mpos)
            on_pbc = self.pbc_button.update(mpos)
            on_menu = self.menu_button.update(mpos)
            on_grid = self.grid_area.collidepoint(mpos)

            # If the menu has been requested update its position
            if self.show_menu:
                self.menu_y += self.menu_speed
                self.menu_y = min(self.menu_y, 0)

            if not self.show_menu:
                self.menu_y -= self.menu_speed
                self.menu_y = max(self.menu_y, (0.06 - 1) * self.height)

            # Update grid and render alive cells
            if self.running:
                self.grid.update()
                self.iteration += 1
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
                        # If refocus is used reset the display settings
                        if on_focus and not self.centered:
                            self.display_size = list(self.screen.get_size())
                            self.display_scroll = [0, 0]
                            self.display_offset = [0, 0]
                            self.centered = True
                        # If random reset, generate a new random grid
                        if on_reset:
                            self.grid.reset_random()
                            self.iteration = 0
                        # If on clear button then clear the grid
                        if on_clear:
                            self.grid.clear()
                            self.iteration = 0
                        # If on PBC, toggle PBC configuration in the grid
                        if on_pbc:
                            self.grid.pbc = not self.grid.pbc
                        # If on menu button open patterns menu
                        if on_menu:
                            self.show_menu = not self.show_menu
                        # If we are in the grid area try to toggle the 
                        # closest cell
                        if on_grid:
                            self.grid.toggle_cell(mpos)
                        

                    # Zoom in
                    if event.button == 4:
                        self.display_size[0] += self.display_zoom
                        self.display_size[1] += self.display_zoom
                        self.centered = False
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
                        self.centered = False
                    if event.key == pygame.K_RIGHT:
                        self.display_scroll[0] = -1
                        self.centered = False
                    if event.key == pygame.K_UP:
                        self.display_scroll[1] = 1
                        self.centered = False
                    if event.key == pygame.K_DOWN:
                        self.display_scroll[1] = -1
                        self.centered = False

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


            # Show where the cell toggle would occur
            pos = [(mpos[0] - self.display_offset[0]) * self.width / self.display_size[0], 
                   (mpos[1] - self.display_offset[1]) *  self.height / self.display_size[1]]
            x = (int(pos[0]) * int(self.grid_size * 1.1) / self.width)
            y = (int(pos[1]) * int(self.grid_size * 1.1) / self.height)
            toggle_pos = [int(x) * self.width // int(self.grid_size * 1.1), 
                          int(y) * self.height // int(self.grid_size * 1.1)]
            self.display.blit(self.toggle_rect, toggle_pos)
            
            # Blit display and update screen
            scaled_display = pygame.transform.scale(self.display, 
                                                    self.display_size)
            self.screen.blit(scaled_display, self.display_offset)

            # Render black margins for the buttons and data
            self.screen.blit(self.margin_y, (0, 0))
            self.screen.blit(self.margin_x, (0, 0))

            # Render buttons on top of everything
            self.play_button.render(self.screen)
            self.refocus_button.render(self.screen)
            self.rr_button.render(self.screen)
            self.clear_button.render(self.screen)
            self.pbc_button.render(self.screen)

            # Render iteration text
            iteration_str = str(self.iteration) if self.iteration <= 9999 else '+9999'
            iteration_text = self.font.render(iteration_str, True, self.text_color_2)
            self.screen.blit(self.iteration_box, (self.width * 0.237, self.height * 0.01))
            self.screen.blit(iteration_text, (self.width * 0.245, self.height * 0.014))
            self.screen.blit(self.iteration_label, (self.width * 0.09, self.height * 0.014))

            # Render patterns text and menu
            self.screen.blit(self.menu_box, (self.width * 0.7, self.menu_y))
            self.screen.blit(self.patterns_box, (self.width * 0.7, 0))
            self.menu_button.render(self.screen)
            self.screen.blit(self.patterns_label, (self.width * 0.75, self.height * 0.011))

            pygame.display.update()
            self.clock.tick(60)

Simulation().run()