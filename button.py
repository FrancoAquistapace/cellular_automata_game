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
import pygame

# General button class
class Button():
    def __init__(self, x, y, size=20, color=(200, 200, 200), 
                                      on_color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.on_color = on_color
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.img = pygame.Surface((self.size, self.size))
        self.img.fill(self.color)

    def update(self, mpos):
        self.img.fill(self.color)
        if self.rect.collidepoint(mpos):
            self.img.fill(self.on_color)
            return True
        return False

    def render(self, surf):
        surf.blit(self.img, (self.x, self.y))


# Play button
class PlayButton(Button):
    def __init__(self, sim, play_color_on, play_color_off, x, y, 
                 size=20, color=(200, 200, 200), 
                 on_color=(255, 255, 255)):
        super().__init__(x, y, size, color, on_color)
        self.play_color = play_color_off
        self.play_color_off = play_color_off
        self.play_color_on = play_color_on
        self.sim = sim

    def update(self, mpos):
        self.img.fill(self.color)
        self.play_color = self.play_color_off
        if self.rect.collidepoint(mpos):
            self.img.fill(self.on_color)
            self.play_color = self.play_color_on
            return True
        return False
    
    def render(self, surf):
        super().render(surf)
        if self.sim.running:
            render_points = [
                (self.x + self.size / 4, self.y + self.size / 4),
                (self.x + 3 * self.size / 4, self.y + self.size / 4),
                (self.x + 3 * self.size / 4, self.y + 3 * self.size / 4),
                (self.x + self.size / 4, self.y + 3 * self.size / 4)
            ]
        else:
            render_points = [
                (self.x + self.size / 4, self.y + self.size / 4),
                (self.x + 3 * self.size / 4, self.y + self.size / 2),
                (self.x + self.size / 4, self.y + 3 * self.size / 4)
            ]

        pygame.draw.polygon(surf, self.play_color, render_points)


# Reset camera button
class RefocusButton(PlayButton):
    def __init__(self, sim, play_color_on, play_color_off, x, y, 
                 size=20, color=(200, 200, 200), 
                 on_color=(255, 255, 255)):
        super().__init__(sim, play_color_on, play_color_off, x, y, 
                         size, color, on_color)
    
    def render(self, surf):
        surf.blit(self.img, (self.x, self.y))

        center = (self.x + self.size / 2, self.y + self.size / 2)
        pygame.draw.circle(surf, self.play_color, center, 
                            radius=self.size/3, width=int(self.size/13))
        # Smaller circle when display is not centered
        if not self.sim.centered:
            pygame.draw.circle(surf, self.play_color, center, 
                            radius=self.size/7, width=int(self.size/15))


# Reset random button
class RandomResetButton(PlayButton):
    def __init__(self, sim, play_color_on, play_color_off, x, y, 
                 size=20, color=(200, 200, 200), 
                 on_color=(255, 255, 255)):
        super().__init__(sim, play_color_on, play_color_off, x, y, 
                         size, color, on_color)

    def render(self, surf):
        surf.blit(self.img, (self.x, self.y))

        rect_pos = [(self.x + 0.25 * self.size, self.y + 0.2 * self.size),
                    (self.x + 0.25 * self.size, self.y + 0.4 * self.size), 
                    (self.x + 0.25 * self.size, self.y + 0.6 * self.size),
                    (self.x + 0.45 * self.size, self.y + 0.2 * self.size),
                    (self.x + 0.45 * self.size, self.y + 0.4 * self.size), 
                    (self.x + 0.45 * self.size, self.y + 0.6 * self.size),
                    (self.x + 0.65 * self.size, self.y + 0.2 * self.size),
                    (self.x + 0.65 * self.size, self.y + 0.4 * self.size), 
                    (self.x + 0.65 * self.size, self.y + 0.6 * self.size)]
        for pos in rect_pos:
            pygame.draw.rect(surf, self.play_color, 
                            [pos[0], pos[1], self.size//10, self.size//10], 0)


# Clear button
class ClearButton(PlayButton):
    def __init__(self, sim, play_color_on, play_color_off, x, y, 
                 size=20, color=(200, 200, 200), 
                 on_color=(255, 255, 255)):
        super().__init__(sim, play_color_on, play_color_off, x, y, 
                         size, color, on_color)

    def render(self, surf):
        surf.blit(self.img, (self.x, self.y))
        # First line
        start_pos_1 = (self.x + self.size / 4, self.y + self.size / 4)
        end_pos_1 = (self.x + 3 * self.size / 4, self.y + 3 * self.size / 4)
        pygame.draw.line(surf, self.play_color, start_pos_1, end_pos_1, width=int(self.size/13))
        # Second line
        start_pos_2 = (self.x + 3 * self.size / 4, self.y + self.size / 4)
        end_pos_2 = (self.x + self.size / 4, self.y + 3 * self.size / 4)
        pygame.draw.line(surf, self.play_color, start_pos_2, end_pos_2, width=int(self.size/13))


# PBC Button
class PBCButton(PlayButton):
    def __init__(self, sim, play_color_on, play_color_off, x, y, 
                 size=20, color=(200, 200, 200), 
                 on_color=(255, 255, 255)):
        super().__init__(sim, play_color_on, play_color_off, x, y, 
                         size, color, on_color)

    def render(self, surf):
        pygame.draw.rect(surf, self.play_color, 
                            [self.x + 0.2 * self.size, self.y + 0.2 * self.size, 
                             0.6 * self.size, 0.6 * self.size], int(self.size/13))

        if self.sim.grid.pbc:
            # Draw horizontal lines
            x_range = [self.x + 0.2 * self.size, self.x + 0.8 * self.size]
            y_1 = self.y + 0.3 * self.size
            y_2 = self.y + 0.65 * self.size
            pygame.draw.line(surf, self.sim.margin_color, 
                            (x_range[0], y_1), (x_range[1], y_1), 
                             width=int(self.size/10))
            pygame.draw.line(surf, self.sim.margin_color, 
                            (x_range[0], y_2), (x_range[1], y_2), 
                             width=int(self.size/10))
            # Draw vertical lines
            y_range = [self.y + 0.2 * self.size, self.y + 0.8 * self.size]
            x_1 = self.x + 0.3 * self.size
            x_2 = self.x + 0.65 * self.size
            pygame.draw.line(surf, self.sim.margin_color, 
                            (x_1, y_range[0]), (x_1, y_range[1]), 
                             width=int(self.size/10))
            pygame.draw.line(surf, self.sim.margin_color, 
                            (x_2, y_range[0]), (x_2, y_range[1]), 
                             width=int(self.size/10))


# Menu button
class MenuButton(PlayButton):
    def __init__(self, sim, play_color_on, play_color_off, x, y, 
                 size=20, color=(200, 200, 200), 
                 on_color=(255, 255, 255)):
        super().__init__(sim, play_color_on, play_color_off, x, y, 
                         size, color, on_color)
    
    def render(self, surf):
        if self.sim.show_menu:
            render_points = [
                (self.x + self.size / 4, self.y + self.size / 4),
                (self.x + 3 * self.size / 4, self.y + self.size / 4),
                (self.x + self.size / 2, self.y + 3 * self.size / 4)
            ]

        else:
            render_points = [
                (self.x + self.size / 4, self.y + self.size / 4),
                (self.x + 3 * self.size / 4, self.y + self.size / 2),
                (self.x + self.size / 4, self.y + 3 * self.size / 4)
            ]

        pygame.draw.polygon(surf, self.play_color, render_points)