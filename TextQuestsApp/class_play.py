import pygame
from random import choices
import os


class Text:
    def __init__(self, x: int, y: int, size: int, font, fcolor, text: str, visible: bool):
        self.x = x
        self.y = y
        self.size = size
        self.fcolor = fcolor
        self.text = text
        self.visible = visible
        self.font = pygame.font.Font(font, self.size)

    def draw(self, screen):
        if self.visible:
            if pygame.font:
                text = self.font.render(self.text, True, self.fcolor)
                textpos = text.get_rect(centerx=self.x, y=self.y)
                screen.blit(text, textpos)

    

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, size: int, font, fcolor, tcolor, text: str, visible: bool):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.size = size
        self.fcolor = fcolor
        self.tcolor = tcolor
        self.text = text
        self.visible = visible
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.strings = []
        if pygame.font:
            self.font = pygame.font.Font(font, self.size)


        current_string = ""
        for i in self.text:
            if self.font.size(current_string)[0] >= (self.width-30) and i in [" ", ",", ".", "!", "?", ":", ";"]:
                current_string += i
                self.strings.append(current_string)
                current_string = ""
            else:
                current_string += i
        self.strings.append(current_string)
            
        
        self.strings_to_draw = []
        for index, item in enumerate(self.strings):
            surf = self.font.render(item, True, self.tcolor)
            if len(self.strings) == 1:
                rect = surf.get_rect(centerx=self.rect.center[0], centery = self.rect.center[1])
            else:
                rect = surf.get_rect(centerx=self.rect.center[0], y = (self.y+((self.size+5))*(index+1)))
            self.strings_to_draw.append((surf, rect))
        

    def draw(self, screen):
            if self.visible:
                pygame.draw.rect(screen, self.fcolor, self.rect)
                for surf, rect in self.strings_to_draw:
                    screen.blit(surf, rect)
    
        
    def update(self, fcolor, tcolor):
        self.fcolor = fcolor
        self.tcolor = tcolor
        self.strings = []
        current_string = ""
        for i in self.text:
            if self.font.size(current_string)[0] >= (self.width-30) and i in [" ", ",", ".", "!", "?", ":", ";"]:
                current_string += i
                self.strings.append(current_string)
                current_string = ""
            else:
                current_string += i
        self.strings.append(current_string)
            
        
        self.strings_to_draw = []
        for index, item in enumerate(self.strings):
            surf = self.font.render(item, True, self.tcolor)
            rect = surf.get_rect(centerx=self.rect.center[0], y = (self.y+((self.size+5))*(index+1)))
            self.strings_to_draw.append((surf, rect))



    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and self.visible:
            if self.rect.collidepoint(event.pos):
                return True

        return False
    

class TextField:
    def __init__(self, x: int, y: int, width: int, height: int, size: int, font, fcolor, tcolor, text: str, visible: bool):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.size = size
        self.fcolor = fcolor
        self.tcolor = tcolor
        self.text = text
        self.visible = visible
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.visible_lines = self.height//(self.size+5)-1
        self.first_visible = 0
        self.strings = []
        
        if pygame.font:
            self.font = pygame.font.Font(font, self.size)


        current_string = "          "
        for i in self.text:
            if  i == "#":
                self.strings.append(current_string)
                current_string = "          "
            else:
                if self.font.size(current_string)[0] >= (self.width-200) and i in [" ", ",", ".", "!", "?", ":", ";"]:
                    current_string += i
                    self.strings.append(current_string)
                    current_string = ""
                else:
                    current_string += i
        self.strings.append(current_string)
            
        
        self.strings_to_draw = []
        visible_strings = self.strings[self.first_visible:(self.first_visible+self.visible_lines)]
        for index, item in enumerate(visible_strings):
            surf = self.font.render(item, True, self.tcolor)
            rect = surf.get_rect(x=self.x+30, y = (self.y+((self.size+5))*(index+1)))
            self.strings_to_draw.append((surf, rect))

    def draw(self, keys, screen):
        if self.visible:
            if keys[pygame.K_UP]:
                if self.first_visible > 0:
                    self.first_visible -=1
            elif keys[pygame.K_DOWN]:
                if self.first_visible < (len(self.strings)-self.visible_lines):
                    self.first_visible +=1
                
            
            self.strings_to_draw = []
            visible_strings = self.strings[self.first_visible:(self.first_visible+self.visible_lines)]
            for index, item in enumerate(visible_strings):
                surf = self.font.render(item, True, self.tcolor)
                rect = surf.get_rect(x=self.x+30, y = (self.y+((self.size+5))*(index+1)))
                self.strings_to_draw.append((surf, rect))
            pygame.draw.rect(screen, self.fcolor, self.rect)
            for surf, rect in self.strings_to_draw:
                screen.blit(surf, rect)

    
    def _rebuild_strings(self):
        self.strings = []
        current_string = "          "
        for i in self.text:
            if i == "#":
                self.strings.append(current_string)
                current_string = "          "
            else:
                if self.font.size(current_string)[0] >= (self.width-150) and i in [" ", ",", ".", "!", "?", ":", ";"]:
                    current_string += i
                    self.strings.append(current_string)
                    current_string = ""
                else:
                    current_string += i
        self.strings.append(current_string)
                    
        
        self.strings_to_draw = []
        visible_strings = self.strings[self.first_visible:(self.first_visible+self.visible_lines)]
        for index, item in enumerate(visible_strings):
            surf = self.font.render(item, True, self.tcolor)
            rect = surf.get_rect(x=self.x+30, y = (self.y+((self.size+5))*(index+1)))
            self.strings_to_draw.append((surf, rect))
    

    
    def change_text(self, text):
        self.text = text
        self.first_visible = 0
        self._rebuild_strings() 

    def update(self, fcolor, tcolor):
        self.first_visible = 0
        self.fcolor = fcolor
        self.tcolor = tcolor
        self._rebuild_strings()


