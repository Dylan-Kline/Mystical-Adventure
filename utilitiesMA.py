# @ utilitiesMA.py
# Utilities for game classes
import pygame

class Clickable_text:

    def __init__(self, text, x, y, font, color, scene):
        self.text = text
        self.scene = scene
        self.x = self.scale_text_to_dialogue(x, y)[0]
        self.y = self.scale_text_to_dialogue(x, y)[1]
        self.font = font
        self.color = color
        self.hover_color = (255, 255, 255) # White
        self.visible = False
        self.text_surfaces = list() # Holds each rendered text_surface to draw
        self.rects = list() # Holds the corresponding rect objects for each text_surface
        self.wrap_text() # Wraps the text and creates text surfaces and their rects
        
    def draw(self, surface):
        if self.visible:
            for text_surface in self.text_surfaces:
                surface.blit(text_surface[0], text_surface[1])
        
    # tells if text box was clicked
    def was_clicked(self, mouse_pos):
        if self.visible:
            for rect in self.rects:
                if rect.collidepoint(mouse_pos):
                    return True
        return False
    
    # Changes text color if mouse hovers over it
    def hovering(self, mouse_pos):
        is_hovering = any(rect.collidepoint(mouse_pos) for rect in self.rects)
        color = self.hover_color if is_hovering else self.color
        self.text_surfaces = [
                                [self.font.render(text_surface[2], True, pygame.Color(color)), text_surface[1], text_surface[2]] 
                                for text_surface in self.text_surfaces
                            ]
    
    def change_visibility(self):
        self.visible = not self.visible
    
    def set_x(self, x):
        self.x = x
        
    def set_y(self, y):
        self.y = y
              
    def set_visibility(self, truthValue):
        if type(truthValue) is bool:
            self.visible = truthValue
              
    def scale_text_to_dialogue(self, box_x, box_y):
        
        margin_X = 10
        margin_Y = 10
        position_X = margin_X + box_x
        position_Y = margin_Y + box_y
        
        return (position_X, position_Y)

    def wrap_text(self):
        
        # Maximum width of text
        max_width = 515
        
        words = self.text.split()
        lines = list()
        current_line = words[0]
        
        for word in words[1:]:
            # Check if current line width is within margins
            if self.font.size(current_line + " " + word)[0] <= max_width:
                current_line += " " + word
            
            else:
                lines.append(current_line)
                current_line = word
                
        lines.append(current_line)
        
        # Render each text surface for each line of text
        self.text_surfaces = [
            [self.font.render(line, True, pygame.Color(self.color)), (self.x, self.y + (i * self.font.get_height())), line]
            for i, line in enumerate(lines)]
        
        # Render each rectangle for each text surface
        self.rects = [text_surface[0].get_rect(topleft=(text_surface[1])) for text_surface in self.text_surfaces]
        
            