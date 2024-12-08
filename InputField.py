from CONSTANTS import *
import pygame
class InputField:
    def __init__(self, x, y, width, height, font, default_text="", text_color=BLACK, border_color=BLACK):
        """
        Initialize an InputField for user text input.
        
        :param x: X position of the input box.
        :param y: Y position of the input box.
        :param width: Width of the input box.
        :param height: Height of the input box.
        :param font: Pygame font object.
        :param default_text: Default text in the input box.
        :param text_color: Color of the text inside the input box.
        :param border_color: Color of the input box border.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text = default_text
        self.text_color = text_color
        self.border_color = border_color
        self.active = False
        self.cursor_visible = True  # Control blinking cursor
        self.cursor_timer = 0  # Timer for cursor blinking

    def draw(self, screen):
        # Draw the white background
        pygame.draw.rect(screen, WHITE, self.rect)

        # Draw the border
        pygame.draw.rect(screen, self.border_color, self.rect, 2)

        # Render the text inside the input box
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

        # Draw blinking cursor if active
        if self.active and self.cursor_visible:
            # Calculate cursor position based on text width
            cursor_x = self.rect.x + 5 + text_surface.get_width() + 2
            cursor_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
            cursor_height = text_surface.get_height()
            pygame.draw.line(screen, self.text_color, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state if clicked inside the field
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False  # Deactivate on Enter
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]  # Remove the last character
            else:
                # Append the character to the text
                self.text += event.unicode

    def update(self):
        # Blinking cursor logic
        if self.active:
            self.cursor_timer += 1
            if self.cursor_timer % 30 == 0:  # Toggle every 30 frames
                self.cursor_visible = not self.cursor_visible
        else:
            self.cursor_visible = False  # Hide cursor if not active