class Image:
    def __init__(self, x, y, width, height, dir, file):
        self.x = x 
        self.y = y
        self.width = width
        self.height = height
        self.dir = dir 
        self.file = file  
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        


    def draw(self, screen):
        self.orig_image = pygame.image.load(os.path.join(self.dir, self.file)).convert_alpha()
        self.image = pygame.transform.scale(self.orig_image, (self.width, self.height))
        screen.blit(self.image, self.rect)
         


class Condition:
    def __init__(self, name, sign, value):
        self.name = name
        self.sign = sign
        self.value = value


class Variable:
    def __init__(self, name: str, value: int):
        self.name=name
        self.initial_v = value
        self.value = value

    def __str__(self):
        return f"Назва: {self.name}, Значення: {self.value}"

class Change:
    def __init__(self, name: str,  change:str, value: int,):
        self.name=name
        self.change=change
        self.value = value
        
class Theme:
    def __init__(self, name: str, background_color, fill_color, font_color, dir=None, file=None, w=None, h=None):
            self.name=name
            self.background_color=background_color
            self.fill_color=fill_color
            self.font_color=font_color
            self.image = None
            self.dir = dir
            self.file = file
            self.w = w
            self.h = h
            if dir and file:
                self.image = Image(0, 0, self.w, self.h, self.dir, self.file)

    def draw(self, screen):
        if self.image:
            self.image.draw(screen)

class Scene:
    def __init__(self, name: str, text: str, theme: Theme, choices, changes: list[Change]):
        self.name = name
        self.text = text
        self.theme = theme
        self.choices = choices
        self.changes = changes

    def change(self, quest):
        if self.changes:
            for c in self.changes:
                for i in quest.variables:
                    if i.name == c.name:
                        if c.change == "=":
                            i.value = c.value
                        if c.change == "+":
                            i.value += c.value
                        if c.change == "-":
                            i.value -= c.value




class Choice:
    def __init__(self, name: str, scenes: dict, conditions: list[Condition]):
        self.name=name
        self.scenes=scenes
        self.conditions = conditions

    def check_availability(self, quest):
        if not self.conditions:
            return True
        is_available = True
        for c in self.conditions:
            if c.sign == "=":
                for i in quest.variables:
                    if c.name == i.name:
                        if not i.value == c.value:
                            is_available = False
            elif c.sign == "<":
                for i in quest.variables:
                    if c.name == i.name:
                        if not i.value < c.value:
                            is_available = False
            elif c.sign == ">":
                for i in quest.variables:
                    if c.name == i.name:
                        if not i.value > c.value:
                            is_available = False
        return is_available
    
    def get_scene(self, quest):
        if len(self.scenes) == 1:
            return list(self.scenes.keys())[0]
        else:
            items = []
            percentages = []
            for key, value in self.scenes.items():
                items.append(key)

                if callable(value):
                    value = value(quest)
                if value >= 0:
                    percentages.append(value)
                else:
                    percentages.append(0)

            selected_item = choices(population=items, weights=percentages, k=1)[0]
            return selected_item
          

class Quest:
    def __init__(self, name: str, description: str, scenes: list[Scene], themes: list[Theme], variables: list[Variable], first_scene_index=0,):
            self.name = name
            self.description = description
            self.scenes = scenes
            self.themes = themes
            self.variables = variables
            self.first_scene_index = first_scene_index
            self.current_scene = scenes[first_scene_index]

    def get_variable(self, name):
        for i in self.variables:
            if i.name == name:
                return i

        raise ValueError(f"Змінну {name} не знайдено")


    

