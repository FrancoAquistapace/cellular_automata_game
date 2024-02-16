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